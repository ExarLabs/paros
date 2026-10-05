---
title: meeting-archive LOCAL
date: 2026-10-05
status: active
description: Personal settings for the meeting-archive skill (recorder folder, temporary folder, areas and their meeting folders, where clients, leads and partners live, shared mirrors, confidentiality, index refresh). Copy to LOCAL.md and fill in your own values.
---

# meeting-archive: personal settings

> Example values for a fictional person who runs a small design studio and volunteers in a neighbourhood repair cafe. Copy this file to `LOCAL.md` next to `CURRENT.md` at adoption and replace everything below with your own. No secrets here: tokens for a shared drive live in your secrets folder (P07).

## Recordings

| What | Where |
|---|---|
| Recorder saves to | `~/Recordings/` (file name is the start time, `YYYY-MM-DD HH-MM-SS.m4a`) |
| Temporary folder for copies and cuts | `~/Media/temp-audio/` (outside the vault) |
| A recording longer than | 3 hours is treated as a forgotten recorder |

## Areas and meeting folders

| Area | Internal meetings | Team meetings (about the team itself) |
|---|---|---|
| Studio | `Work/Studio/meetings/` | `Work/Studio/team/meetings/` |
| Repair Cafe | `Community/Repair Cafe/meetings/` | `Community/Repair Cafe/team/meetings/` |
| Home | `Home/meetings/` | not used |

## Outside parties

| Class | Where |
|---|---|
| Client | `Work/Studio/Clients/<Client>/meetings/` (for example `Work/Studio/Clients/Northwind/meetings/`) |
| Lead | `Work/Studio/Leads/<Lead>/meetings/` |
| Partner | `Work/Studio/Partners/<Partner>/meetings/` (printers, the accountant, the landlord) |

The Repair Cafe has no clients. The library that lends the hall counts as a partner: `Community/Repair Cafe/Partners/Library/meetings/`.

## Shared mirrors

| Meeting | Mirror | Rule |
|---|---|---|
| Studio client or lead | Studio team drive, `Clients/<Client>/meetings/transcripts/` and `notes/` | ask each time |
| Studio internal | Studio team drive, `Internal/meetings/` | ask each time |
| Repair Cafe internal | Repair Cafe shared folder, `meetings/` | ask each time |
| Any team meeting, anything about a person | none | never mirrored |
| Home | none | vault only |

## Confidential

- Client meetings marked confidential by the client: not to the external transcription service without my yes, never to a mirror other than that client's own folder.
- Anything with health, pay or legal details: vault only, ask before deleting the audio.

## Naming

- Slug: lowercase English words, hyphenated, three or four words at most (`autumn-repair-day`).

## Index

- Refresh: `python ~/paros-kits/search/build_index.py` (or whatever your vault uses), then search two or three words from the new note.
