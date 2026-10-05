# Playbooks: how to do it, step by step

A playbook is a guided path for one thing people want to achieve with PAROS: connect a tool, build a dashboard, organise knowledge, run meetings, think with several AIs. Each one comes from how PAROS is used every day, and the advisor walks you through it in **your** vault.

Ask with `/paros <question>`, for example `/paros how do I connect two Gmail accounts?` or `/paros how do I build a dashboard on my vault?`

**Status:** `ready` has a full playbook here; `planned` means the advisor answers from the principles, skills and kits that already exist, and a detailed playbook is on the way.

## Foundations
| Playbook | What you get | Status |
|---|---|---|
| [`organise-your-knowledge`](organise-your-knowledge.md) | Areas instead of projects, frontmatter with content descriptions, an entry file your agents read | **ready** |
| [`task-inbox`](task-inbox.md) | One task list with an inbox you drop things into unformatted; the agent sorts them | **ready** |
| `project-state` | One current-state file per long-running project or area | ready (skill: `skills/project-state`) |
| `search-your-vault` | Index-first search, ranked, in milliseconds | ready (kit: `kits/search`) |
| `shared-memory-across-machines` | One agent memory for every machine (symlink or junction into the vault) | planned |
| [`sync-and-backup`](sync-and-backup.md) | Your vault on every device (Obsidian Sync, iCloud, Google Drive, OneDrive, Dropbox or git, chosen for you) plus a real backup with a test restore | **ready** |
| `session-naming` | Session titles with machine, area and topic, readable on a phone | planned |

## Learning and reliability
| Playbook | What you get | Status |
|---|---|---|
| `teach-your-agents` | Corrections become rules, reviewed and integrated without compaction | ready (kits: `learn-merge`; agent: `maestro`) |
| `cognitive-cycle` | Weighted rules, visible use, a cycle report with a heat map | ready (kit: `kits/cognition`) |
| `health-checks` | End-to-end canary and checks that alert only on state change | ready (kit: `kits/health`) |
| `secrets-and-new-machines` | Secrets outside the vault, an inventory, encrypted transfer between machines | ready in part (kit: `kits/secrets`) |
| `build-your-own-skills` | Thin entries, live definitions, versions, packaging skills as plugins | ready (kit: `kits/thin-entry`) |

## Connectors
| Playbook | What you get | Status |
|---|---|---|
| [`connect-gmail-multiple`](connect-gmail-multiple.md) | Several Gmail accounts in parallel, each with its own token | **ready** |
| `connect-microsoft-365` | Outlook, Teams and SharePoint, including an extra tenant through a script | planned |
| `connect-any-mailbox` | Any IMAP and SMTP mailbox, sending only with approval | planned |
| [`connect-google-workspace`](connect-google-workspace.md) | Sheets, Forms, Drive and Calendar from scripts, several accounts | **ready** |
| `connect-a-crm` | A CRM as the shared truth: contacts, deals, events, sign-ups synced from forms | planned |
| `connect-project-tools` | Jira, Trello, Redmine, GitHub: read freely, write with approval | planned |
| `unified-calendar` | Every calendar in one agenda, with meeting prep from the vault | planned |
| [`notebooklm-experts`](notebooklm-experts.md) | NotebookLM notebooks as consultable experts, with a knowledge map of what each knows | **ready** |
| [`connect-a-web-app-without-api`](connect-a-web-app-without-api.md) | Use any web app that has no API (a notebook tool, an admin portal, a social media tool your team builds) from your agent: connection ladder, your signed-in browser, a recipe note per app, the bridge rules, a skill around it | **ready** |
| `youtube-knowledge-base` | Followed channels transcribed into a searchable knowledge base | planned |

## Thinking with AI
| Playbook | What you get | Status |
|---|---|---|
| `think-with-several-ais` | One question to several AIs (API and browser), a state file, a synthesis | ready (skill: `skills/think`) |
| `independent-judge` | A second model family that checks the first one's conclusions | ready (kit: `learn-merge/judge.py`) |

## Personal operations
| Playbook | What you get | Status |
|---|---|---|
| [`daily-briefing`](daily-briefing.md) | Today's plan from tasks, calendar and mail | **ready** |
| `email-triage` | Mail sorted into prepared dossiers, nothing sent without you | ready in part (agent: `alfred`) |
| [`capture`](capture.md) | Raw thoughts dropped in, sorted later | **ready** |
| `recap-and-journal` | What you did, from an activity log, weekly | planned |
| `planner-and-timeline` | A priority board and a life timeline generated from your notes | planned |

## People and money
| Playbook | What you get | Status |
|---|---|---|
| `people-notes` | Per-person notes, append-only, across areas | ready in part (agent: `iris`) |
| `household-finance` | Family bookkeeping and a budget sheet | ready in part (agent: `moneto`) |
| `business-finance` | Methodology per organization, analysis, bookkeeping behind a gate | ready in part (agent: `moneto`) |

## Content and media
| Playbook | What you get | Status |
|---|---|---|
| [`meetings`](meetings.md) | Prep, recording, transcript, intake, second pass, archive | **ready** |
| `transcribe` | Audio, video or YouTube to text, with a completeness check | ready (skill: `skills/transcribe`) |
| `podcast` | From episode prep to publishing | ready (pack: `packs/podcast`) |
| `reels-from-video` | Short clips from long video with captions | planned |
| `speed-reading` | A book or article into a structured note | ready (skill: `skills/speed-reader`) |
| `marketing-campaigns` | Campaigns, adapting to platforms, a publishing gate, a publication log | ready in part (agent: `presto`) |
| `language-editing` | Native-quality editing in any language, your rules in `LOCAL.md` | ready (skill: `skills/language-editor`) |

## Views, web and presentations
| Playbook | What you get | Status |
|---|---|---|
| [`build-a-dashboard`](build-a-dashboard.md) | No app, a zero-build view, or a React app on the same API | **ready** |
| `publish-a-microsite` | A small website from your notes, deployed in minutes | planned |
| `presentations` | Slide decks as code, one design system, presented from a link | planned |
| `print-design` | Roll-ups and posters measured in real centimetres, contrast checked | planned |
| `publish-from-your-vault` | Selected views of your vault made public, generated, never hand-edited | planned |
| `measure-your-ai-usage` | How you use your AI tools, per machine and over time | planned |

## Working with others
| Playbook | What you get | Status |
|---|---|---|
| `share-with-your-team` | Publish a vault note to shared tools on purpose; pull shared state back with a date | planned |
| `shared-orchestration` | Several personal systems coordinated on shared tools | planned (concept: `principles/P08`) |
