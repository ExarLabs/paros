---
title: print-design
date: 2026-10-05
status: active
description: Playbook for physical display material (roll-ups, posters, banners) designed as HTML in real centimetres. Covers bleed and the visible area, height zones measured from the floor, the two mandatory measurements before composition (accent colour contrast on its background, font size checked on the longest line), approval PNGs, and the print PDF checks done on the finished file.
---

# Playbook: print design (roll-ups, posters, banners)

Designing something that will hang in a hall is not designing a web page. The size is real, people read it from several metres away, the bottom of a roll-up is hidden behind people's legs, and the printer receives a file you cannot fix afterwards. This playbook turns that into a repeatable procedure, so every new roll-up does not have to be reinvented.

## What you get

- A print design built as an HTML page **measured in centimetres**, previewed at true proportion, with a technical view that shows bleed and height zones.
- Two numbers written next to the design before anything is composed: **the contrast of the accent colour on its background**, and **the font size measured on the longest line**.
- A PNG for approval, and a separate **vector PDF for the printer**, checked as a file (size, pages, fonts, image resolution, QR code), not trusted because the export said "done".
- A short **hand-over sheet** for the printer: size, bleed, colour mode, fonts, effective image resolution, and the questions you still have for them.

## Before you start

| Piece | Status |
|---|---|
| This procedure | here |
| A small print toolchain (one HTML template sized in `cm`, a preview page, a PNG export, a PDF export with checks) | written by the agent at adoption, **outside** your vault (a tools or design folder); nothing in this repository yet |
| A contrast calculator | one short script, written by the agent (the WCAG contrast formula, a few lines) |
| The brand's real values | hex codes, font files, logo (vector if possible), the exact text |

You need: a Chromium based browser (Chrome, Edge) or a headless one through a script, and the brand's own font files. The agent asks:
- Which format? (a roll-up of 85 × 200 cm, a 100 cm wide one, a poster, a banner) and do you know the printer yet?
- Which design system? If the brand has more than one living look, **you choose**; this is not something the agent derives.
- Where will it stand: on a floor among people, or on a stage?
- What exactly must it say, word for word?

## Steps

### 1. Collect real values, not a mood

Hex codes, font family and files, logo, slogan, the literal text. If the brand has a live website, measure the values there instead of working from memory. The brand's own web font is the authentic one; a look-alike substitute is not. Check that the font covers your language's accented letters **in every weight you use**: some families ship extended Latin only for the regular cut, and a bold heading then falls back to a system font for two letters.

### 2. Measurement one: the accent colour on its background

Before any composition, compute the contrast ratio of the accent colour on the page background (the WCAG formula; the agent runs it).

| Combination (invented example) | Ratio | Consequence |
|---|---|---|
| fresh lime `#8FD14F` on paper `#F6F8F0` | 1.72:1 | the lime may only be a fill, never text or a line |
| mustard `#F2C230` on cream `#FAF7F0` | 1.57:1 | the planned thin rule is dropped |
| dark ink `#14321F` on lime `#8FD14F` | 7.57:1 | the highlighted word sits in a lime box, in dark ink |

The rule: **below 3:1 the accent is a fill only**: no text, no outline, no hairline. The answer is not to drop the colour but to **swap roles**: dark letters on the coloured box, a light logo in a dark band. Measure the **logo's colours** on the background too: a pale tip of a symbol at 1.0:1 makes the mark fall apart. The pattern repeats: fresh, light accent colours on light backgrounds almost always fail.

### 3. Measurement two: font size on the longest line

Height is not the limit; **width is**. One long word pulls down the size of the whole page. Measure in the running page, with the real font metrics (a canvas `measureText` in the browser), not by counting characters:

```js
await document.fonts.load('700 120px "Brand Sans"');
const c = document.createElement("canvas").getContext("2d");
const cm = 12;                                   // preview scale: px per cm
c.font = `700 ${10.5 * cm}px "Brand Sans"`;      // 10.5 cm type size
c.letterSpacing = `${-0.03 * 10.5 * cm}px`;      // the page's own letter spacing
c.measureText("fresh every morning").width / cm; // result in centimetres
```

Then compare it with the width of the type area. Write the result **into the stylesheet as a comment next to the size, naming the line it was measured on**. Rules that came from real misses:
- **Include the letter spacing.** Without it, `-0.03em` on a 13 character line at 10 cm is about 4 cm of error, which is the whole safety margin.
- **The lower bound is the longest unbreakable word**, not the longest line: a line can only break at spaces. Divide the type area by that word's measured width to get the maximum size, then round down for a margin.
- **Calibrate the measuring page.** A font check can say "available" while the measurement silently runs on a fallback font (about 10 % off, enough to flip a decision). Load the real font first, confirm it is in the `loaded` state in the page you measure, and re-measure one value recorded earlier: if it matches within 0.1 cm, trust the pad.
- **The measured size belongs to the text, not to the page.** Any text change requires a new measurement; nothing will fail if you skip it, the page renders and the PDF exports.
- Rule of thumb for a check: 1 cm of capital height reads from about 3 metres.

### 4. Build in centimetres, with bleed and zones

