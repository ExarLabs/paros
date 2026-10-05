#!/usr/bin/env python3
"""PAROS secrets inventory (P07, layers 3 and 4), kit version 0.1.0.

The canonical inventory is SECRETS.json (in the vault, it syncs): for every secret,
what it is, what it is for, who uses it, how much access it grants, when it must be
rotated, and where to revoke it. This script NEVER reads or writes a value: from the
local secrets folder it sees only file names and dates, and from the other machines
only the plain file lists of their encrypted transfer bundles, if there are any.

    python secrets_inventory.py            # status: presence per machine and differences
    python secrets_inventory.py render     # rewrite SECRETS.md (the human and agent view)
    python secrets_inventory.py check      # machine output for the health check (JSON)

Configuration (environment):
    PAROS_SECRETS_DIR        the local secrets folder (default ~/.paros/secrets)
    PAROS_SECRETS_INVENTORY  the inventory JSON (default SECRETS.json next to this script)
    PAROS_SECRETS_BUNDLES    optional folder of encrypted transfer bundles named
                             bundle-<machine>.enc.json, each with a plain "contents"
                             list of {"path": ...} and a "created" date
                             (default: keyring/ next to the inventory, if it exists)
    PAROS_HOST               this machine's name (default: the host name)
"""
import datetime as dt
import json
import os
import socket
import sys
import uuid
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
INV = Path(os.environ.get("PAROS_SECRETS_INVENTORY") or HERE / "SECRETS.json").expanduser().resolve()
VIEW = INV.with_suffix(".md")
BUNDLES = Path(os.environ.get("PAROS_SECRETS_BUNDLES") or INV.parent / "keyring").expanduser()
SECRETS = Path(os.environ.get("PAROS_SECRETS_DIR") or Path.home() / ".paros" / "secrets").expanduser()
SKIP_DIRS = {"_backup", "__pycache__", "venv", ".venv"}
# Statuses that are not checked for presence or rotation.
QUIET = {"noise", "to-retire", "config"}
TODAY = dt.date.today()


def host():
    return (os.environ.get("PAROS_HOST") or socket.gethostname()).lower().split(".")[0]


def local_files():
    """File names (relative paths) and modification dates in the local secrets folder. Never the content."""
    out = {}
    if not SECRETS.exists():
        return out
    for root, dirs, files in os.walk(SECRETS):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            p = Path(root) / f
            rel = p.relative_to(SECRETS).as_posix()
            # The machine's own key material is listed only by its private key file.
            if rel.startswith("keyring/") and rel != "keyring/private.json":
                continue
            out[rel] = dt.date.fromtimestamp(p.stat().st_mtime).isoformat()
    return out


def presence(inv):
    """{machine: {"files": set or None, "source": str}}"""
    me = host()
    pres = {me: {"files": set(local_files()), "source": "local folder, now"}}
    for m in inv.get("machines", []):
        if m == me:
            continue
        b = BUNDLES / f"bundle-{m}.enc.json"
        if b.exists():
            try:
                d = json.loads(b.read_text(encoding="utf-8"))
                pres[m] = {"files": {c["path"] for c in d.get("contents", [])},
                           "source": f"transfer bundle {str(d.get('created', ''))[:10]}"}
            except Exception:
                pres[m] = {"files": None, "source": "bundle unreadable"}
        else:
            pres[m] = {"files": None, "source": "no bundle"}
    return pres


def analyse(inv):
    pres = presence(inv)
    me = host()
    known = {s["path"]: s for s in inv["secrets"]}
    removed = {r["path"] for r in inv.get("removed", [])}
    cleanup = [f"{p} @ {m}" for m, v in pres.items() if v["files"] for p in sorted(v["files"]) if p in removed]
    unknown = sorted(p for p in pres[me]["files"] if p not in known and p not in removed)
    for m, v in pres.items():
        if m != me and v["files"]:
            unknown += [f"{p} ({m})" for p in sorted(v["files"])
                        if p not in known and p not in removed and p not in pres[me]["files"]]
    missing, overdue, soon = [], [], []
    for s in inv["secrets"]:
        if s.get("status") in QUIET:
            continue
        for m, v in pres.items():
            if v["files"] is None or s.get("no_file") or (s.get("per_machine") and m != me):
                continue
            if s["path"] not in v["files"]:
                missing.append(f"{s['path']} @ {m}")
        rb = s.get("rotate_by")
        if rb:
            d = dt.date.fromisoformat(rb)
            if d <= TODAY or s.get("status") == "rotate":
                overdue.append(f"{s['path']} ({rb})")
            elif (d - TODAY).days <= 30:
                soon.append(f"{s['path']} ({rb})")
        elif s.get("status") == "rotate":
            overdue.append(f"{s['path']} (marked)")
    noise = [s["path"] for s in inv["secrets"] if s.get("status") in ("noise", "to-retire")]
    return pres, {"unknown": unknown, "missing": missing, "overdue": overdue, "soon": soon,
                  "noise": noise, "cleanup": cleanup}


LABELS = {"unknown": "Unknown (not in the inventory)", "missing": "Missing on a machine",
          "overdue": "To rotate / overdue", "soon": "To rotate within 30 days",
          "noise": "Noise or to retire", "cleanup": "Removed, but still present on a machine"}


