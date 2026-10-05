#!/usr/bin/env python3
"""PAROS cognitive cycle: weighted learned rules (kit version 0.1.0).

A deterministic engine, no LLM inside. The thinking work (what is a new lesson,
did a rule help, is it still valid) is done by a caretaker agent in its cycle
mode, inside a normal agent session on the owner's subscription, not on API
credits. This script only keeps records, computes weights and renders views.

Stores (the JSON and markdown are the truth, the rest is derived):
  registry.json          canonical: the learned rules (ID, source, text, scope)
  events/<host>.jsonl    canonical, append-only, one writer per machine: everything
                         that happened to the rules (born, confirm, used, outcome,
                         reviewed, deprecated, revived)
  state.json             the history of cycles (only `apply` writes it)
  lease.json             who is running a cycle right now (90 minute lease)
  weights.json           DERIVED, can be recomputed at any time
  CYCLES.md              the log of cycle reports, for humans

The weight (0..1) is computed from the events, in order:
  born        base by evidence (owner decision 0.40, human correction 0.35,
              measured 0.30, convergence 0.30, agent inference 0.15)
  confirm     w += 0.15 * (1 - w)
  helpful     w += 0.12 * (1 - w)
  harmful     w -= 0.30 * w, and the rule goes to review
  neutral     only the exposure grows
  idle        after 60 days without use: x0.95 per month (human-origin rules
              have a 0.15 floor, so they never fall asleep on their own)
  dormant     w < 0.12: left out of the loaded list, but kept in the file

Configuration (environment):
  PAROS_COGNITION_DIR    where the stores live (default: this script's folder)
  PAROS_VAULT            the vault root (default: detected upwards from the data
                         folder, by a .obsidian, .git or AGENTS.md marker)
  PAROS_LEARNING_ROOTS   folders (relative to the vault, separated by os.pathsep)
                         scanned for changed LEARNINGS.md and observations/*.md;
                         default: the whole vault
  PAROS_MEMORY_DIR       optional: a folder of agent memory files (relative to the
                         vault). If set, changed rule-type memory files go into the
                         packet, and rules targeting a file there are marked in the
                         memory index by an ID prefix on the index line
  PAROS_MEMORY_INDEX     the memory index file name (default MEMORY.md)
  PAROS_CYCLE_DOC        the cycle procedure the hook points to
                         (default kits/cognition/CYCLE.md)

Commands:
  due [--hook] [--hours N]   is a cycle due; --hook: UserPromptSubmit hook mode
  stop-hook                  Stop hook: rules cited as [L-xxxx] in the answer get a
                             use event (outcome: pending)
  used L-0001 [--outcome helpful|harmful|neutral|pending] [--note ...]
  packet [--out F]           the caretaker agent's work packet for the cycle
  apply decisions.json       the caretaker's decisions: events, weights, render, report
  report                     the current state as a report (no cycle)
  render                     rewrite the generated blocks in the target files
"""
import argparse
import datetime as dt
import json
import os
import re
import socket
import sys
import uuid
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def _detect_vault(start):
    for p in [start, *start.parents]:
        if any((p / m).exists() for m in (".obsidian", ".git", "AGENTS.md")):
            return p
    return Path.cwd()


COG = Path(os.environ.get("PAROS_COGNITION_DIR") or Path(__file__).resolve().parent).resolve()
VAULT = Path(os.environ["PAROS_VAULT"]).resolve() if os.environ.get("PAROS_VAULT") else _detect_vault(COG)
REGISTRY = COG / "registry.json"
EVENTS = COG / "events"
STATE = COG / "state.json"
LEASE = COG / "lease.json"
WEIGHTS = COG / "weights.json"
CYCLES = COG / "CYCLES.md"
MEMORY_DIR = (VAULT / os.environ["PAROS_MEMORY_DIR"]).resolve() if os.environ.get("PAROS_MEMORY_DIR") else None
MEMORY_INDEX = os.environ.get("PAROS_MEMORY_INDEX", "MEMORY.md")
CYCLE_DOC = os.environ.get("PAROS_CYCLE_DOC", "kits/cognition/CYCLE.md")


def learning_roots():
    raw = os.environ.get("PAROS_LEARNING_ROOTS")
    if not raw:
        return [VAULT]
    return [VAULT / r for r in raw.split(os.pathsep) if r.strip()]


