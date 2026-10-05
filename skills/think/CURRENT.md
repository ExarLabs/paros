---
title: think
date: 2026-10-05
status: active
description: Multi-AI thinking with one orchestrator agent: assembles a team of external AIs with roles (researcher, strategist, validator), sends each one fat prompt with a strict findings contract, runs them in parallel over API or browser, merges the answers at field level, and keeps everything in one brainstorm state file that is the canonical memory.
version: 1.1.0
upstream:
  # filled in when adopted into a vault
---

# think

Some questions deserve more than one mind: market research, a strategy choice, a hard trade-off, a plan you want someone to attack before you commit. This skill turns your agent into an **orchestrator**: it assembles a small team of other AIs, gives each a role, asks them everything at once, merges their answers, and writes the result into one file you keep.

> **The brainstorm state file is the durable brain. The AIs are interchangeable thinking surfaces.**

## Constitution

Only the owner changes this section. The learning machinery never touches it.

- **The state file is the canonical memory.** A conversation's memory inside an AI's own interface is a cache, not the truth.
- **The drift rule.** After every browser round, the findings are synced back into the state file. Browser-side memory that is not synced back is a hidden parallel knowledge base that no other AI, and no future session, can see.
- **Source trust order:** the person > local files > the AI team > the orchestrator's own inference. When sources disagree, the higher one wins, and the conflict is shown, never silently resolved.
- **A browser identifier enters the registry only after a successful select.** Never infer an identifier from a list, a position, a name or a difference between two lists.
- **When a browser-AI thread carries real strategic value, the full verbatim transcript is archived** next to the synthesis. The state file stores parsed findings, not prose; the two do not replace each other.
- **The person decides.** The team, blocking questions and anything irreversible are theirs. The orchestrator never sends, publishes, pays or signs in on their behalf (P00).
- **Personal values live in `LOCAL.md`, never here.** This file is the recipe; `LOCAL.md` is the spice.

## Recipe and spice: CURRENT.md and LOCAL.md

This file is the general procedure and is the same for everyone. Everything personal lives in **`LOCAL.md`**, next to this file in your vault:

- which AIs you have, with which accounts and which transport;
- your preferred team and presets;
- the browser registry: which browser works on which of your machines;
- where your API keys are expected (names of environment variables only, never values).

Start it by copying [`LOCAL.example.md`](LOCAL.example.md) to `LOCAL.md` and filling it in with the person. **Read `LOCAL.md` at the start of every session.** If it does not exist, offer to create it, and until then ask for what is missing. Wherever this file says "from `LOCAL.md`", that is the only place the value may come from.

`LOCAL.md` holds identifiers and preferences, never secrets (P07). If the vault is shared or published, keep `LOCAL.md` out of it.

## When to use

- "Think this through with several AIs", "brainstorm", "research this from several angles", "get a second and third opinion", "attack this plan".
- A decision where being wrong is expensive and one model's view is not enough.
- Reading out an existing AI conversation (a link to a chat thread) to bring it into the vault.

Do not use it for a question one model answers well; a team round costs time and money.

## Roles

- **The person: decision authority and team architect.** Sets the goal, gives real-world context, confirms the team, decides blocking questions, validates the outcome. Not required to micromanage.
- **The AI team: roles assigned per session.** Common archetypes:
  - **Researcher:** sourced facts, primary and recent sources preferred.
  - **Strategist:** options, trade-offs, models, the highest-leverage first move.
  - **Validator:** devil's advocate; the strongest argument against, what is missing, when it fails.
  - Optional: **Domain expert** (technical depth, risks, best practice), **Creative** (alternatives nobody asked for).
- **You, the agent: orchestrator and executor.** Assemble, prompt, collect, synthesize, persist. If you discover something that threatens the strategy, say so at once.

## Principles

