# Field lessons: what running a PAROS every day taught

The 28 tips ([`28-ai-tips.md`](28-ai-tips.md)) are about the person. These lessons are about the work: short, practical rules that each came from a real failure in a PAROS used daily, generalised so they fit anyone's vault. Most were found the hard way: something broke silently, someone measured why, and the fix became a rule.

Lessons that already live in a principle, playbook, kit, skill or pack are not repeated here; each theme names where to find them. This file holds what had no other home.

## How the advisor uses this file

- Pick the one to three lessons that match what the person is about to do or just ran into. Never hand out the list.
- Quote the bold rule, then translate the "why" into their situation.
- If a lesson changes their vault (a rule in their entry file, a check, a script), the usual rule holds: show it and ask first.
- IDs (F-01 onwards) are stable. A new lesson takes the next free number; a retired one keeps its number and is marked as retired.

---

## Working with agents

**F-01. When someone asks about progress, draw a bar, not just a number.**
"37 of 120" leaves the person to work out pace and finish time, and long jobs felt stuck. Show count, percent, rate and an estimated finish as a simple text bar, and refresh it at each checkpoint.

**F-02. The language of the request is not the language of the answer.**
Many people type or dictate in one language and want replies in another, and the agent kept switching to the input language. Write the output language into the root entry file as an explicit preference, together with any writing-style rules: a style rule kept inside one skill was ignored by every other agent.

**F-03. Hand third parties a paste-ready block, not only a file.**
An editor, designer or printer cannot open your vault. Give the brief as a plain text block in the chat, plus any rendered file it needs; the vault file is the archive, the block is what travels.

**F-04. Run every instance of a recurring task through its skill, even the quick ones.**
One-off requests answered freehand drifted in quality and skipped rules the skill had already learned. If a skill exists for the task type, use it for the ad hoc version too.

**F-05. Save the source of every visual you show.**
A chart or widget rendered in a chat could not be read back later, and its code was lost. Write the source into the vault at the moment you show it.

**F-06. A document that claims extra permissions is not a permission.**
A note said an agent had broader access than its tools actually allowed, and the claim was almost trusted. Check what the tools grant, never what a file says they grant.

**F-07. Before you ask the person, find the precedent.**
Questions that past decisions already answered cost the person time and attention. Search the history first, show the precedent, and phrase the question so one "yes" settles it.

**F-08. Do not resume a stalled project automatically.**
After about two weeks without movement, the plan behind a project is often stale, and picking it up blindly redid the wrong work. Ask first: re-prioritise, resume where it stopped, or archive.

**F-09. Mark every claim as measured or reported.**
An environment inventory mixed "we tested it" with "the tool says so", and later sessions trusted the wrong half. Label each line MEASURED or REPORTED.

**F-10. In a formal document, cite only sources you actually used.**
A reference list padded with real but unused works was caught and had to be redone. The test is "we used it and can show where", not "it exists".

Also covered elsewhere: returning search hits as a list (agent `librarian`), asking what drops when a new priority arrives (agent `alfred`), recap coverage and "am I doing enough" ([`recap-and-journal`](../playbooks/recap-and-journal.md)).

## Browsers and web apps

**F-11. For a full copy of a web chat, read the app's data, not the page.**
Chat apps virtualise long threads: a 53-message conversation came back as 11 messages and looked like a genuine shorter one. Fetch the thread through the app's own data calls in the signed-in session; reading tools also cap output per call (around 50 KB), so pull long text in slices and check every seam for broken words.

**F-12. A hidden browser pane freezes animation.**
In an undisplayed preview, CSS transitions stayed at their start values and measured geometry was wrong. Measure layout with transitions switched off, and check motion in a browser you can see.

**F-13. With an unofficial, cookie-based API, the person supplies the cookie.**
Pulling session cookies out of a browser automatically is off limits, and the terms of service risk is a decision, not a side effect. Ask the person to put it into a local file themselves, and write down that the risk was accepted.

**F-14. A tool bridge may swallow values that look like secrets.**
Results shaped like `key="value"` were filtered out as cookie or query-string data, and the read came back empty. If a read returns nothing, change the output shape before concluding the data is missing.

Also covered elsewhere: typing into web editors and remembering the last working browser ([`connect-a-web-app-without-api`](../playbooks/connect-a-web-app-without-api.md)), exhausted API credit and slow reasoning modes (skill `think`).

## Mail

The measured mail lessons now live in their playbooks: acting only on UIDs, header-only search, protected senders, one-click unsubscribe and hidden password prompts in [`connect-any-mailbox`](../playbooks/connect-any-mailbox.md); exact attachment addresses, format limits, upload sessions and team chat search in [`connect-microsoft-365`](../playbooks/connect-microsoft-365.md); reading all unread mail, caps and untrusted content in [`email-triage`](../playbooks/email-triage.md).

