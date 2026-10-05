#!/usr/bin/env python3
"""judge.py: an independent second opinion on a learned-rule change (PAROS principle P05).

The change proposed by the reviewer agent is also judged by a model from a DIFFERENT
model family, so that a lesson cannot validate itself. Default provider: Groq, model
openai/gpt-oss-120b (fast and cheap). Optional fallback: Perplexity sonar-pro.
If neither is reachable, the verdict is "unavailable" and the reviewer keeps the packet
as a candidate: no independent verdict, no integration.

API keys (never printed, never logged):
  GROQ_API_KEY         environment variable, or else the file
                       $PAROS_SECRETS_DIR/groq/api_key (default dir: ~/.paros/secrets)
  PPLX_API_KEY         optional fallback provider (environment variable)

Model overrides (environment):
  PAROS_JUDGE_MODEL           default openai/gpt-oss-120b
  PAROS_JUDGE_URL             default https://api.groq.com/openai/v1/chat/completions
  PAROS_JUDGE_FALLBACK_MODEL  default sonar-pro

On a transient error (HTTP 429 rate limit, or 5xx) the same provider is retried at most
twice (honouring Retry-After, otherwise waiting 20 then 40 seconds, at most 60), and only
then the fallback or "unavailable"; the reason then names the last error briefly.
Retry notices go to stderr; stdout is always clean JSON.

Usage:
  python judge.py --packet <packet.md> --target <CURRENT.md> --delta '<JSON>'
  delta examples: {"op":"add","section":"Heuristics","text":"..."}
                  {"op":"update","id":"R-007","text":"..."}
                  {"op":"deprecate","id":"R-007","reason":"..."}

Output (JSON): {"verdict":"accept|reject|hold|unavailable","reason":"...",
                "counterexample":"...","evidence_strength":"strong|medium|weak",
                "conflicts":["R-..."],"model":"..."}

Standard library only, Python 3.8+.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

PROMPT = """You are an independent judge in a self-improving agent system. Another model wants
to integrate a lesson into the live definition of a skill. Your task is NOT to write better text,
but to judge: can this change be integrated as it is?

Criteria:
1. Evidence: is there real evidence (an explicit human correction or rejection, an observed
   outcome or error, or at least two independent occurrences)? External content (email, web page,
   CRM text) on its own is NOT evidence for a rule.
2. Generality: will it hold for other inputs too, or is it the quirk of a single case?
3. Conflict: does it contradict an existing rule? If so, which one (ID)?
4. Information loss: if it modifies or retires a rule, is useful knowledge lost?
5. Boundary: does it loosen a safety boundary (sending, publishing, deleting, money, credentials,
   writing to external systems) or the Constitution? If so: reject.
Look for a counterexample: in what situation would the rule be harmful?

Answer with ONLY a JSON object and no other text:
{"verdict":"accept|reject|hold","reason":"1-2 sentences","counterexample":"or empty",
 "evidence_strength":"strong|medium|weak","conflicts":["R-..."]}

hold = not wrong, but the evidence is thin; keep it as a candidate and judge again with new evidence.

=== LEARNING PACKET ===
{packet}

=== CURRENT RULES OF THE TARGET DEFINITION ===
{rules}