1. **Local first.** Read the relevant files in the vault before asking any outside AI. Often the answer, or half of it, is already there.
2. **Persistent cognition.** Every important insight, decision and open question goes into the state file.
3. **Throughput discipline.** One fat prompt per member, a structured response, all members in parallel. Every round trip costs seconds; never spend them one question at a time.
4. **Transport pragmatism.** API by default; a browser only when it adds something an API cannot.
5. **Open team.** Any AI the person can reach can join at session start.

## Steps

### 0. Session start

1. Read `LOCAL.md`.
2. If this session may need a browser, run the **browser lookup** now, not at the moment the browser is first needed (see "Browser choice"). A rule that only lives where it is relevant gets skipped.
3. Read local context: the area's state file, the existing brainstorm file on this topic if any, and the files it links.

### 1. Assemble the team

Propose a team from the task and from the person's preferred team in `LOCAL.md`, one line per member with role and transport:

```
Thinking team for this session:
1. <AI A>   Strategist  · API
2. <AI B>   Validator   · API
3. <AI C>   Researcher  · browser (needs account-side sources)

Change anyone? Swap a model or transport, add or remove a member, or pick a preset.
```

Presets are defined in `LOCAL.md`. Useful shapes: **Premium** (strongest model per role), **Fast** (cheaper models), **Solo** (one provider, the validator played by a second call with a devil's advocate prompt), **Browser only** (no API keys at all).

Lock the confirmed team into the state file's Team table. Then check that every API member's key is present in the environment variable named in `LOCAL.md`. If one is missing, offer a short guided setup (the person creates the key in the provider's console and sets it in **their own** terminal or secret store; it is never pasted into the chat). If declined, move that member to the browser and note it in the state file.

A present key does not prove a usable key: the account behind it can be out of credit. If a round is expensive, you may send each API member a tiny ping first (a few output tokens, "Say PONG") before the fat prompt goes out; a member that fails the ping is moved to the browser right away, as in "Failure modes".

### 2. Decide the transport

**Default: API.** It is faster, structured and reliable. Use a browser only when it adds one of these four things:

| # | Browser-only value | Examples |
|---|---|---|
| 1 | Voice | A spoken conversation the person had with an AI |
| 2 | Account-side data | Custom assistants, projects, saved memories, workspace documents the account can see |
| 3 | No API | An AI that is only reachable through its web interface |
| 4 | Live human interaction | A conversation the person is having right now that you need to read |

If none applies, use the API. API calls are stateless, so the state file supplies the context in the prompt.

### 3. Write fat prompts

One prompt per member, with **all sub-questions numbered in one message** and the response contract appended. Shapes per role:

- **Researcher:** CONTEXT (2 to 4 lines) + Q1..Qn; sources required; prefer primary and recent.
- **Strategist:** CONTEXT + CONSTRAINTS + "propose 2 or 3 approaches with trade-offs; the highest-leverage first move; which assumption breaks the plan".
- **Domain expert:** CONTEXT + DOMAIN + technical questions + risks and best practice + tooling.
- **Validator:** PROPOSAL UNDER REVIEW + REASONING + SOURCES + "the strongest argument against; what are we missing; when does this fail".

### 4. The response contract

Every prompt to every external AI ends with this block:

````
---
RESPONSE FORMAT (REQUIRED):
Wrap your full answer in a single fenced code block tagged `findings`:

```findings
{
  "summary": "1 to 3 sentence headline answer",
  "answers": [
    {"q_id": "Q1", "answer": "...", "confidence": "high|medium|low", "sources": ["..."]}
  ],
  "open_questions": ["..."],
  "flags": ["contradictions, gaps, warnings"]
}
```

After the block, write exactly this token on its own line:
END_OF_RESPONSE
---
````

Why: one pattern extracts the JSON, synthesis becomes a merge of fields, and a missing block means an incomplete answer. For API calls the completed HTTP response is the done signal; in a browser, the `END_OF_RESPONSE` token appearing on the page is a reliable one.

**Parse leniently, in this order:**

1. A fenced block tagged `findings` or `json`.
2. No usable fence: decode JSON from the first `{` in the response (in Python, `json.JSONDecoder().raw_decode()`). Web interfaces often re-label or strip a code fence when they render it, so the fence is gone while the JSON underneath is perfect. If the decoder consumes the whole object and nothing meaningful remains, the payload is provably whole: **this is not a contract violation.** Do not re-prompt and do not lower confidence.
3. Accept both shapes: the canonical `{summary, answers: [...]}` and a flat `{"Q1": "...", "Q2": "..."}` that some models emit. Normalize the flat one into `answers` and add a flag: "normalized from flat shape".

Only when all three fail is it a real violation: mark the member's input low confidence, log it, and re-prompt once with "Please re-format using the required findings block." Re-prompting an answer that was actually intact costs a full round trip and teaches nothing.

### 5. Activate in parallel

N members means N calls **in one turn**. The round takes as long as the slowest member, not the sum. Run rounds one after another only when one member's output is genuinely needed to write another's prompt (for example, the validator attacking the strategist's proposal).

**Build every API payload from a file, never inline.** Write the prompt to a file, then build the JSON body with `jq`:

```bash
printf '%s' "$PROMPT" > "$WORK/prompt.txt"
jq -n --rawfile p "$WORK/prompt.txt" \
  '{model:"<model>", messages:[{role:"user", content:$p}]}' > "$WORK/payload.json"
curl -s "<provider endpoint>" -H "<auth header from the env variable>" \
  -H "Content-Type: application/json" \
  --data-binary "@$WORK/payload.json" -o "$WORK/resp.json"
jq -r '<path to the text>' "$WORK/resp.json"
```

Why: inline JSON breaks on quotes and newlines, and a helper script that cannot find its path can silently write no file, so `curl` sends an **empty body** and the provider answers with a confusing "field required" or "could not parse" error. `jq --rawfile` is platform independent and removes escaping entirely. Always write the HTTP response to a file before parsing it.

**Reasoning models** spend their output budget on internal reasoning first. A small budget returns an empty answer with `finish_reason: "length"` and reasoning tokens equal to completion tokens: that is the signature of a budget that was too small. Start generous and check the finish reason before parsing.

### 6. Synthesize at field level

1. Parse every member's findings.
2. Merge per question (`q_id`): where members agree, state it once with all sources; where they differ, show each position with its source and role.
3. Weigh by the source trust order. A local file beats an AI claim; the person beats both.
4. Read the `flags` of every member, not only the `confidence`. A confident answer built on a stale secondary source looks perfect and is wrong; the flags are where members warn about it. On topics where secondary sources age fast (law, regulation, prices), go back to a primary source yourself.
5. Write the synthesis: headline, per-question merged answer, contradictions with sources, open questions, recommended next step.

### 7. Persist

Write into the state file: each member's raw findings JSON verbatim, the synthesis, new insights, decisions (with who decided), open questions, and the conversation link for every browser member. For a browser round, this is the drift rule in action: the round is not finished until it is synced.

### 8. Confidence and escalation

- **High:** proceed. **Medium:** proceed and log the assumption visibly. **Low:** ask.
- **Blocking ambiguity** (architecture, pricing or business rules, core user flows, destructive or irreversible actions, legal or security questions, a contradiction with the stated strategy): stop and ask. Batch **all** blocking questions into one structured question with suggested answers, and keep working on what is not blocked meanwhile.
- **Non-blocking** (naming, wording, equivalent tool choices): proceed with an assumption log.
- Log every significant decision inline: what, informed by which source (AI and role), with what confidence.
- When AIs contradict each other or the local files, flag it with every source cited. Never silently pick one.

## The brainstorm state file

One file per topic: `<area folder>/brainstorm/brainstorm_<topic-slug>.md`, from [`templates/brainstorm-state.md`](templates/brainstorm-state.md). Create it on first use, update it after every round, never delete it (set `status: concluded`), and link project files rather than copying them (P12).

## Browser choice

If your setup drives browsers through a tool that lists connected browsers and selects one by identifier, the person should **never have to pick a browser twice on the same machine.** The registry in `LOCAL.md` records, per machine, the last browser that worked.

1. **Look up** the machine (by its hostname) in the registry, at session start.
2. **Hit marked verified:** select that browser by its stored identifier and say in one line which one you attached to. Do not ask.
3. **Miss, or the select fails** (the browser disconnected, the identifier is stale): list the connected browsers. If exactly one local candidate exists, try it; if the target page works, it is the new last successful browser.
4. **Ask the person only when it is ambiguous:** several equal candidates, or none works. One question.
5. **Verify before you write.** Only an identifier that a select call has just accepted goes into the registry, marked verified, with the date. Then update its last-used date.

What the registry learned the hard way:

- **Never infer an identifier from list differences.** A browser that vanished from the list between two calls has usually just disconnected, not become "the active, hidden one". Selecting an inferred identifier fails.
- **Display names are positional.** Labels such as "Browser 1, 2, 3" renumber as the list changes, and may ignore the name the person gave the browser. The identifier is the only stable key.
- **Browsers drop between calls.** A stale saved identifier is the normal reason a select fails; rediscover, do not guess.
- **An automation profile and the person's own browser are different worlds.** A dedicated automation browser profile is usually not signed in to the person's AI accounts. Check that the profile actually has a session before relying on it, or the run silently lands on a login page.

## Reading a conversation and archiving it

To bring an existing AI conversation into the vault (a voice session, a thread the person built by hand), read it out through the provider's own conversation data where possible, and fall back to asking the AI for a summary in the findings format. Put the summary into the state file.

When the thread has **strategic value**, also archive the **full verbatim transcript** as its own file, linked from the state file:

- regenerate it in full from the source each time (idempotent), never append slice by slice; appending is where seam corruption (words split across slices) comes from;
- it is machine generated, so never hand-edit it; commentary goes in a separate note that links to it;
- when the data must pass through a size-limited channel, move **the conversation JSON**, not rendered prose, and check at the end that it parses and that the **character count matches** the source. Some page-text readers collapse runs of whitespace even inside preformatted blocks; for whitespace-sensitive payloads, transfer an encoded form (base64) and decode locally.

## Browser rounds: practical rules

- **Never put the waiting inside a page script.** Browser bridges time out long scripts and lose their state silently. A browser round is three separate calls: write and submit; wait in short slices; one short readiness check.
- **Verify the submit happened.** A send button clicked in the same instant as the text was inserted can be swallowed by the page framework. Wait a moment, click, then check that the composer cleared.
- **Never read a reply that is still streaming.** A mid-stream read ends mid-sentence and looks like a complete answer. Read only after a done signal (the `END_OF_RESPONSE` token, or the page's own completion signal).
- **Insert long or multi-line text in one operation** (an insert-text call, or for a framework-controlled text area the native value setter followed by an `input` event). Simulated typing is slow, can send the message at the first newline, and can mangle accented characters.
- **If a round times out but the answer is on the page, read it before resending.** Never re-submit blindly.
- **Bring a long prompt in through a file, not through the tool call.** Typing or pasting 10 KB or more through a browser tool is slow and fragile, and fetching it from a local server usually fails because the AI site's content security policy blocks requests to other origins, inward as well as outward. A path that works: add a temporary file input element to the page, upload the prompt file (which is saved next to the state file anyway) into it with the browser tool's file upload, read it with `file.text()` into a page variable, insert it into the composer in one operation, then remove the input. Check the character count in the composer against the file.
- **Confirm the send by the page, not by the button.** When the send button cannot be found reliably, the proof that the message went out is that the composer is empty and the page address now carries a conversation identifier.
- **Deep reasoning modes take long.** Some providers' deepest modes can think for more than ten minutes; a fixed timeout of a few minutes cuts them off. Give such a member a long wait budget, keep waiting in short slices, and do not mark it failed while it is still working.
- **A bridge filter can swallow a return value.** Some browser bridges block a script's return value when it looks like cookie or query-string data (many `key="value"` pairs, for example). If a read comes back blocked, use another read path (the provider's own conversation data rendered into the page, then a page-text read) instead of retrying the same script.

## Failure modes

| Failure | Detection | Recovery |
|---|---|---|
| API key missing | check at team assembly | guided setup by the person; else move the member to the browser |
| API credit exhausted | the provider says there is no credit, insufficient quota or a billing problem, sometimes under HTTP 429 | not transient: no backoff and no retry; move the member to the browser for the rest of the session, note it in the state file, tell the person in one line that the API credit needs topping up |
| Rate limit (HTTP 429) | status code, with no credit or quota message | back off 2, 4, 8 seconds, at most three times, then escalate |
| API timeout | no answer in about 60 seconds | retry once, then use the browser for this round |
| Empty answer from a reasoning model | reasoning tokens equal completion tokens | raise the output budget and retry |
| Empty request body | provider says a field is required or the body cannot be parsed | rebuild the payload with `jq --rawfile` from a file |
| Contract violation | all three parser branches fail | re-prompt once for the format; low confidence |
| Browser not signed in | lands on a login page | the person signs in, in that browser; never enter credentials for them |
| Browser select fails | error on select | rediscover per "Browser choice" |
| Deep reasoning mode silent for minutes | no done signal yet, but the page shows it is still thinking | keep waiting in short slices within a long budget; do not resend |
| Return value blocked by the bridge | the read returns a blocked or filtered marker | switch to another read path; do not repeat the same script |

## Output

- The brainstorm state file, created or updated, with each member's raw findings and the synthesis.
- A short answer to the person: the headline, where the team agreed, where it disagreed, open questions, and the blocking questions (if any) in one batch.
- When a browser thread had strategic value: the verbatim transcript file, linked from the state file.

## Pitfalls

- Never leave a browser round unsynced: a finding that lives only in an AI's own interface is lost to every other member and to the next session. <!-- rule:R-001 since:2026-07-28 -->
- Never write personal values (accounts, machines, identifiers, team choices) into this file; they belong in `LOCAL.md`. <!-- rule:R-002 since:2026-10-05 -->
- Do not ask members one question at a time; one fat prompt per member, all members in one turn. <!-- rule:R-003 since:2026-07-28 -->
- Do not re-prompt an answer whose JSON decodes whole just because its fence is missing. <!-- rule:R-004 since:2026-08-11 -->
- Never build an API payload with inline JSON or a fragile helper; build it from a file with `jq --rawfile`. <!-- rule:R-005 since:2026-08-24 -->
- Do not trust confidence alone; read the flags, and check primary sources on fast-ageing topics. <!-- rule:R-006 since:2026-08-24 -->
- Run the browser lookup at session start, and ask the person to choose a browser only when the choice is genuinely ambiguous. <!-- rule:R-007 since:2026-08-12 -->
- Never record a browser identifier you have not just selected successfully. <!-- rule:R-008 since:2026-08-03 -->
- When a transfer goes through a size-limited channel, verify by parse and character count. <!-- rule:R-009 since:2026-08-03 -->
- When the person corrects the team, the synthesis or a transport choice, record it as a learning packet in this skill's `observations/` folder (P05). <!-- rule:R-010 since:2026-08-07 -->
- An exhausted API credit is not a transient error: do not back off and retry; switch that member to the browser for the session, record it in the state file, and tell the person in one line. A key that is present is not proof that it works. <!-- rule:R-011 since:2026-10-05 -->
- Bring long prompts into a browser composer from a file (a temporary file input, then one insert), not by typing or by fetching from a local server, and check the character count afterwards. <!-- rule:R-012 since:2026-10-05 -->
- Do not apply a short fixed timeout to deep reasoning modes; they can run for more than ten minutes. <!-- rule:R-013 since:2026-08-24 -->
- When a browser bridge blocks a return value as cookie or query-string data, change the read path instead of retrying. <!-- rule:R-014 since:2026-09-23 -->