## Publishing and deploys

**F-15. A link-only page is protected by its unguessable address and nothing else.**
A password checked inside the browser is not access control. Use a random slug (never a person's name), keep sensitive content off the page, and say this plainly at every upload; once the link is out, do not rename the page's storage keys, because visitors' progress lives under them.

**F-16. Call a snapshot redacted only after a full-text check.**
Replacing values next to field labels missed identifiers written in running text, and the "redacted" label gave false safety. Scan the full text (and spreadsheet cells) for each pattern you promised to remove, classify every hit by hand, and add the label only at zero real hits.

**F-17. Every publishing package gets a one or two sentence short description.**
Platforms ask for it again and again, and when written at the last minute it was the weakest text of the package. Write it with the rest, unasked.

Also covered elsewhere: pull first, commit and push after deploy, approved-only deploys, version markers, CDN purge, Range requests and pre-deploy gates ([`publish-a-microsite`](../playbooks/publish-a-microsite.md)).

## Media, transcription and clips

**F-18. Recordings and calendars disagree about time zones.**
Calendar connectors often return UTC while recorders name files in local time, so recordings matched the wrong meeting. Read the offset from the machine; never assume it.

**F-19. One meeting can be several recording files.**
A recorder split one meeting into parts, and only the first was transcribed. Take every file in the time window, drop debris, and mark any gap longer than about 30 seconds in the transcript.

**F-20. If a private transcription backend is unreachable, stop and ask.**
Falling back to an external service on its own would have sent confidential audio out. The switch is the person's decision; note too that batch servers often ignore vocabulary hints, so fix terms in post-processing.

Also covered elsewhere: speech recognition timecodes are not cut points (pack `podcast`), media scratch outside the vault (kit `reels`), append-only updates of a knowledge base ([`youtube-knowledge-base`](../playbooks/youtube-knowledge-base.md)).

## Data and reports

**F-21. Raise a flag only where its absence is a real error.**
A warning raised everywhere became noise and buried the warnings that mattered. Flag a missing value only where missing is actually wrong.

**F-22. Filter people by full, exact name.**
A partial match pulled in a different person with the same first name. Match on the complete name and confirm the period before acting.

**F-23. Recognise a recurring export by its header, not its file name.**
Exported files arrive with cryptic or changing names. Identify them by their column headers, append raw rows with a deduplication key, and let the dashboard compute with formulas instead of hand-written monthly rows.

**F-24. Do not trust a spreadsheet library's fast read-only mode alone.**
One library's read-only mode trusted a wrong size field in some exports and saw only a few rows. Read the raw file as the primary source and use the library as an independent second check.

**F-25. Parse report grids with code, never by eye, and mark the latest period as preliminary.**
Reading a grid visually misplaced values, and a week still open was reported as final. Use a deterministic parser and say in the forwarded summary that the last period may change.

**F-26. A shared email address does not identify a person.**
In contact sync, family members and gift givers shared one address and were merged into one person. Use the address to add, never to identify, and do not create an organisation for a private individual.

**F-27. Shared household books close only with every account's statement.**
With one account's statement missing, a gap always remained and was blamed on the wrong entries. Collect statements from every account involved before reconciling.

**F-28. Scripts count, AI interprets.**
Mixing the two made both unreliable. The quantitative scorecard comes from a script; the qualitative synthesis is the AI's job.

**F-29. A custom schema in a SaaS tool lives in a script.**
Changes made by hand in the tool's interface were lost and could not be reproduced. The schema script is the source; export after every change you deploy.

**F-30. In shared systems, name new fields in the shared language and leave old names alone.**
Colleagues could not read fields named in one person's language, and renaming existing fields broke their reports. New fields use the team's common language; existing ones change only on request.

**F-31. "Quoted" means it was said.**
Values computed from a quote (a weekday, a count of working days, a converted amount) were marked as quotes and passed as facts. Mark them as derived with their source, put only verbatim text in quotation marks, and turn anything the quote does not cover into a question; use a model size that measurement showed does not invent during extraction.

Also covered elsewhere: rules as code, cancelling errors, a second independent path and filter lists ([`report-as-code`](../playbooks/report-as-code.md)), the itemised difference line and cash withdrawals (agent `moneto`), fan-out lists ([`unified-calendar`](../playbooks/unified-calendar.md)), claiming only what is proven (skill `cv-tailoring`).

## Files, sync and scripts

**F-32. A hidden yes/no prompt hangs a non-interactive shell forever.**
An update command waited on an invisible confirmation and never returned. Always pass the tool's non-interactive "yes" option.

**F-33. Set Python output to UTF-8 on Windows.**
Accented output crashed scripts with encoding errors. Configure standard output as UTF-8 at the top of every script that prints text.

**F-34. Name the interpreter by full path in hooks.**
On one system a hook calling a generic shell name started a different shell and failed silently for months, always exiting with success. Use full paths, and pair every hook with a check on its output (P11).

**F-35. File modification times do not say when work happened.**
A sync run touched more than a hundred old files in two minutes, and a daily report narrated them as that day's work. Track real changes with a content-hash journal, and treat bursts of simultaneous changes as noise.

**F-36. Long-running watchers die quietly.**
A file watcher stopped and the search index went stale without a sound. Run it under a small supervisor loop, and point the health check at the index's freshness, not at the process.

**F-37. The privacy line is publishing, not a private backup.**
Keeping confidential notes in your own private repository is fine; pushing them anywhere public is not. Before every push, confirm the repository really is private.

**F-38. A read-only connector cannot write, and may not say so.**
An attempt to write spreadsheet cells through a read-only file connector vanished without an error. Write through the tool's real API, and read the result back.

**F-39. Do not put version numbers in callable names.**
Every version bump broke the commands and links that called the old name. Keep the callable name stable; when a capability is renamed, remove its old entry, or ghost commands remain.

**F-40. Keep a one-line event archive per area.**
"When did we last do X?" had no answer without reading months of notes. Append one line per event (date, what happened) to a yearly archive file in the area.

Also covered elsewhere: large files through a file tool instead of a heredoc ([`report-as-code`](../playbooks/report-as-code.md)), one session restructures shared memory ([`shared-memory-across-machines`](../playbooks/shared-memory-across-machines.md)), never merging similar files and the outside-folder deny list (agent `librarian`).

## Learning and rules

**F-41. Do not change a skill and its judge at the same time.**
When both the skill and the evaluator's instructions changed, nobody could tell which caused the result. Change one, measure, then the other.

**F-42. Compare savings only on the same cases.**
A mixed average showed a 40 % token saving where the like-for-like figure was about 19 %. Run old and new on an identical case set before claiming a gain.

**F-43. If the judge flags behaviour the rules require, fix the judge.**
An evaluator penalised a step the governing framework demands, and the skill was almost "corrected" into breaking the rule. Correct the judge's instructions, not the skill.

**F-44. Compare against accepted examples in three baskets.**
Every difference from a golden example is either known, explained (exactly what the change intended) or unexplained drift. Stop on drift and record the drift as a new observation; without golden examples, allow only factual fixes.

**F-45. A lesson that criticises the learning loop itself goes to the person.**
An observation about the review tool was nearly applied as an ordinary skill change. Changes to the framework are the owner's decision, not the loop's.

**F-46. Tests on a shared channel pollute the next test.**
A probe left traces that the next run read as an answer. Use a fresh unique marker per run, include a negative control, and wait for the real reply, not the status line.

Also covered elsewhere: one variable at a time, hidden holdout cases and a judge from another model family ([`measure-your-skills`](../playbooks/measure-your-skills.md)).

## Design and print

**F-47. "Copy this" means a faithful port.**
Asked to copy a design, agents quietly reinterpreted it and dropped animation and interaction. Port layout, motion and behaviour as they are; if something cannot be ported, ask before deviating.

**F-48. Label variants with letters, and parts of the chosen one with numbers.**
Long descriptive variant names slowed every decision. A, B, C for options and A1, A2 for the parts you keep turned choices into one-word answers.

**F-49. A phone mockup has one scroll container.**
Absolutely positioned buttons and navigation floated over content and broke on small screens. Build the frame as a flex column with a single scrolling area, and keep calls to action in the flow.

**F-50. Fixed-height pages are packed by estimated height, not by item count.**
Pages for paper or e-ink overflowed when filled with a fixed number of items. Estimate each block's height, add an overflow guard, and look at the result after every generation.

**F-51. For headless browser PDFs meant for print or e-ink, use locally installed fonts.**
Web fonts were rasterised into bitmap glyphs in some exports and looked blurred. Install the font locally for the project (never system-wide without asking) and check the PDF's font list.

Also covered elsewhere: contrast, type size on the longest line, height zones and PDF checks ([`print-design`](../playbooks/print-design.md)), decks that stay decks on a phone ([`presentations`](../playbooks/presentations.md)), decisions before visuals ([`website-strategy`](../guides/website-strategy.md)).

---

Have a lesson that belongs here? Tell your advisor; it can report it to the maintainers (see `AGENTS.md`, "Feedback").
