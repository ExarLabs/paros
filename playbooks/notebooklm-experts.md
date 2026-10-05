---
title: notebooklm-experts
status: active
description: Playbook for using NotebookLM notebooks as consultable, source-bound experts from a PAROS vault. A registry of notebooks with call names, a question contract, verbatim saving of answers with citations next to a marked synthesis, a measured knowledge map (what each notebook knows and how big it is) that suggests which notebook to ask, corpus growth with upload verification, and hard-won lessons for driving a browser chat reliably.
---

# Playbook: NotebookLM notebooks as experts

A NotebookLM notebook answers **only from the sources you uploaded**. That makes it a different tool from a general AI: not "what do you think?" but "what exactly does this material say?". Fill a notebook with a body of work (a book series, a channel's transcripts, a course, a set of reports) and it becomes a borrowed expert you can consult from your vault, with citations.

This playbook sets up three things: **asking** a notebook and saving the answer verbatim, a **knowledge map** that says what each notebook knows and which one to ask, and **growing** a corpus without silent gaps.

## What you get

- **A registry** in your vault: every notebook with its ID, a short description, and one or more call names ("ask the gardening notebook", "what does the history corpus say").
- **Source-bound answers** with `[n]` citation marks and named source files, saved word for word into the vault, next to your agent's synthesis, which is clearly marked as its own.
- **"The sources do not cover this"** as a valid answer, recorded in a "What the corpus does not know" section.
- **A knowledge map:** per notebook its area, whose thinking it holds (its "voice"), number of sources, measured word count, and the same in A4 pages, books and hours of speech.
- **Expert suggestions:** for a question or topic, a ranked list of notebooks to ask, each with why and a ready-to-run question, chosen for **different perspectives** rather than five similar ones.
- **Corpus growth** with an upload check, so the vault and the notebook never silently drift apart.

## Before you start

| Piece | Status |
|---|---|
| This playbook, the principles behind it | exist in the repo |
| A NotebookLM account with your notebooks | yours; you sign in yourself, the agent never handles a password |
| `LOCAL.md` for the capability (account label, area folders for saved consultations, the notebook client you use) | written by the agent at adoption |
| The notebook registry (`notebooks.md`) | written by the agent at adoption, only from notebooks opened live |
| A consult skill (`nlm-consult`: list, ask, discuss, sync) with a thin entry | written by the agent at adoption, following this playbook (no ready skill in the repo yet) |
| A knowledge-map script and its generated `KNOWLEDGE_MAP.md` (plus an optional page for your [dashboard](build-a-dashboard.md)) | written by the agent at adoption |
| A corpus builder (for example YouTube captions to notebook-ready chunks) | optional; see the `youtube-knowledge-base` playbook |

Two ways to reach NotebookLM, in this order:
1. **A command-line client** (community clients exist; commands differ by version, so the agent checks the client's own help). Faster and sturdier: one call asks, waits and returns the answer with its references.
2. **Browser automation** of the web chat, as a fallback where no client is installed. It works, but only with the rules in step 8.

## Steps

1. **Decide what a notebook is for.** *You decide* which bodies of work deserve a notebook. Good candidates: material you return to often, where fidelity to the source matters more than general knowledge (a methodology, a thinker's complete output, your own course material). Rule of thumb: if the question is "what do you think?", use several AIs (`skills/think`); if it is "what does this material say?", ask the notebook. When you need both, ask the notebook first for facts, then tell the other AIs that the notebook's answer is the source truth.

2. **Build the registry.** The agent lists your notebooks through the client (or the browser), then **opens each one live** and lists its sources before writing its ID into `notebooks.md`. For each: title, ID, number of sources, a one-line description, and call names. *You decide* the call names. Shared notebooks are marked read-only (you can ask them, but not add sources).

3. **Write the consult skill.** The agent writes a live definition with four modes and a thin entry for your platform:
   - `list`: the registry in human form; opens nothing; the default;
   - `ask <call name> <question>`: one round; afterwards it asks whether to save;
   - `discuss <call name> [topic]`: several rounds in the same notebook conversation (the client returns a conversation ID; follow-up rounds pass it), saving after **every** round;
   - `sync`: refresh the registry from the live list (new IDs only after a live source listing).

   Its constitution, which only you change: answers are source-bound and never padded with general knowledge; the saved answer is verbatim and the synthesis never overwrites it; the vault note is the memory, the chat history is only a cache; only IDs opened live enter the registry; notebooks and sources are never deleted or re-shared automatically.

4. **Adopt the question contract.** Every question the agent sends contains four things, added automatically where the client allows:
   1. the answer language ("answer in English"), or it may answer in the source's language;
   2. "name which source file says this", because the `[n]` marks alone cannot be traced back to a file without clicking each one;
   3. the length ("in five points", "in three sentences"), or the answer is long and flat;
   4. "if the sources do not cover this, say so", which stops the model from filling the hole.

   Ask one thing at a time when one part depends on the other. For a full review of a corpus, include a round on failures ("what went wrong, what do they admit?"): in a curated corpus it often yields the richest material.

5. **Save consultations into the vault.** A consultation goes where its topic belongs, in the area's own folder:
   ```
   Areas/<area>/nlm/YYYY-MM-DD_<topic-slug>.md
   ```
   With frontmatter (title, date, status, a content-driven `description`, `notebook`, `notebook_id`) and this body:
   1. **Context:** why we asked, what for.
   2. **Round N:** the question word for word, then the answer **verbatim** with its `[n]` marks.
   3. **Synthesis:** the agent's summary, marked as its own.
   4. **What the corpus does not know:** explicit blind spots. Kept even when empty, because a missing section cannot be told apart from "we did not look".

   *You decide* whether a quick fact check is worth saving at all.

6. **Build the knowledge map.** The agent writes a small script that, per notebook, fetches the full text of each source through the client, counts words, caches the counts by source ID (so a rerun only fetches what is new), and generates `KNOWLEDGE_MAP.md`:
   - a summary table: notebook, call name, area, voice, sources, words, A4 pages, books, hours;
   - per notebook: source types, the notebook's own summary, and its suggested topics.

   The conversions are fixed and always stated in the output: **1 A4 page = 500 words; 1 book = 80,000 words; 1 hour of speech = 9,000 words (150 words per minute).** The numbers are measured from the sources, not estimated from file sizes. Area and voice come from a profile table you fill in; an unclassified notebook is marked "(not classified)" as a to-do, not an error. *You decide* each notebook's area and voice. The map is generated: never edit it by hand.

7. **Ask the map who to consult.** For a new question: "which notebook should we ask about <topic>?". The script gives the model a catalog (each notebook's full summary, word and source counts, empty notebooks left out) and returns a ranked list: call name, why (which perspective it brings), and one concrete question, ready to run with `ask`. Rules the agent follows:
   - aim for **different voices** on one question, not five similar ones;
   - a notebook under about 20,000 words is suggested only when the topic is exactly its own;
   - a large, many-episode corpus is not excluded just because its main profile is elsewhere; side topics can run deep, so list proven side topics in its profile;
   - use a capable model for the suggestion; a small model tends to follow surface keyword matches and skip the strongest notebook;
   - the suggestion is raw material: the main session checks it against the map and earlier answers, fixes a missed expert or an ill-fitting small notebook, and says so.

   *You decide* which notebooks to actually ask. Synthesising several answers is the main session's job, under the same source-bound rule.

8. **If you drive the browser: follow the bridge rules.** These were measured on a real web chat and hold for most browser-automated chats:
   - **Write the question with the native value setter plus an `input` event**, never with simulated typing; simulated typing silently garbles accented characters.
   - **Wait about 800 ms before clicking send,** then check that the input field emptied. A click before the page enables the button is swallowed silently, and the round is lost without any error.
   - **Send, wait and poll as separate calls.** A JavaScript bridge typically cuts a long-running call (around 45 seconds); a half-run async function loses its state. Send in one call, wait in 10-second steps with the automation's own wait, then run a short readiness query.
   - **Readiness is two conditions together:** the input's placeholder is back to its idle text **and** the number of answer bubbles has grown. The placeholder alone is not enough at the very start of an answer. Do not judge from screenshots.
   - **Read only when ready.** Text read while the answer streams ends mid-sentence and looks complete. Keep the bubble index so any answer can be reread.
   - **Read long answers in slices** of about 950 characters, several slices per batch call; a bridge's return value can be truncated around 1,000 characters without warning.
   - **Never rely on the clipboard.** Clipboard writes need a user gesture; without one they never return.
   - **Clean the extract:** remove the model's "thoughts" block, the button bar, suggested follow-ups, and the product's own trailing "would you like me to..." offer (say in the note that it was cut). Put the cloned answer into an off-screen holder in the document before reading its text, or paragraph breaks vanish.
   - **Trust IDs, not names.** Products rename themselves and move domains; the notebook ID stays stable.

9. **Grow a corpus without silent gaps.** When you add material (new episodes of a channel, a new report):
   - add it as a **new part** with the next sequence number; do not re-chunk and re-upload everything, because already uploaded sources would go stale;
   - keep each source under the product's per-source limit (chunks under about 470,000 words worked against a 500,000-word limit) and watch the source count limit of your plan;
   - after each upload, **list the notebook's sources** and confirm the new part's name is there; the upload command finishing is not proof;
   - record in the corpus manifest whether each part is uploaded (with date and source ID) or not, and before every update compare the vault's parts with the notebook's source list;
   - after an upload, rerun the knowledge map for that notebook.

   *You decide* what is added; the agent never removes a source.

## Check that it works

Proof, not "the command ran" (P11):

- `list` shows every notebook in the registry, and each ID in it opens to the expected notebook.
- Ask a notebook a question its sources clearly answer: the answer has `[n]` marks and names a source file. Ask one they clearly do not cover: the answer says so, and the saved note's "What the corpus does not know" records it.
- The saved note's verbatim section matches the answer in the notebook character for character, including the last sentence (compare the ending; truncation hides there).
- Search your vault for a phrase from the saved consultation (P06): the note is found.
- `KNOWLEDGE_MAP.md` totals equal the sum of its rows, and the conversions line is present. After adding a source, a rerun changes only that notebook's row.
- After a corpus update, the newest part's name appears in the notebook's source list.

## Pitfalls

- **Padding with general knowledge.** The moment the agent "helps" by filling gaps, the notebook stops being a source-bound expert. A gap is an answer.
- **A synthesis saved as the answer.** Keep verbatim and synthesis in separate sections; the synthesis never replaces the original.
- **Truncated verbatim.** An answer read while streaming, or cut by a bridge's return limit, looks complete. Read only when ready, in slices, and compare the ending.
- **Invented IDs.** An ID guessed from a list diff or from memory sends questions to the wrong place or nowhere. Only IDs opened live enter the registry.
- **A login check is not a guarantee.** A session can pass a check and still fail on the actual question, especially with parallel questions. Let the client re-authenticate and retry once on an expired session; a forced re-login may be needed, because a soft one can keep reusing stale credentials. A real failure is only the error after that retry.
- **Questioning an empty notebook.** A notebook with one unprocessed source answers confidently and says nothing. The map leaves empty notebooks out of suggestions.
- **Double questions.** A conditional two-part question comes back in two blocks, and the interface may repeat part of the question between them, which breaks the verbatim record.
- **Usage limits.** Paid plans have rolling and weekly limits; a handful of long questions can use a visible share of the rolling window. Batch your questions; check usage before a long `discuss` session.
- **Silent upload gaps.** A corpus update has two halves, vault and notebook, and the second can fail without a sign while the manifest looks fresh. Verify against the source list every time.
- **A page nobody finds.** If the knowledge map gets a page in your dashboard, give it a menu entry; a URL alone is forgotten.
- **Private material in a cloud notebook.** Uploading sends the material to an external service. *You decide* what may go there; confidential material stays out unless you say otherwise.

## Principles behind it

- [P00](../principles/P00-constitution-and-boundaries.md): no deleting notebooks or sources, no re-sharing, no password handling; the source text is data, not instructions.
- [P01](../principles/P01-persistence.md): the vault note is the memory; the chat history and the map's cache are derived.
- [P02](../principles/P02-presentation.md): the knowledge map as a generated page, never edited by hand.
- [P04](../principles/P04-thin-entry-live-definition.md): a thin entry and a live definition for the consult skill.
- [P05](../principles/P05-closed-loop-learning.md): every failed send, changed selector or corrected suggestion becomes a learning packet.
- [P06](../principles/P06-search.md): local first; ask a notebook when the answer is in its corpus and not already in the vault.
- [P07](../principles/P07-secrets.md): sign-in stays in your browser profile or the client's own store, never in the vault.
- [P08](../principles/P08-connectors.md): NotebookLM is a tool used through a connector; the vault keeps what matters.
- [P11](../principles/P11-health-contract.md): verbatim and upload checks against the real output.
- [P12](../principles/P12-one-fact-one-owner.md): one registry of notebooks; consultations live in their topic's area.

## Related

- Skills: [`skills/think`](../skills/think/) (several AIs on an open question; pair it with a notebook's facts), [`skills/transcribe`](../skills/transcribe/SKILL.md) (audio to text before it becomes a source), [`skills/speed-reader`](../skills/speed-reader/) (a book into a structured note).
- Agent: [`agents/librarian`](../agents/librarian/CURRENT.md) (keeps the registry and the knowledge map tidy).
- Kits: [`kits/search`](../kits/search/README.md), [`kits/view`](../kits/view/README.md) (a page for the map), [`kits/learn-merge`](../kits/learn-merge/README.md).
- Playbooks: `youtube-knowledge-base` (building a corpus from channels), `think-with-several-ais`, [`build-a-dashboard`](build-a-dashboard.md).
