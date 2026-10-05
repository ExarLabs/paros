---
title: cv-tailoring LOCAL
date: YYYY-MM-DD
status: active
description: Personal configuration of the cv-tailoring skill in this vault: where source CVs live and in which order to search them, the house CV format and anonymisation, the opportunity folder layout, people notes, and the language and signature of the covering note. No secrets.
schema: cv-tailoring.local.v1
---

# cv-tailoring: local configuration

> Copy this file to `LOCAL.md` next to your adopted `CURRENT.md`, then fill it in with your agent. The values below are invented. It holds **locations and preferences only, never secrets**. Keep it out of anything you share or publish.

## 1. Who uses it

- Mode: `<own CV for job applications | team lead proposing colleagues for bids>`
- Example: team lead at a small consultancy, Brightmoor Data (invented), proposing colleagues to partners and tenders.

## 2. Where source CVs live, in search order

| Order | Place | How to search | Notes |
|---|---|---|---|
| 1 | the vault: `Clients/Bids/**/profiles/` | file name contains the surname and `CV` | earlier bids often hold a fresh tailored copy |
| 2 | the vault: `Team/CV-library/` | file name | the master copies |
| 3 | a shared document library: `<library name>/profiles/` | search by "<Surname> CV" | choose by last modified date; if the tool cannot read the file, ask the person to download it |

## 3. House CV format

- File type: `<docx | odt | markdown | pdf from a source file>`
- Layout to keep: header with logo, initials block, two-column skills table, experience by employer.
- Anonymisation: `<initials only in the document, full name only in the file name | full name>`
- File names: `<Name> CV - v0 <source>.docx`, `<Name> CV - <opportunity short> v1.docx`

## 4. Opportunity folders

- One folder per opportunity: `Clients/Bids/<Opportunity>/`
- Verbatim request: `_sources/`
- CVs and plans: `profiles/`, `profiles/_plans/`
- Notes with the covering note draft and action items: `NOTES.md`

## 5. People notes

- Where: `Team/People/<Name>.md`
- Sections the skill may read: role, level, form of employment, allocation, skills.
- Section the skill never reads: `## Compensation` (name yours here if it differs).
- Where current load is recorded (for the capacity check): `<time records, allocation table, invoices folder>`

## 6. Covering note

- Language: the language of the thread (fallback: `<language>`)
- Voice: short sentences, first person plural, no superlatives.
- Signature: `<how you sign internal notes>`

## 7. Local notes

Anything your setup taught you that is specific to it (a library that hides older versions, a partner who always wants a one-page CV). General lessons go to the skill's `observations/` folder instead, so they can improve `CURRENT.md`.
