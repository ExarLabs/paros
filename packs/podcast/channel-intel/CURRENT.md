---
title: podcast channel-intel
date: 2026-10-05
status: active
description: Maintains the channel intelligence file that the title, thumbnail, cold-open and description skills read, by feeding measured post-publish patterns back into pre-publish work; diagnoses growth or decline in four layers instead of comparing two windows, and enforces validation rules for any scoring or forecasting model (blind scoring, out-of-sample tests, noise first, channel type first, comparable benchmarks).
version: 1.0.0
upstream:
  # filled in when adopted into a vault
---

# channel-intel: the loop from measured results back to the next episode

The metadata skills are only as good as the patterns they rank against. This skill is the single path by which post-publish measurements reach pre-publish decisions. If it does not run, the title and thumbnail skills work from stale beliefs.

## Constitution

Only the owner changes this section. The learning machinery never touches it.

- The **structure** of the channel intelligence file stays; only numbers and patterns are updated. Several skills read it by section.
- Every number carries its date and source. A number from a sub-sample is never quoted as a channel figure.
- A model's accuracy is quoted only from an out-of-sample test. A claim that fails validation is withdrawn in writing, not quietly dropped.

## Personal settings: LOCAL.md

Show block, where the intelligence file, the syntheses, the patterns file and a monthly time series live, how to reach analytics, the update cadence, and the section list of the intelligence file. Without `LOCAL.md`, create the intelligence file with the sections below.

Suggested sections of the intelligence file: audience (channel baseline, declared versus real, by topic); what works (top performers); title patterns (working, failing, length); thumbnail patterns; hook and cold open patterns; description and search; series; end screens and in-channel navigation; publishing time.

## When to use

- After every five to ten new syntheses, or at the end of a synthesis batch.
- "Update the intelligence", "what changed?"
- Any trend question: "are we declining?", "is the channel growing?", "what happened last month?"
- Any time a scoring or forecasting model is built, quoted or updated.

## Steps: updating the intelligence

1. Read the patterns file, the tracking matrix and the current intelligence file.
2. Compare: new audience patterns, changes in the top ten, title, hook or thumbnail patterns that worked or failed, traffic source shifts, retention insights.
3. Update numbers and patterns in place, each with date and source. Keep the structure.
4. Report: syntheses analysed, new patterns, top-ten changes, files updated.

## Trend diagnosis

On a channel where old videos ride recommendation waves, comparing the last 30 days with the previous 30 misleads: the window can show any sign. The minimum answer has four layers, in this order:

1. **Watch time and average view duration next to views.** Falling views with steady watch time is a quality gain. Trouble is when watch time falls too.
2. **The daily trajectory inside the window.** Where it opens and closes: a wave fading from a peak, or a drop below the baseline?
3. **Weekly views of the top five videos.** Which wave peaked, which is fading, did a new one replace it?
4. **Publishing cadence in the same window.** A publishing gap is the most common hidden cause.

Two cheap controls:

- **Year over year:** the same window a year earlier separates season from trend. In one measured case a window that looked like a 13 % decline was a 55 % increase year over year.
- **Subscribers per thousand views, read with the recommended-traffic share.** When the share of recommended traffic rises, the conversion rate falls partly through dilution (a colder audience), not failure. The north star is returning viewers, not raw subscriber counts.

Keep a monthly time series and extend it each month.

## Validation rules for scoring and forecasting models

If this skill builds, runs, quotes or updates a model that predicts performance from content (a popularity score, a host score):

1. **Blind scoring.** The scorer must not see or be able to infer the outcome it predicts. For a new episode: three independent scorers, transcript only, median per dimension. A scorer who knows the views scores backwards, and the correlation measures itself.
2. **Out-of-sample test.** Accuracy measured on the fitting data is not accuracy. At least leave-one-out cross-validation; before any public claim, an external sample (another channel) with a decision threshold fixed in advance.
3. **Noise first.** Before tuning weights, measure test-retest reliability. While two independent scorings differ by ten points or more, weight tuning is meaningless.
4. **Channel type first, before scoring an external channel.**
   - **Distribution pre-filter:** right after pulling the catalogue, compute the 90th to 10th percentile ratio and the top-ten share of views. A narrow spread with a top-ten share under about 10 % means a brand-driven channel; a content model does not apply.
   - **On the scored era:** channels change type over their life; classify the same era you score.
   - **With the epistemic register:** on a tribe- or worldview-driven channel, a model that measures mainstream breadth is structurally blind. Say so in advance.
   - **The pre-filter is necessary, not sufficient:** one channel passed it and the model still gave an inverted signal. Pilot five to ten episodes to check each dimension's direction before the full run.
5. **Benchmarks only from the same protocol.** A sub-sample mean and a full-catalogue mean are not comparable.

Communicate forecasts as a **band** (hit candidate, baseline, niche) with an interval, not a decimal score. A difference under about five points between two scores supports no decision.

## Output

The updated intelligence file, and a short report. For trend questions: the four layers plus controls, then the conclusion. For model work: which validation rules were met, and the numbers that may be quoted.

## Pitfalls

- Never answer a trend question with a two-window comparison; use the four layers plus year over year. <!-- rule:R-001 since:2026-08-16 -->
- Score blind, test out of sample, measure noise before tuning; an in-sample accuracy claim for a scoring model had to be withdrawn when an independent validation found a far weaker fit. <!-- rule:R-002 since:2026-08-21 -->
- Classify an external channel's type before scoring it, on the scored era, with its epistemic register, then pilot. Three of five external validations failed or inverted without this. <!-- rule:R-003 since:2026-10-02 -->
- Quote a benchmark only from the same protocol; a sub-sample mean was cited as a catalogue figure in three documents. <!-- rule:R-004 since:2026-10-02 -->
- Keep the structure of the intelligence file; other skills read it by section. <!-- rule:R-005 since:2026-07-28 -->
- Audience definitions drift: replace any declared audience with the measured one, with date and source, and note that per-video demographics are not the channel's. <!-- rule:R-006 since:2026-07-28 -->
- Shares can exceed likes on a podcast channel; when they do, ask "who would they send it to", not "would they like it". Low evidence: one channel. <!-- rule:R-007 since:2026-07-28 evidence:low -->
- When the owner corrects a conclusion, record it as a learning packet in this skill's `observations/` folder (P05). <!-- rule:R-008 since:2026-10-02 -->
