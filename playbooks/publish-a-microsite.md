---
title: publish-a-microsite
date: 2026-10-05
status: active
description: Playbook for a small website built from your notes and deployed in minutes on a static host. A build process (scaffold, real copy, design system) plus a separate design judgement step, legal pages that reuse the real header and footer, mechanical pre-deploy checks, staging before production, the agent running an approved deploy, and a commit and push after every deploy.
---

# Playbook: publish a microsite

A microsite is a small website: one to a handful of pages for an event, a course, a service, a campaign or a club. With an agent it takes minutes to build, which is exactly why it needs a process: the fast part is the build, the slow and costly part is everything that goes wrong silently afterwards (a legal page that looks like it belongs to another site, a deploy from an old copy that rolls back the live page, work that exists only on one machine).

## What you get

- A **site factory** of your own: one folder (outside the vault, under git) with a scaffold, a shared design system or theme, one subfolder per site, a deploy script and a pre-deploy check script.
- For each site: **real copy from your notes**, a design pass by a separate judgement step, legal pages with the site's real header and footer, and a deploy to **staging first, then production**.
- After every production deploy: **a commit and a push**, automatically, so the live site always exists in the repository.

## Before you start

| Piece | Status |
|---|---|
| This procedure | here |
| The strategy before the build (what to say, to whom, how big the project is) | [`guides/website-strategy.md`](../guides/website-strategy.md) |
| The factory: scaffold, theme, `deploy` and `pre-deploy-check` scripts | written by the agent at adoption, **outside** your vault, in a git repository; nothing in this repository yet |
| A static host account (for example Cloudflare Workers or Pages, Netlify, GitHub Pages) | created by **you**; the agent never signs up or handles passwords |
| The host's API token | stored by you outside the vault ([`kits/secrets`](../kits/secrets/README.md)); scripts load it without printing it |

The agent asks:
- What is the site for, and what should a visitor do on it (one action)?
- Which notes are the source (an event note, a course outline, a service description)?
- Is there an existing brand, logo, colours, fonts?
- Do you have a domain, or is the host's free address fine for now?
- Which legal pages does your country require (imprint, privacy notice), and from which note does the company data come?

## Steps

### 1. Strategy, sized to the project

Do not start with colours. Decide the tier first (Lean for a small business or a campaign page, Standard for a typical marketing site, Premium only where the stakes justify it) and work through the layers in [`website-strategy`](../guides/website-strategy.md). For a Lean site this is about two hours: one page of foundation, one offer, copy-first wireframes.

### 2. Scaffold the site

The agent creates the site folder from the factory scaffold (`new-site <slug> <theme>`), registers it in the factory's site list, and checks that no placeholder survived (a quick search for the scaffold's placeholder marker). A scaffold script that fails half way leaves a half-made folder: remove it before running again.

### 3. Real copy from your notes

Every section gets one idea, one proof point and **real text**, taken from the source notes. Placeholder text and invented facts are not allowed: if a phone number, an address or a company registration number is missing, the page says so to you, it does not make one up. Invented data on a live site is worse than an empty field.

### 4. Build, then a separate design judgement

Two different jobs, deliberately kept apart:
- **The build process** (a skill or a checklist): structure, components, responsive layout, assets, metadata.
- **The design judgement** (a design review skill or a second pass with a different brief): hierarchy, typography, spacing, restraint, accessibility. When the two disagree, the judgement wins.

Rules for the code: no inline `<script>` (keep JavaScript in files; structured data blocks are the only exception), and if you load your own CSS or JS with a version marker (`style.css?v=7`), **bump the marker in every page that references it** on each change, or browsers keep running the old file.

### 5. Legal pages with the real header and footer

The most common defect in small sites: the home page gets a custom, branded header and footer during polishing, and the legal pages keep the bare scaffold version. The content renders fine, so nobody notices that the page looks like it belongs to another site. The rule: **legal pages reuse the exact header and footer markup of the home page** (simplify interactive bits like a language switcher, keep the structure and classes). Do not fix this by hand per site: make it a check (step 6).

### 6. Pre-deploy checks: mechanical, not by eye