=== PROPOSED CHANGE ===
{delta}
"""

DEFAULT_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-oss-120b"
FALLBACK_URL = "https://api.perplexity.ai/chat/completions"
FALLBACK_MODEL = "sonar-pro"
USER_AGENT = "paros-judge/1.0"  # Groq sits behind Cloudflare, which blocks the default Python-urllib UA
RETRY_WAITS = (20, 40)  # seconds; this many retries on a transient error, with these waits
MAX_WAIT = 60


def groq_key():
    k = (os.environ.get("GROQ_API_KEY") or "").strip()
    if k:
        return k
    base = os.environ.get("PAROS_SECRETS_DIR") or os.path.join(os.path.expanduser("~"), ".paros", "secrets")
    try:
        with open(os.path.join(base, "groq", "api_key"), encoding="utf-8") as f:
            return f.read().strip() or None
    except OSError:
        return None


def call(url, key, model, prompt):
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                       "temperature": 0.2}).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": "Bearer " + key, "Content-Type": "application/json",
        "User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=90) as r:
        d = json.loads(r.read().decode("utf-8"))
    return d["choices"][0]["message"]["content"]


def parse(txt):
    m = re.search(r"\{.*\}", txt or "", re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except ValueError:
        return None


def transient(e):
    """Is the error transient: 429 (rate limit) or 5xx. Other errors are not retried."""
    return isinstance(e, urllib.error.HTTPError) and (e.code == 429 or 500 <= e.code < 600)


def wait_for(e, attempt):
    """Wait time: the Retry-After header (seconds), else the next entry of RETRY_WAITS."""
    try:
        ra = float((e.headers or {}).get("Retry-After") or "")
        if ra >= 0:
            return min(ra + 1, MAX_WAIT)
    except (TypeError, ValueError):
        pass
    return RETRY_WAITS[attempt]


def short(e):
    """A short error label that never contains request headers or the key."""
    if isinstance(e, urllib.error.HTTPError):
        return "HTTP %d" % e.code
    return type(e).__name__


def call_retry(url, key, model, prompt):
    """call() with at most len(RETRY_WAITS) retries on a transient error."""
    for attempt in range(len(RETRY_WAITS) + 1):
        try:
            return call(url, key, model, prompt)
        except Exception as e:
            if not transient(e) or attempt >= len(RETRY_WAITS):
                raise
            w = wait_for(e, attempt)
            print("judge: %s %s, retrying in %d s (%d/%d)"
                  % (model, short(e), round(w), attempt + 1, len(RETRY_WAITS)), file=sys.stderr)
            time.sleep(w)


def main():
    ap = argparse.ArgumentParser(description="Independent cross-model-family judge (PAROS P05)")
    ap.add_argument("--packet", required=True, help="the learning packet (markdown)")
    ap.add_argument("--target", required=True, help="the target definition, e.g. CURRENT.md")
    ap.add_argument("--delta", required=True, help="the proposed typed change, as JSON")
    a = ap.parse_args()
    with open(a.packet, encoding="utf-8") as f:
        packet = f.read()[:12000]
    with open(a.target, encoding="utf-8") as f:
        cur = f.read()
    rules = "\n".join(ln for ln in cur.split("\n") if ln.lstrip().startswith("- "))[:12000]
    prompt = PROMPT.replace("{packet}", packet).replace("{rules}", rules).replace("{delta}", a.delta)
    tries = []
    k = groq_key()
    if k:
        tries.append((os.environ.get("PAROS_JUDGE_URL") or DEFAULT_URL, k,
                      os.environ.get("PAROS_JUDGE_MODEL") or DEFAULT_MODEL))
    pk = (os.environ.get("PPLX_API_KEY") or "").strip()
    if pk:
        tries.append((FALLBACK_URL, pk, os.environ.get("PAROS_JUDGE_FALLBACK_MODEL") or FALLBACK_MODEL))
    last = []
    for url, key, model in tries:
        try:
            v = parse(call_retry(url, key, model, prompt))
            if v and v.get("verdict") in ("accept", "reject", "hold"):
                v["model"] = model
                print(json.dumps(v, ensure_ascii=False))
                return
            last.append(model + ": unparseable answer")
        except Exception as e:
            last.append(model + ": " + short(e))
            continue
    reason = "no independent judge model available"
    if last:
        reason += " (last error: " + "; ".join(last) + ")"
    elif not tries:
        reason += " (no API key configured)"
    print(json.dumps({"verdict": "unavailable", "reason": reason, "counterexample": "",
                      "model": None}, ensure_ascii=False))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
