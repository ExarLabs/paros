---
title: publish-from-your-vault
date: 2026-10-05
status: active
description: Playbook for making selected views of a vault public as a small static site. Notes stay the source; a data file is extracted from them, a generator writes the HTML (never hand-edited), a share gate checks every outgoing file for personal data and secrets, and only then is it deployed. Private views stay in the local dashboard.
---

# Playbook: publish from your vault

Some things in your vault are worth showing to others: a reading list, a seed library, a club's schedule, a course catalogue, a public changelog of your own system. Copying them into a website by hand creates a second truth that drifts away from the notes. This playbook publishes **views**: generated from the vault, checked before they leave, and replaced, never edited, on the web.

## What you get

```
note in the vault (the truth)
      |
      v
data file (JSON)        extracted from the note, or kept next to it
      |
      v
generator               writes the HTML; readable without JavaScript
      |
      v
share gate              personal data, secrets, private paths: blocks
      |
      v
pre-deploy checks       the site's own checks
      |
      v
deploy                  static host, after your yes
```

- A small static site with one page per published view.
- A change of state is **one field in the data** ("planned" becomes "done"), then regenerate and deploy. Nobody touches the HTML.
- A **share gate** that every outgoing file passes, with a report you read before anything is published.

## Before you start

| Piece | Status |
|---|---|
| This procedure | here |
| A site factory with staging, deploy, commit and push | [`publish-a-microsite`](publish-a-microsite.md) |
| The generator and the share gate script for your views | written by the agent at adoption, **outside** your vault; nothing in this repository yet |
| A denylist for the share gate (names, companies, clients, machine names, private folders) | written by **you** with the agent, kept outside the published folder |

The agent asks:
- Which view do you want public, and who is it for?
- Which note is its source?
- What must never leave: people, clients, money, health, family, mail, private folders?
- Does it really need to be on the web? If only you need it, from your phone or the workshop, a local dashboard or a synced note may be enough.

## Steps

### 1. Decide public or private, honestly

This playbook is about **publishing**: what goes outward. A view only you need belongs in your local dashboard ([`build-a-dashboard`](build-a-dashboard.md)), not on an unlisted web page: an address nobody can guess is obscurity, not access control. Never publish client data, finances, notes about people, or mail.

### 2. Mark what may go out

Publishing is opt-in. A note is eligible only if its frontmatter says so (for example `share: public`); no marker means private. A path-based denylist (private folders) blocks even a note that is marked by mistake.

### 3. Extract the data

The agent writes a small extractor: from the source note to a data file (`views/<view>.json`), with only the fields the page needs. Internal frontmatter, comments and hidden blocks never reach the data file. Links to notes that are not published become plain text, listed under "not published references", so the page has no dead links and leaks no titles.

### 4. Generate the HTML

A generator (`build` script) turns the data into complete HTML: readable without JavaScript, with search or filters added by a separate script file. The rule that matters: **the HTML is generated, never hand-edited.** A hand fix is overwritten by the next build, or worse, kept and drifting. Every page carries a provenance line: "generated from the owner's notes on YYYY-MM-DD; edit at the source".

### 5. The share gate

Before anything is deployed, a script checks every outgoing file and blocks on:
- denylist terms (names, companies, clients, machine names, private paths, email addresses);
- secret patterns (API keys, tokens, private keys);
- any text from notes not marked for sharing.

It warns (does not block) on things that need a human look, such as text in an unexpected language. The agent shows you the report and the list of files; **you** say yes. A gate that only runs when someone remembers is not a gate: make it part of the build or a pre-commit hook.

### 6. Deploy, verify, commit

Staging first, then production after your yes, then commit and push ([`publish-a-microsite`](publish-a-microsite.md), steps 6 to 9). Update the source note in the same round: it is the truth, the page is its view.

If the custom domain still shows the old version while the host's own address shows the new one, purge the CDN cache; check by downloading the page and comparing its size with the generated file.

## Check that it works

- Change one status field in the source note, run the build: exactly that item changes on the page, nothing else differs (`git diff` on the generated files).
- Put a denylisted word into a test note marked for sharing: the gate blocks and names the file and line. Remove it: the gate passes.
- Hand-edit the generated HTML, rebuild: your edit is gone. (That is the point.)
- A clone of the site repository on another machine can rebuild and deploy without files copied by hand.

## Pitfalls

- **Editing the HTML "just this once".** The next build silently removes it, or the page stops matching the notes.
- **An unlisted page for private things.** Obscurity is not protection; private views stay local.
- **Opt-out instead of opt-in.** "Everything except..." eventually publishes the one note you forgot.
- **A site that lives on one machine.** Without a commit, a push and an entry in the site list, it cannot be rebuilt elsewhere.
- **Line-ending noise after a build.** On some systems generated files show as modified without a real change; trust `git diff --numstat`, not the status list.
- **Third-party embeds that collect data.** Fonts, video previews and analytics are external requests; list them in the privacy notice or leave them out.

## Principles behind it

- [P12](../principles/P12-one-fact-one-owner.md): the note owns the fact; the page is derived.
- [P00](../principles/P00-constitution-and-boundaries.md): publishing is a deliberate act, with your yes each time.
- [P01](../principles/P01-persistence.md): the knowledge stays in plain files you own.
- [P07](../principles/P07-secrets.md): the gate blocks secret patterns.
- [P11](../principles/P11-health-contract.md): the gate is tested by deliberately breaking it.

## Related

- Playbooks: [`publish-a-microsite`](publish-a-microsite.md), [`build-a-dashboard`](build-a-dashboard.md) (private views), `share-with-your-team` (publishing to shared tools).
- Kit: [`kits/secrets`](../kits/secrets/README.md).