DUE_HOURS = 4
LEASE_MIN = 90
BASE = {"owner_decision": 0.40, "human_correction": 0.35, "measured": 0.30,
        "convergence": 0.30, "agent_inferred": 0.15}
HUMAN_ORIGIN = {"owner_decision", "human_correction"}
DORMANT = 0.12
IDLE_DAYS = 60
TIERS = [(0.25, "seedling", "░"), (0.50, "growing", "▒"), (0.75, "strong", "▓"), (1.01, "root", "█")]
CITE = re.compile(r"\[(L-\d{4})\]")
BEGIN = "<!-- COGNITION:BEGIN"
END = "<!-- COGNITION:END -->"
SKIP_PARTS = {"_archive", "_archiv", "versions", ".git", "node_modules", ".obsidian", ".trash"}


def now():
    return dt.datetime.now(dt.timezone.utc)


def iso(t=None):
    return (t or now()).isoformat(timespec="seconds")


def parse(ts):
    t = dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
    return t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc)


def host():
    h = os.environ.get("PAROS_HOST") or socket.gethostname().lower().split(".")[0]
    return re.sub(r"[^a-z0-9-]", "-", h.lower()) or "unknown"


def load(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, path)


def append_event(ev):
    EVENTS.mkdir(parents=True, exist_ok=True)
    ev.setdefault("id", uuid.uuid4().hex[:12])
    ev.setdefault("ts", iso())
    ev.setdefault("host", host())
    with (EVENTS / f"{host()}.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    return ev


def all_events():
    out = []
    for p in sorted(EVENTS.glob("*.jsonl")) if EVENTS.exists() else []:
        for line in p.read_text(encoding="utf-8").splitlines():
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    out.sort(key=lambda e: e.get("ts", ""))
    return out


def tier(w):
    for lim, name, ch in TIERS:
        if w < lim:
            return name, ch
    return TIERS[-1][1], TIERS[-1][2]


# ---------------------------------------------------------------- weights

def compute(registry=None, events=None, at=None):
    registry = registry or load(REGISTRY, {"next_id": 1, "rules": {}})
    events = events if events is not None else all_events()
    at = at or now()
    state = load(STATE, {})
    since = parse(state["telemetry_since"]) if state.get("telemetry_since") else at
    res = {}
    for rid in registry["rules"]:
        res[rid] = {"w": 0.0, "status": "active", "exposure": 0, "helpful": 0, "harmful": 0,
                    "neutral": 0, "pending": 0, "confirm": 0, "last": None, "review": False}
    resolved = {e["ref"] for e in events if e.get("type") == "outcome" and e.get("ref")}
    for e in events:
        rid = e.get("rule")
        if rid not in res:
            continue
        s, t = res[rid], e.get("type")
        if t == "born":
            s["w"] = BASE.get(registry["rules"][rid].get("evidence"), 0.15)
        elif t == "confirm":
            s["w"] += 0.15 * (1 - s["w"]); s["confirm"] += 1
        elif t == "used":
            s["exposure"] += 1
            if e.get("outcome", "pending") == "pending" and e["id"] not in resolved:
                s["pending"] += 1
            elif e.get("outcome") in ("helpful", "harmful", "neutral"):
                apply_outcome(s, e["outcome"])
        elif t == "outcome":
            apply_outcome(s, e.get("value"))
        elif t == "reviewed":
            s["review"] = False
        elif t == "deprecated":
            s["status"] = "deprecated"
        elif t == "revived":
            s["status"] = "active"; s["w"] = max(s["w"], 0.2)
        # A birth registered before telemetry started (an inventory of old rules)
        # does not count as activity: otherwise every old rule would look fresh.
        if t != "born" or parse(e["ts"]) >= since:
            s["last"] = e["ts"]
    for rid, s in res.items():
        last = max(parse(s["last"]) if s["last"] else since, since)
        idle = (at - last).days
        if idle > IDLE_DAYS:
            w = s["w"] * 0.95 ** ((idle - IDLE_DAYS) / 30)
            if registry["rules"][rid].get("evidence") in HUMAN_ORIGIN:
                w = max(w, min(s["w"], 0.15))
            s["w"] = w
        s["w"] = round(min(max(s["w"], 0.0), 1.0), 3)
        if s["status"] != "deprecated":
            if s["review"]:
                s["status"] = "review"
            elif s["w"] < DORMANT:
                s["status"] = "dormant"
    return res


def apply_outcome(s, v):
    if v == "helpful":
        s["helpful"] += 1; s["w"] += 0.12 * (1 - s["w"])
    elif v == "harmful":
        s["harmful"] += 1; s["w"] -= 0.30 * s["w"]; s["review"] = True
    elif v == "neutral":
        s["neutral"] += 1


# ---------------------------------------------------------------- hooks

def cmd_due(a):
    state, lease = load(STATE, {}), load(LEASE, {})
    last = parse(state["last_cycle_at"]) if state.get("last_cycle_at") else None
    hours = (now() - last).total_seconds() / 3600 if last else None
    due = hours is None or hours >= a.hours
    leased = lease.get("at") and (now() - parse(lease["at"])).total_seconds() < LEASE_MIN * 60
    if not a.hook:
        print(json.dumps({"due": due, "hours_since": hours, "leased": bool(leased), "lease": lease}, ensure_ascii=False))
        return
    if not due or leased:
        return
    try:
        inp = json.loads(sys.stdin.read() or "{}")
    except Exception:
        inp = {}
    save(LEASE, {"host": host(), "session": inp.get("session_id", ""), "at": iso()})
    ago = "never yet" if hours is None else f"{hours:.0f} hours ago"
    msg = (f"PAROS cognitive cycle is due (the last one ran {ago}; this session holds the lease). "
           "While you serve the person's request, start your caretaker agent in cycle mode, in the BACKGROUND, "
           f"with this prompt: \"Mode: cycle. Run the cognitive cycle as described in {CYCLE_DOC} "
           "and return the report verbatim.\" When it comes back, put the report block unchanged at the end "
           "of your answer. Do not ask about it and do not explain it; the owner decided this.")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": msg}}, ensure_ascii=False))


def last_assistant_texts(transcript):
    """From the end of the transcript: the assistant texts after the last real user message."""
    try:
        with open(transcript, "rb") as f:
            f.seek(0, 2); size = f.tell(); f.seek(max(0, size - 600_000))
            lines = f.read().decode("utf-8", "ignore").splitlines()
    except Exception:
        return []
    out = []
    for line in reversed(lines):
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get("type") == "user" and isinstance(d.get("message", {}).get("content"), str):
            break
        if d.get("type") == "assistant" and not d.get("isSidechain"):
            for c in d.get("message", {}).get("content", []):
                if isinstance(c, dict) and c.get("type") == "text":
                    out.append((d.get("uuid", ""), c.get("text", "")))
    return out


def cmd_stop_hook(a):
    try:
        inp = json.loads(sys.stdin.read() or "{}")
    except Exception:
        return
    texts = []
    if inp.get("last_assistant_message"):
        texts.append(("last", inp["last_assistant_message"]))
    if inp.get("transcript_path"):
        texts += last_assistant_texts(inp["transcript_path"])
    reg = load(REGISTRY, {"rules": {}})["rules"]
    seen_p = COG / f".seen.{host()}.json"
    seen = load(seen_p, [])
    sid = inp.get("session_id", "")
    for uid, text in texts:
        for rid in sorted(set(CITE.findall(text))):
            key = f"{sid}:{rid}"
            if rid in reg and key not in seen:
                m = re.search(r"[^\n]*\[" + rid + r"\][^\n]*", text)
                append_event({"type": "used", "rule": rid, "outcome": "pending", "session": sid,
                              "transcript": inp.get("transcript_path", ""), "msg": uid,
                              "context": (m.group(0) if m else "")[:300]})
                seen.append(key)
    save(seen_p, seen[-2000:])


def cmd_used(a):
    reg = load(REGISTRY, {"rules": {}})["rules"]
    if a.rule not in reg:
        sys.exit(f"unknown rule: {a.rule}")
    ev = append_event({"type": "used", "rule": a.rule, "outcome": a.outcome, "note": a.note or ""})
    s = compute()[a.rule]
    print(f"{a.rule}: {a.outcome} recorded, weight now {s['w']:.2f} ({tier(s['w'])[0]}), event {ev['id']}")


# ---------------------------------------------------------------- cycle

NOT_HUMAN = ("<task-notification>", "<local-command-", "<system-reminder>")


def is_human_turn(d):
    """A real message from the person: a text user line, not meta (image, skill or agent
    message), not a notification or hook output."""
    c = d.get("message", {}).get("content")
    return (d.get("type") == "user" and isinstance(c, str) and not d.get("isMeta")
            and not d.get("isSidechain") and not c.lstrip().startswith(NOT_HUMAN))


def next_user_text(transcript, msg_uuid, limit=700, after_ts=None):
    """The person's first message after the citing answer: the basis for judging whether it helped.

    msg_uuid: the uuid of the citing assistant message. If it is "last" or empty (the Stop hook
    recorded it from last_assistant_message), the anchor is the event time (after_ts): the first
    person message later than that. Without an anchor the result is empty, never the first
    message of the session.
    """
    try:
        lines = Path(transcript).read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return None
    by_time = msg_uuid in ("", "last")
    if by_time and not after_ts:
        return ""
    anchor = parse(after_ts) if by_time else None
    found = False
    for line in lines:
        try:
            d = json.loads(line)
        except Exception:
            continue
        if by_time:
            try:
                found = bool(d.get("timestamp")) and parse(d["timestamp"]) > anchor
            except Exception:
                found = False
        elif not found and d.get("uuid") == msg_uuid:
            found = True
            continue
        if found and is_human_turn(d):
            return d["message"]["content"][:limit]
    return ""


RULE_MEMORY_TYPES = ("feedback", "reference")


def memory_type(p):
    """The `type` field of a memory file's frontmatter (top level or under metadata); empty on error."""
    try:
        txt = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    m = re.match(r"---\r?\n(.*?)\r?\n---", txt, re.S)
    t = re.search(r"(?m)^[ \t]*type:[ \t]*['\"]?([A-Za-z_-]+)", m.group(1)) if m else None
    return t.group(1).lower() if t else ""


def rel(p):
    try:
        return str(p.relative_to(VAULT)).replace("\\", "/")
    except ValueError:
        return str(p).replace("\\", "/")


def cmd_packet(a):
    reg = load(REGISTRY, {"next_id": 1, "rules": {}})
    events = all_events()
    w = compute(reg, events)
    state = load(STATE, {})
    last = state.get("last_cycle_at")
    resolved = {e["ref"] for e in events if e.get("type") == "outcome"}
    pending = []
    for e in events:
        if e.get("type") == "used" and e.get("outcome") == "pending" and e["id"] not in resolved:
            local = e.get("transcript") and Path(e["transcript"]).exists()
            age = (now() - parse(e["ts"])).days
            item = {"event": e["id"], "rule": e["rule"], "rule_text": reg["rules"].get(e["rule"], {}).get("text", ""),
                    "ts": e["ts"], "host": e.get("host"), "cited_in": e.get("context", "")}
            if local:
                item["next_user_message"] = next_user_text(e["transcript"], e.get("msg", ""), after_ts=e.get("ts"))
            elif not e.get("transcript"):
                item["note"] = "no transcript pointer: judge from the citation text and the note"
            elif age > 14:
                item["note"] = "older than 14 days and the transcript is not on this machine: neutral"
            else:
                continue  # another machine will judge it
            pending.append(item)
    review = [{"rule": rid, **reg["rules"][rid], "weight": s["w"], "harmful": s["harmful"],
               "helpful": s["helpful"]} for rid, s in w.items() if s["status"] == "review"]
    changed = []
    cutoff = parse(last).timestamp() if last else 0
    for root in learning_roots():
        if not root.exists():
            continue
        for p in root.rglob("LEARNINGS.md"):
            if SKIP_PARTS & set(p.parts):
                continue
            if p.stat().st_mtime > cutoff:
                changed.append(rel(p))
        for p in root.rglob("observations/*.md"):
            if p.name != "README.md" and not (SKIP_PARTS & set(p.parts)) and p.stat().st_mtime > cutoff:
                changed.append(rel(p))
    known_sources = sorted({r["source"] for r in reg["rules"].values() if r.get("source")})
    if MEMORY_DIR and MEMORY_DIR.exists():
        for p in sorted(MEMORY_DIR.glob("*.md")):
            r = rel(p)
            if p.name == MEMORY_INDEX or p.name.startswith(Path(MEMORY_INDEX).stem + ".") or p.stat().st_mtime <= cutoff:
                continue
            if p.name.startswith("feedback_") or memory_type(p) in RULE_MEMORY_TYPES or r in known_sources:
                changed.append(r)
    pkt = {"generated": iso(), "host": host(), "last_cycle_at": last, "cycle_no": state.get("cycles", 0) + 1,
           "rule_count": len(reg["rules"]), "pending_outcomes": pending, "review_queue": review,
           "changed_sources_since_last_cycle": sorted(set(changed)), "known_sources": known_sources,
           "decisions_schema": DECISIONS_SCHEMA}
    out = json.dumps(pkt, ensure_ascii=False, indent=1)
    if a.out:
        Path(a.out).write_text(out, encoding="utf-8"); print(a.out)
    else:
        print(out)


DECISIONS_SCHEMA = {
    "register": "[{skill, area, source, target, text, applies_when, origin_date, evidence, confirmations, still_valid, superseded_by}] new learned rules; evidence: owner_decision|human_correction|measured|convergence|agent_inferred",
    "confirm": "[{rule, note}] a new, independent confirmation of an existing rule",
    "outcomes": "[{event, rule, value: helpful|harmful|neutral, note}] judgements of pending uses",
    "reviews": "[{rule, decision: keep|refine|deprecate, note}] decisions on the review queue (refine: improve the text or scope, see the text/applies_when fields)",
    "questions": "[text] what to ask the owner (only if uncertain AND important)",
    "notes": "[text] short observations for the report",
}


def cmd_apply(a):
    dec = json.loads(Path(a.decisions).read_text(encoding="utf-8"))
    reg = load(REGISTRY, {"next_id": 1, "rules": {}})
    state = load(STATE, {})
    if not state.get("telemetry_since"):
        state["telemetry_since"] = iso()
    save(STATE, state)
    before = load(WEIGHTS, {}).get("rules", {})
    born, deprecated_now = [], []
    by_key = {(r.get("source"), r["text"]): rid for rid, r in reg["rules"].items()}
    for item in dec.get("register", []):
        key = (item.get("source"), item["text"])
        if key in by_key:
            continue
        rid = f"L-{reg['next_id']:04d}"
        reg["next_id"] += 1
        reg["rules"][rid] = {k: item.get(k) for k in
                             ("skill", "area", "source", "target", "text", "applies_when", "origin_date", "evidence")}
        reg["rules"][rid]["registered"] = iso()
        by_key[key] = rid
        save(REGISTRY, reg)
        append_event({"type": "born", "rule": rid, "note": item.get("origin_date") or ""})
        for _ in range(int(item.get("confirmations") or 0)):
            append_event({"type": "confirm", "rule": rid, "note": "inventory: later confirmation in the source"})
        if item.get("still_valid") is False:
            append_event({"type": "deprecated", "rule": rid, "note": item.get("superseded_by") or "no longer valid per the inventory"})
            deprecated_now.append(rid)
        born.append(rid)
    for c in dec.get("confirm", []):
        if c["rule"] in reg["rules"]:
            append_event({"type": "confirm", "rule": c["rule"], "note": c.get("note", "")})
    for o in dec.get("outcomes", []):
        if o.get("rule") in reg["rules"]:
            append_event({"type": "outcome", "rule": o["rule"], "ref": o.get("event"), "value": o["value"], "note": o.get("note", "")})
    for r in dec.get("reviews", []):
        rid = r["rule"]
        if rid not in reg["rules"]:
            continue
        if r["decision"] == "deprecate":
            append_event({"type": "deprecated", "rule": rid, "note": r.get("note", "")}); deprecated_now.append(rid)
        else:
            if r["decision"] == "refine":
                for k in ("text", "applies_when"):
                    if r.get(k):
                        reg["rules"][rid].setdefault("history", []).append({k: reg["rules"][rid].get(k), "until": iso()})
                        reg["rules"][rid][k] = r[k]
                save(REGISTRY, reg)
            append_event({"type": "reviewed", "rule": rid, "decision": r["decision"], "note": r.get("note", "")})
    save(REGISTRY, reg)
    w = compute(reg)
    snapshot = summarize(reg, w)
    state = load(STATE, {})
    state["cycles"] = state.get("cycles", 0) + 1
    state["last_cycle_at"] = iso()
    state["last_cycle_host"] = host()
    state.setdefault("history", []).append({"n": state["cycles"], "at": state["last_cycle_at"], "host": host(),
                                            "total": snapshot["active"], "mass": snapshot["mass"], "tiers": snapshot["tiers"]})
    save(STATE, state)
    save(WEIGHTS, {"computed": iso(), "rules": {k: {"w": v["w"], "status": v["status"]} for k, v in w.items()}})
    render(reg, w)
    text = report(reg, w, before, state, born=born, deprecated_now=deprecated_now,
                  outcomes=dec.get("outcomes", []), reviews=dec.get("reviews", []),
                  questions=dec.get("questions", []), notes=dec.get("notes", []))
    log_cycle(state["cycles"], text)
    try:
        LEASE.unlink()
    except Exception:
        pass
    print(text)


# ---------------------------------------------------------------- report

def summarize(reg, w):
    tiers = {name: 0 for _, name, _ in TIERS}
    extra = {"review": 0, "dormant": 0, "deprecated": 0}
    mass = 0.0
    for rid, s in w.items():
        if s["status"] in extra:
            extra[s["status"]] += 1
        else:
            tiers[tier(s["w"])[0]] += 1
            mass += s["w"]
    return {"tiers": tiers, **extra, "active": sum(tiers.values()), "mass": round(mass, 2)}


def spark(values):
    if not values:
        return ""
    chars = "▁▂▃▄▅▆▇█"
    lo, hi = min(values), max(values)
    return "".join(chars[3 if hi - lo < 0.05 else int((v - lo) / (hi - lo) * 7)] for v in values)


def report(reg, w, before=None, state=None, born=(), deprecated_now=(), outcomes=(), reviews=(), questions=(), notes=()):
    before = before or {}
    state = state or load(STATE, {})
    sm = summarize(reg, w)
    n = state.get("cycles", 0)
    when = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    L = []
    L.append(f"PAROS COGNITIVE CYCLE #{n}   {when}   machine: {host()}")
    L.append("=" * 64)
    t = sm["tiers"]
    L.append(f"Live knowledge: {sm['active']} rules, total weight {sm['mass']:.1f}")
    L.append(f"  █ root {t['root']:>3}   ▓ strong {t['strong']:>3}   ▒ growing {t['growing']:>3}   ░ seedling {t['seedling']:>3}")
    L.append(f"  ! review {sm['review']:>3}   · dormant {sm['dormant']:>3}   × retired {sm['deprecated']:>3}")
    hist = state.get("history", [])
    if len(hist) > 1:
        L.append(f"Growth (total weight per cycle): {spark([h['mass'] for h in hist])}  {hist[0]['mass']:.1f} -> {hist[-1]['mass']:.1f}")
    up = [r for r in w if r in before and w[r]["w"] > before[r]["w"] + 0.005]
    down = [r for r in w if r in before and w[r]["w"] < before[r]["w"] - 0.005]
    L.append("")
    L.append(f"This cycle: +{len(born)} new   ↑{len(up)} stronger   ↓{len(down)} weaker   "
             f"{len(list(reviews))} reviews closed   {len(list(deprecated_now))} retired")
    L.append("")
    L.append("HEAT MAP  (row = capability, cell = rule, darker = stronger)")
    areas = {}
    for rid, r in reg["rules"].items():
        if w[rid]["status"] == "deprecated":
            continue
        areas.setdefault(r.get("area") or "Other", {}).setdefault(r.get("skill") or "?", []).append(rid)
    for area in sorted(areas, key=lambda k: -sum(len(v) for v in areas[k].values())):
        skills = areas[area]
        aw = [w[x]["w"] for v in skills.values() for x in v]
        L.append(f"{area}  ({len(aw)} rules, mean {sum(aw) / len(aw):.2f})")
        for sk in sorted(skills, key=lambda k: -sum(w[x]["w"] for x in skills[k])):
            ids = sorted(skills[sk], key=lambda x: -w[x]["w"])
            cells = "".join("!" if w[x]["status"] == "review" else "·" if w[x]["status"] == "dormant"
                            else tier(w[x]["w"])[1] for x in ids)
            more = ""
            if len(cells) > 30:
                cells, more = cells[:30], f" +{len(ids) - 30}"
            L.append(f"  {sk[:28]:<28} {cells}{more}")
    act = [r for r in w if w[r]["status"] == "active"]
    top = sorted(act, key=lambda r: -w[r]["w"])[:5]
    L.append("")
    L.append("Strongest rules:")
    for r in top:
        L.append(f"  {r} {w[r]['w']:.2f}  {short(reg['rules'][r]['text'])}")
    if born and len(born) <= 12:
        L.append("Born now:")
        for r in born:
            L.append(f"  {r} {w[r]['w']:.2f}  {short(reg['rules'][r]['text'])}")
    if outcomes:
        L.append("Live use judged:")
        for o in list(outcomes)[:10]:
            mark = {"helpful": "+ helpful", "harmful": "- harmful", "neutral": "= neutral"}.get(o["value"], o["value"])
            L.append(f"  {o['rule']} {mark}: {short(o.get('note', ''), 60)}")
    if up:
        L.append("Stronger: " + ", ".join(f"{r} {before[r]['w']:.2f}->{w[r]['w']:.2f}" for r in up[:8]))
    if down:
        L.append("Weaker:   " + ", ".join(f"{r} {before[r]['w']:.2f}->{w[r]['w']:.2f}" for r in down[:8]))
    rv = [r for r in w if w[r]["status"] == "review"]
    if rv:
        L.append("Waiting for review: " + ", ".join(rv[:10]))
    for q in questions:
        L.append(f"QUESTION FOR THE OWNER: {q}")
    for x in notes:
        L.append(f"Note: {x}")
    L.append("=" * 64)
    L.append("Marking during work: [L-xxxx] = this decision depended on a learned rule.")
    return "\n".join(L)


def short(s, n=70):
    s = " ".join((s or "").split())
    return s if len(s) <= n else s[: n - 1] + "…"


def log_cycle(n, text):
    if not CYCLES.exists():
        CYCLES.write_text(
            f"---\ntitle: CYCLES\ndate: {dt.date.today().isoformat()}\nstatus: active\n"
            "description: Append-only log of the PAROS cognitive cycle reports: per cycle the state of the "
            "weighted knowledge, its heat map, and the rules born, strengthened, weakened and retired.\n"
            f"id: {uuid.uuid4()}\ntags: [paros, learning, cognitive-cycle]\n---\n\n"
            "# Cognitive cycles\n\n> Append-only. Written by `cognition.py apply`.\n", encoding="utf-8")
    with CYCLES.open("a", encoding="utf-8") as f:
        f.write(f"\n## Cycle #{n} ({dt.date.today().isoformat()})\n\n```text\n{text}\n```\n")


def cmd_report(a):
    reg = load(REGISTRY, {"next_id": 1, "rules": {}})
    print(report(reg, compute(reg), load(WEIGHTS, {}).get("rules", {})))


# ---------------------------------------------------------------- render

def render(reg, w):
    by_target = {}
    for rid, r in reg["rules"].items():
        if r.get("target"):
            by_target.setdefault(r["target"], []).append(rid)
    memory_ids = {}
    for target, ids in by_target.items():
        p = (VAULT / target).resolve()
        if MEMORY_DIR and MEMORY_DIR in p.parents:
            # Memory files carry no block; the rule ID goes onto the file's index line.
            for rid in ids:
                memory_ids[p.name] = rid
            continue
        if not p.exists() or p.suffix != ".md":
            continue
        live = sorted([x for x in ids if w[x]["status"] in ("active", "review")], key=lambda x: -w[x]["w"])
        sleep = [x for x in ids if w[x]["status"] == "dormant"]
        lines = [f"{BEGIN} (generated: cognition.py render; do not edit by hand) -->",
                 "## Learned rules with weights (cognitive cycle)",
                 "",
                 "If a decision of yours depends on one of these, mark it in the answer like this: `[L-xxxx]`; "
                 "that is how the caretaker learns whether the rule helped. Weight 0..1: in a conflict the higher "
                 "one wins, a seedling (below 0.25) is only a suggestion. The rule text in the body above or in its "
                 "source is authoritative; this list is an index.",
                 ""]
        for x in live:
            r, s = reg["rules"][x], w[x]
            name, ch = tier(s["w"])
            flag = " (under review)" if s["status"] == "review" else ""
            when = f" When: {r['applies_when']}." if r.get("applies_when") else ""
            lines.append(f"- `{x}` {ch} {s['w']:.2f} {name}{flag}: {r['text']}{when}")
        if sleep:
            lines.append(f"- Dormant (not applied by default, but kept): {', '.join(sleep)}")
        lines.append(END)
        txt = read_raw(p)
        eol = eol_of(txt)
        block = eol.join(lines)
        new = splice_block(txt, block, eol)
        if new is None:
            print(f"render: skipped, the generated block markers are ambiguous: {target}", file=sys.stderr)
            continue
        if new != txt:
            write_raw(p, new)
    idx = MEMORY_DIR / MEMORY_INDEX if MEMORY_DIR else None
    if memory_ids and idx and idx.exists():
        raw = read_raw(idx)
        eol = eol_of(raw)
        out = []
        for line in raw.splitlines():
            m = re.match(r"^- (`L-\d{4}` )?(\[.*?\]\(([^)]+)\).*)$", line)
            if m and m.group(3) in memory_ids:
                line = f"- `{memory_ids[m.group(3)]}` {m.group(2)}"
            out.append(line)
        new = eol.join(out) + eol
        if new != raw:
            write_raw(idx, new)


# A marker counts only at the start of its own line (a marker quoted in text or backticks does not).
BEGIN_LINE = re.compile(r"(?m)^" + re.escape(BEGIN) + r"\b[^\r\n]*(?=\r?$)")
END_LINE = re.compile(r"(?m)^" + re.escape(END) + r"[ \t]*(?=\r?$)")
BLOCK_RE = re.compile(r"(?ms)^" + re.escape(BEGIN) + r"\b[^\r\n]*(?=\r?$).*?^" + re.escape(END) + r"[ \t]*(?=\r?$)")


def read_raw(p):
    """Read without newline translation, so the write can keep the original line ending (CRLF or LF)."""
    with open(p, encoding="utf-8", newline="") as f:
        return f.read()


def write_raw(p, txt):
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(txt)


def eol_of(txt):
    crlf = txt.count("\r\n")
    return "\r\n" if crlf and crlf * 2 >= txt.count("\n") else "\n"


def splice_block(txt, block, eol):
    """Replace or append the generated block. None if the markers are ambiguous (then nothing is written).

    Only a marker at the start of its own line counts; the BEGIN and END counts must match, and every
    block must hold exactly one `## ` heading (its own generated heading). With several intact blocks,
    each is replaced."""
    nb, ne = len(BEGIN_LINE.findall(txt)), len(END_LINE.findall(txt))
    if nb == 0 and ne == 0:
        return txt.rstrip("\r\n") + eol + eol + block + eol
    blocks = BLOCK_RE.findall(txt)
    if nb != ne or len(blocks) != nb:
        return None
    if any(len(re.findall(r"(?m)^## ", b)) != 1 for b in blocks):
        return None
    return BLOCK_RE.sub(lambda m: block, txt)


def cmd_render(a):
    reg = load(REGISTRY, {"next_id": 1, "rules": {}})
    render(reg, compute(reg))
    print("render done")


def main():
    ap = argparse.ArgumentParser(description="PAROS cognitive cycle")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("due"); p.add_argument("--hook", action="store_true"); p.add_argument("--hours", type=float, default=DUE_HOURS)
    sp.add_parser("stop-hook")
    p = sp.add_parser("used"); p.add_argument("rule"); p.add_argument("--outcome", default="pending",
                                                                       choices=["helpful", "harmful", "neutral", "pending"]); p.add_argument("--note")
    p = sp.add_parser("packet"); p.add_argument("--out")
    p = sp.add_parser("apply"); p.add_argument("decisions")
    sp.add_parser("report")
    sp.add_parser("render")
    a = ap.parse_args()
    fn = {"due": cmd_due, "stop-hook": cmd_stop_hook, "used": cmd_used, "packet": cmd_packet,
          "apply": cmd_apply, "report": cmd_report, "render": cmd_render}[a.cmd]
    if a.cmd in ("due", "stop-hook"):
        try:
            fn(a)
        except Exception:
            pass  # a hook must never block the work; the health check watches the cycle
        return
    fn(a)


if __name__ == "__main__":
    main()