def cmd_status(inv):
    pres, a = analyse(inv)
    print(f"Secrets inventory: {len(inv['secrets'])} entries ({INV.name}, updated {inv.get('updated')})")
    for m, v in pres.items():
        n = "?" if v["files"] is None else len(v["files"])
        print(f"  {m}: {n} files ({v['source']})")
    for k, lab in LABELS.items():
        if a[k]:
            print(f"{lab} ({len(a[k])}):")
            for x in a[k]:
                print(f"  - {x}")


def cmd_check(inv):
    _, a = analyse(inv)
    ok = not a["unknown"] and not a["overdue"]
    parts = []
    if a["unknown"]:
        parts.append(f"{len(a['unknown'])} unknown: " + ", ".join(a["unknown"][:3]))
    if a["overdue"]:
        parts.append(f"{len(a['overdue'])} to rotate: " + ", ".join(a["overdue"][:3]))
    if a["missing"]:
        parts.append(f"{len(a['missing'])} missing on a machine")
    print(json.dumps({"ok": ok, "detail": "; ".join(parts) or "the inventory matches, no overdue secret"},
                     ensure_ascii=False))


def cmd_render(inv):
    pres, a = analyse(inv)
    machines = list(pres)
    labels = inv.get("machine_labels", {})
    short = {m: labels.get(m) or m[:8] for m in machines}
    L = ["---", "title: SECRETS", f"date: {TODAY.isoformat()}", "status: active",
         "description: \"Generated view of the secrets inventory: for every secret, without its value, what it is "
         "for, which connector or script uses it, how much access it grants, on which machine it is present, when "
         "to rotate it and where to revoke it. The canonical source is SECRETS.json; written by secrets_inventory.py.\"",
         f"id: {uuid.uuid5(uuid.NAMESPACE_URL, 'paros-secrets-view')}",
         "tags: [paros, secrets, connectors, inventory]", "---", "",
         "# Secrets inventory", "",
         f"> **Generated view, do not edit by hand.** The source is [`{INV.name}`]({INV.name}); rewrite it with "
         "`python secrets_inventory.py render`. **No secret value is here or in the JSON.** "
         "For agents: this tells you which secret serves which purpose; never read or print the secret itself, "
         "the script fetches it by name (P07).", ""]
    if any(a.values()):
        L += ["## To do", ""]
        for k, lab in (("overdue", "Rotate now"), ("unknown", "Unknown secret"), ("missing", "Missing on a machine"),
                       ("soon", "Rotate within 30 days"), ("noise", "Noise, can be cleaned up (on the owner's word)"),
                       ("cleanup", "Clean up on that machine too")):
            for x in a[k]:
                L.append(f"- **{lab}:** `{x}`")
        L.append("")
    L += ["## Secrets", "",
          "| Secret | Provider / account | Purpose | Used by | Access | " + " | ".join(short[m] for m in machines)
          + " | Rotate by | Status |",
          "|---|---|---|---|---|" + "---|" * len(machines) + "---|---|"]
    for s in sorted(inv["secrets"], key=lambda s: (s.get("status") in QUIET, s["path"])):
        cells = []
        for m in machines:
            f = pres[m]["files"]
            cells.append("n/a" if s.get("no_file") else "?" if f is None or (s.get("per_machine") and m != host())
                         else ("✓" if s["path"] in f else "·"))
        keys = f" ({', '.join(s['env_keys'])})" if s.get("env_keys") else ""
        used = "<br>".join(f"`{u}`" for u in s.get("used_by", [])[:4])
        L.append(f"| `{s['path']}`{keys} | {s.get('provider', '')}<br>{s.get('account', '')} | {s.get('purpose', '')} | "
                 f"{used} | {s.get('access', '')} | " + " | ".join(cells) + f" | {s.get('rotate_by') or ''} | {s.get('status', '')} |")
    L += ["", "## Revoke if something goes wrong", ""]
    for s in inv["secrets"]:
        if s.get("revoke") and s.get("status") not in QUIET:
            L.append(f"- `{s['path']}`: {s['revoke']}")
    L += ["", "## Machines", ""]
    for m in machines:
        n = "?" if pres[m]["files"] is None else len(pres[m]["files"])
        L.append(f"- **{m}** ({short[m]}): {n} files, source: {pres[m]['source']}")
    if inv.get("removed"):
        L += ["", "## Removed", ""]
        for r in inv["removed"]:
            L.append(f"- `{r['path']}` ({r.get('date', '')}): {r.get('reason', '')}. Where: {r.get('where', '')}")
    L += ["", "Legend: ✓ present, · missing, ? cannot be checked from here (a machine's own key is visible only "
          "locally, or there is no bundle), n/a lives only at the provider."]
    VIEW.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{VIEW} written")


def main():
    if not INV.exists():
        sys.exit(f"inventory not found: {INV} (set PAROS_SECRETS_INVENTORY, or start from SECRETS.example.json)")
    inv = json.loads(INV.read_text(encoding="utf-8"))
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    fn = {"status": cmd_status, "render": cmd_render, "check": cmd_check}.get(cmd)
    if not fn:
        sys.exit("usage: secrets_inventory.py [status|render|check]")
    fn(inv)


if __name__ == "__main__":
    main()