A script runs before every deploy and blocks on failure. Typical checks:
- the working copy is up to date with the remote (**pull first**: a deploy from an old checkout rolls back the live site);
- no scaffold placeholders left, no inline scripts, no broken internal links, no missing images;
- legal pages share the home page's header and footer classes;
- every page has a title, a description and a language attribute;
- no secrets or private notes in the output folder.

Every recurring defect class becomes one more check. Fixing the same mistake page by page is a sign a check is missing. Watch for tool differences between machines: a check that uses a feature your system's `grep` does not support may fail silently and report false results.

### 7. Staging first

Deploy to **staging** (a separate address, ideally on the project's own domain once it has one) and verify there:
- open it on a phone-sized viewport and a desktop one;
- click every link, including the legal pages and any QR code targets;
- compare the downloaded page with the local file (same byte size is a falsifiable check; "looks right" is not).

If the custom domain still shows the old version while the host's own address shows the new one, the CDN cache is stale: **purge it** (both the `/page` and `/page.html` forms if the host redirects one to the other). A cache-busting query string does not help with a CDN cache.

### 8. Approval, then the agent deploys to production

You look at staging and say yes. From then on, running the production deploy is the agent's job, not yours: you approved the content, the agent runs the command. Two limits stay:
- the agent deploys **only what you approved**, and tells you if staging also carries other, unapproved work (for example commits from another session);
- the first time, your agent platform may ask you to allow the deploy command; that is your decision to make once.

### 9. Commit and push after every deploy

The deploy script's last step: commit the site folder and the site list with a message like `chore(<slug>): deploy production build <n>`, and push. If the push is rejected, pull with rebase and try again; if that fails, a loud warning with the exact commands to fix it. Stage **only that site's folder**, so another site's half-finished work is not swept in, and list any other unpushed or uncommitted factory files at the end so they do not stay local by accident.

Why it matters: a static host treats the uploaded folder as the whole truth. A deploy from another machine that lacks your latest work **deletes** what is missing from the live site.

## Check that it works

- The pre-deploy check fails when you deliberately break a legal page's header, and passes again after you restore it.
- Staging and production show the same build number, and the production page downloaded with a plain HTTP client has the same size as your local file.
- `git log` on the factory shows a deploy commit for the build that is live, and `git status` is clean.
- On a second machine, a fresh clone of the factory can deploy the site without anything copied by hand.

## Pitfalls

- **Strategy skipped.** A beautiful, generic page. The meaning comes from the foundation layers, not from the theme.
- **Invented data as a placeholder.** It goes live sooner or later.
- **Deploying from a stale checkout.** Always pull first; parallel sessions and colleagues commit too.
- **Live work that exists only locally.** Commit and push after every deploy, every time.
- **Commits with a broad pathspec** in a shared factory: other sessions may have staged files. Commit with an explicit path.
- **Large media on a static asset host.** Some hosts do not answer byte-range requests, so audio and video seeking jumps back to the start; load big media another way, and mind the per-file size limit.
- **Treating an unlisted URL as private.** An address nobody can guess is obscurity, not access control. A page only you need belongs in your local dashboard, not on the web ([`build-a-dashboard`](build-a-dashboard.md)).
- **A token typed into the chat.** Never; the deploy script reads it from your secret store.

## Principles behind it

- [P00](../principles/P00-constitution-and-boundaries.md): publishing is approved by you; running the approved deploy can be delegated.
- [P11](../principles/P11-health-contract.md): mechanical checks and a byte-size comparison instead of "it looks fine".
- [P10](../principles/P10-backup-and-recovery.md): the repository, not one machine, holds the live state.
- [P07](../principles/P07-secrets.md): host tokens outside the vault.
- [P12](../principles/P12-one-fact-one-owner.md): the note is the source; the page is its published view.

## Related

- Guide: [`website-strategy`](../guides/website-strategy.md) (the layers before the build).
- Playbooks: [`presentations`](presentations.md) (decks published under the same site), [`print-design`](print-design.md) (posters and roll-ups whose QR code leads here), [`publish-from-your-vault`](publish-from-your-vault.md) (generated pages from vault data).
- Kit: [`kits/secrets`](../kits/secrets/README.md).
