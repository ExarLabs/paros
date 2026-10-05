# Website strategy: seven layers and a pulse

What stands behind a marketing website that is rich and beautiful, yet clean? Not the visual layer. Most ugly or generic sites are not badly designed; they skipped the decisions that come before design. This guide is a decision spine for any site you build with an agent, sized to the project so a small business does not drown in strategy. Principles: P02 (presentation), P12 (one fact, one owner), P11 (prove it works).

## The model: seven layers and the Pulse

This is not a waterfall. Copy and wireframe are made **together** (layers 5 and 6), there are loops back, and the Pulse feeds back into layers 2 to 5.

| # | Layer | What it produces | Useful frameworks |
|---|---|---|---|
| 1 | **Brand core** | Why you exist, what you believe, your character, and what you do **not** do. One page, not a manifesto. This is what makes the site not generic | Golden Circle, brand pyramid |
| 2 | **Market and audience** | Who it is for, how aware they are of the problem, which alternatives they weigh, in what decision situation they arrive, what progress they want | Jobs to be done, awareness levels |
| 3 | **Positioning and offer** | Category, main promise, differentiator, the concrete offer, the conversion goal | Competitive alternatives, distinctive capabilities, value, best-fit customer, category |
| 4 | **Message and proof** | Message hierarchy, objections (why they would not believe you), proof, trust elements. The clean message is decided here, but not yet the words | Story-based messaging, objection mapping |
| 5 | **Narrative UX and information architecture** | Which pages and sections in which order, the persuasion arc (problem, why us, proof, action), the call-to-action logic. **Made together with the copy** | Content first, copy-first wireframes |
| 6 | **Creative direction, then design system** | **First** a visual direction (premium, artisan, editorial, technical, minimal), **then** the formal system: palette, type, tokens, components, rules of restraint. A design system does not start from tokens; it starts from a strong direction | Mood boards, atomic design, design tokens |
| 7 | **Build, polish, quality gate** | The finished, mobile-first site and its gate: speed, responsiveness, accessibility, image quality, consistency, restrained interaction. **This is where "beautiful" lives** | Mobile first, automated checks |
| ↻ | **Pulse** (a loop, not a layer) | Analytics, tests, iteration; feeds back into layers 2 to 5 | Message-market fit, conversion review |

### Inputs that are not layers

- **Brand asset audit:** logo, existing colours, type, photo style, brand debt, taboos. It **constrains** layer 6.
- **Content and media inventory:** are there good photos, video, product shots, client logos? Without them the creative direction looks different.
- **Business logic:** a full business model only when needed. For a landing page the monetisation logic is enough: for whom, which offer, which conversion.

## Tiers: size the spine to the project

Seven layers are not for everyone. A neighbourhood bakery needs trust and conversion (opening hours, address, price list, an order button), not a manifesto. Too much strategy for a small project is analysis paralysis.

| Tier | Layers | When |
|---|---|---|
| **Lean** | 5 + Pulse: foundation (brand core and positioning merged), audience and offer, copy-first wireframe (message, structure and copy together), visual identity (asset audit, direction and system in one), build and polish | Small business, campaign page, first version, sales landing |
| **Standard** | 7 + Pulse | A typical marketing site, a growing company |
| **Premium** | 9 + Pulse: the full business model becomes its own layer, audience separate from positioning, and offer and conversion architecture separate too | Premium services, high-value B2B, investor pages, a new category |

A rough feel for effort: a Lean foundation takes 30 to 60 minutes, a Lean copy-first wireframe one to two hours per page; a Premium audience layer includes real interviews (five to ten conversations), which no tool replaces.

Each layer has a **done signal** you can check. Examples: the Lean foundation fits on one page and its "what we do not do" field is filled; the offer says who gets what and how it converts; every wireframe section has one idea, one proof point and real text (no placeholder text).

## Where beauty lives

- **Clean means restraint.** One idea per section, one type, colour and motion system, white space. The design system and a good structure give this.
- **Rich and beautiful means craft in the execution,** not in the catalogue. Design catalogues give correct defaults; beauty is a correct system built with mastery.
- **Meaningful, not generic, comes from layers 1 to 4.** Most ugly marketing pages skipped them.
- **And it works,** because you know for whom, at what decision moment, and which new belief they must accept before acting. And because you measure.

## The state file

Each site project keeps one state file at the root of its area in the vault, for example `brand-spine-state.md`. It is the single source of truth for where the project stands, so any session (or any agent) can say "we are at layer 4, the next step is the objection list" without guessing.

Frontmatter:

```yaml
---
project: Riverside Pottery Studio
project_slug: riverside-pottery
tier: lean                  # lean | standard | premium
status: in_progress         # planning | in_progress | paused | shipped | iterating
started: 2026-09-01
last_updated: 2026-10-05T10:30
current_layer: 3            # or "pulse" when iterating
anti_references:            # protection against looking like everything else
  other_projects: [the bakery site already uses warm brick, cream and a serif]
  first_category_reflex: "earthy beige and hand-drawn icons"
  forbidden_palettes: []
---
```

Body: one section per layer, with the same small schema:

```markdown
### 3. Positioning and offer
- status: not_started | in_progress | complete | needs_revision
- artifact: positioning.md
- next_action: one sentence
- blockers: []
- decisions:
  - 2026-10-04: the offer is a six-week evening course, not single classes
```

The anti-references matter more than they look: when you build several sites with the same agent and the same tools, they converge on the same look. Naming the first and second category reflex, and what other projects already use, keeps each site its own.

## What this model does not do

- **The vision is rarely stable.** The market decides, and the brand core often becomes clear only at the end. That is why there is a Pulse.
- **AI tools are not flawless.** They are a source of risk, not magic; the quality gate in layer 7 is not optional.
- **Beauty is not conversion.** A beautiful page can be slow or confusing. Craft serves conversion, it does not replace it.
- **It does not replace strategic thinking** in layers 1 to 4. A person has to do that work; the agent asks, drafts and checks.

## Downstream

```
strategy (layers 1 to 7 + Pulse)  ->  site factory  ->  staging, deploy, domain, analytics
"what, for whom, why, and does it work"   "how it goes live"
```

How it goes live: [`playbooks/publish-a-microsite.md`](../playbooks/publish-a-microsite.md). The same design system then carries over to [`presentations`](../playbooks/presentations.md) and [`print-design`](../playbooks/print-design.md); when a printed piece carries a QR code, the system of the page it leads to wins.

## Ask your agent

> Start a website strategy for <project>: propose a tier, create the state file in its area, and walk me through the first layer.