- Every dimension is a `cm` based CSS variable. If you start sizing in pixels, both the measurements and the print file break.
- The print is taller than what people see: an 85 × 200 cm roll-up is typically printed about 217 cm tall, because a strip rolls into the cassette and another sits under the top bar. **Only an even background may run into the bleed**, so colour bands extend into it.
- **Height zones, measured from the floor:** the bottom 55 cm or so is hidden by people standing in front (unless it stands on a stage). Nothing essential goes there. A QR code belongs at about 64 to 90 cm, at the bottom of the text area or under a phone mock up, never in the hidden band.
- **Spread the content blocks over the whole visible height**, so the empty part falls into the hidden band. Never put a colour change above an empty field: it turns quiet space into a hole.

### 5. Judge the composition in the standing view

Make composition decisions only from the **standing view**: the visible area, without the cassette strip and the top profile, with a line drawn at the hidden-band height. The full print file makes the base look bigger and emptier than it is, and leads to wrong redesigns.

### 6. Images and logo

- **Look at every image you take over from another surface.** Small business website images are often social media composites with burnt-in text, a quote or a stock photo. You need the clean original.
- **Resolution on the printed size:** aim for 150 dpi, 100 at minimum. A 78 cm tall photo needs about 4,600 px; the website copy is often 800. Use the print asset, not the web one.
- Never enlarge a raster logo. Trace it if you must, **say that it is a trace**, and ask for the original vector before the final hand-over.

### 7. Approval PNG, then the print PDF

The PNG is **for approval only**. The printer gets a vector PDF at 1:1, generated from the same HTML. Then check the finished file, not the export's exit code:

1. **Measure the PDF itself:** page count, page size in mm (pt × 25.4 / 72), fonts, raster images. A browser can happily "print" an error page into a valid-looking PDF.
2. **Effective dpi of every raster at print size** (target 150, minimum 100).
3. **Full-resolution photo crops**; if one is missing, the build stops with an error instead of falling back to the web image.
4. **QR codes:** read the code back from the finished PDF, measure module size and quiet zone (4 modules, generated as part of the code, not as CSS padding), size it for the longest link, and **open the target page and compare it with the caption next to the code**. A wrong target passes approval easily.
5. **Render the PDF back to an image and look at it.** Text filled with a gradient can simply vanish from a browser-made PDF; put such words on the page as outlines.
6. **Machine-independent paths:** any setting that points to a folder is a list of candidates (the first that exists wins) plus an environment variable override.
7. **A missing check tool never means success.** If the PDF checker library is not installed, the check must fail loudly, or be done by hand (`pdfinfo`, `pdffonts`, `pdfimages -list`).
8. **A watchdog on the headless browser:** on some systems it does not exit after writing the file. Wait until the output exists and its size is stable, then stop it.
9. **Page size rounding:** browsers round the PDF page to 0.01 inch, which can leave a 0.3 to 0.5 pt white strip on the right or bottom edge. Give the size in inches rounded to 0.01, let full-bleed layers overshoot by a couple of pixels, and check that the four edge pixels of the rendered PDF are not white.

Things to know about browser-made PDFs: without `print-color-adjust: exact` the browser drops backgrounds; variable web fonts come out as vector glyphs (Type3), which some printers' software dislikes; static fonts are embedded, not outlined, so if the font licence asks for outlines, check the PDF's font list instead of assuming. The PDF is RGB; ask the printer whether their software converts, and ask for a proof of the brand's critical colour.

### 8. Hand-over sheet

Next to the PDFs, a short note: size, bleed, colour mode, fonts and how they are embedded, effective dpi of each image, and the open questions for the printer. Roll-up height conventions differ by about 5 cm between printers; confirm theirs before sending.

## Check that it works

- The two measurements are written next to the design, with the line the size was measured on.
- The technical view shows nothing essential in the bleed or below the hidden-band line.
- The PDF report lists the expected page count and the exact size in mm, every image at 100 dpi or more, and the fonts you expected.
- The QR code decodes from the finished PDF, has a 4 module quiet zone, and opens the page its caption promises.
- If only the text changed in a resubmitted PDF, sample the QR module grid in the old and new renders: zero changed modules proves the earlier check still holds.

## Pitfalls

- **Composing first, measuring later.** Both measurements decide the structure of the page; done afterwards they force a redesign.
- **Trusting the export.** "Done" from a script, a file that exists, a correct exit code: none of these is a checked PDF.
- **Measuring with a fallback font.** The number looks precise and is wrong by 10 %.
- **A text change without a new measurement.** The old number silently stops being true.
- **Judging the full print file.** It is not what anyone will see.
- **Web images and web logos in print.** They look fine on screen at any size.
- **A fixed port for a local preview server.** On some systems two servers can share a port silently and requests go to the wrong one; bind to port 0 to get a free one.
- **Publishing previews from a shared toolchain with uncommitted engine changes.** Another session's half-finished work can end up on a live page; publish engine files from the last commit, not from the working copy.

## Principles behind it

- [P11](../principles/P11-health-contract.md): prove it with the finished file, not with "the script ran".
- [P02](../principles/P02-presentation.md): the design is HTML, the PDF and PNG are derived from it.
- [P05](../principles/P05-closed-loop-learning.md): every miss above became a rule; yours will too.
- [P00](../principles/P00-constitution-and-boundaries.md): sending files to a printer is your act, never the agent's.

## Related

- Playbooks: [`publish-a-microsite`](publish-a-microsite.md) (where the QR code leads), [`presentations`](presentations.md) (the same design system on slides).
- Guide: [`website-strategy`](../guides/website-strategy.md) (which design system wins when there are several: the one the QR code leads to).
- Guide: [`add-a-skill`](../guides/add-a-skill.md): once you have made two print pieces, turn this procedure into a skill in your vault.
