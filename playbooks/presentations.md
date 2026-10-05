---
title: presentations
date: 2026-10-05
status: active
description: Playbook for slide decks built as code on one shared deck engine and one design system. Fixed 1920x1080 slides that stay slides on a phone (scaled, with round previous and next buttons, a rotate hint in portrait), copy buttons injected on every prompt, published under a site and shared as a direct link. Never a re-flowed web page.
---

# Playbook: presentations

A deck built as code is a web page that behaves like a slide show: the same file is presented from a laptop, opened on a phone by the audience, and linked from an email. The risk is that it slowly turns into "a web page that looks like a presentation": slides that re-flow into a scrolling page on a phone, ad hoc styling per deck, a different navigation every time. This playbook keeps decks decks.

## What you get

- **One deck engine** shared by all your decks (navigation, scaling, keyboard and touch controls, print), and **one design system per deck** (a theme: colours, fonts, slide layouts).
- Every deck as **fixed 1920 × 1080 slides**, scaled to fit any screen.
- **On a phone the deck stays a deck:** the same scaled 16:9 slide, round ‹ › buttons for previous and next, and a "rotate your phone" hint in portrait. No re-flow into a long page.
- A **copy button on every prompt** shown on a slide, so the audience can paste it into their own AI.
- The deck **published under a site** and handed over as one direct link.

## Before you start

| Piece | Status |
|---|---|
| This procedure | here |
| The deck engine (one HTML/CSS/JS bundle) and a theme folder | written by the agent at adoption, inside your site factory ([`publish-a-microsite`](publish-a-microsite.md)), **outside** your vault; nothing in this repository yet |
| A publish script (`publish-deck <deck> <site> <path>`) | written by the agent at adoption |
| The deck's content | a note in your vault: outline, speaker notes, the prompts you will show |

The agent asks:
- Who is the audience, how long is the talk, and will people open the deck on their phones?
- Which design system? One deck, one theme. Other brands appear at logo level (a partner logo on a slide), not as a second palette.
- Is there an earlier deck that already behaves the way you like? That one is the reference.

## Steps

### 1. Start from the reference, not from a blank page

Before building, **open your reference deck** (an earlier deck you were happy with) and note how it behaves: navigation, slide numbers, how it looks on a phone. Do not invent new UI behaviour for a deck before checking how the existing ones work. If this is your first deck, the engine's defaults are the reference.

### 2. Content from the vault

The outline lives in a note: one slide per idea, speaker notes under each, the literal prompts in code blocks. The deck is generated from or written next to that note, and the note stays the source: a change of content starts there.

### 3. Build on the shared engine

- Create the deck folder (`decks/<slug>/`) from the engine's template and pick the theme.
- Slides are fixed **1920 × 1080**; the engine scales the whole slide to the screen. Do not write per-slide responsive layouts.
- Keep custom code small. If a deck needs a feature (a timer, a QR slide, a video slide), add it to the engine so the next deck has it too.

### 4. Phones: a deck stays a deck

The behaviour to keep, because the alternative was tried and rejected:
- the same 16:9 slide, scaled down;
- touch navigation **only** through round ‹ › buttons (no tap-anywhere to advance, no swipe, which fire by accident while zooming or scrolling);
- in portrait, a hint to rotate the phone.

A "reading mode" that re-flows slides into a scrolling page is not a presentation; it is a different product. If people need a readable handout, make a separate page or a PDF.

### 5. Copy buttons on prompts

Every prompt shown on a slide (a `.prompt` box) gets a copy button. Inject them with one script, not by hand, so future prompts get one too:
- capture the prompt text **before** adding the button;
- an icon-only button on the right edge, vertically centred, with padding reserved so text never runs under it;
- feedback by swapping the clipboard icon for a check mark for about 1.5 seconds;
- the click handler stops propagation (decks often advance on any click);
- use the clipboard API with a hidden textarea fallback for pages opened without HTTPS.

The same idea applies to any element someone may want to reference later (a card, a framework, a checklist): give it a stable id and a copy-reference button.

### 6. Publish and share a link

- Publish the deck under a site: `publish-deck <slug> <site> <path>/presentation`.
- Deploy to **staging**, open it on a phone-sized viewport and a desktop one, step through every slide.
- After your yes, deploy to production, commit and push ([`publish-a-microsite`](publish-a-microsite.md), steps 7 to 9).
- Hand over **the direct public link**. No password unless you ask for one, and remember that a client-side password is not protection: nothing confidential goes on a public deck.

## Check that it works

- On a phone in landscape, every slide shows whole, and the ‹ › buttons move one slide at a time; tapping the slide itself does nothing.
- In portrait, the rotate hint appears.
- Clicking a copy button puts exactly the prompt text on the clipboard (paste it somewhere to check) and does not advance the slide.
- The production link opens the same build as staging, and the factory repository has the deploy commit.

## Pitfalls

- **A re-flowed "mobile version".** It reads like a web page, and the presenter loses the deck everyone else sees.
- **Inventing behaviour per deck.** Check the reference deck first; put shared behaviour into the engine.
- **Two palettes in one deck.** One theme per deck; other brands at logo level.
- **Hand-placed copy buttons.** The next prompt you add will not have one.
- **Content edited only in the HTML.** The vault note drifts from the deck; next time you rebuild the old version.
- **Confidential material behind a client-side password.** Anyone can read the page source.

## Principles behind it

- [P02](../principles/P02-presentation.md): presentation is HTML, derived from markdown.
- [P04](../principles/P04-thin-entry-live-definition.md): one shared engine, thin decks on top of it.
- [P05](../principles/P05-closed-loop-learning.md): every correction ("this is not a presentation") becomes an engine rule.
- [P00](../principles/P00-constitution-and-boundaries.md): publishing is your decision.

## Related

- Playbooks: [`publish-a-microsite`](publish-a-microsite.md) (the factory, staging, deploy, commit and push), [`print-design`](print-design.md) (the same design system on paper), [`build-a-dashboard`](build-a-dashboard.md) (copy-reference buttons on cards).
- Guide: [`website-strategy`](../guides/website-strategy.md) (where a design system comes from).
