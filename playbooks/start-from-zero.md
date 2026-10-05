---
title: start-from-zero
date: 2026-10-05
status: active
description: Playbook for a person with no notes system at all, guided by their agent, Obsidian first. Explains in plain words what notes, a vault, Obsidian, Claude and PAROS are; installs Obsidian; creates the vault; opens the agent in it; shows why every area of life belongs in one place; builds a minimal structure only with the person's yes; delivers a first useful result; covers phone, cost, backup, privacy and what happens if they stop.
---

# Playbook: start from zero (Obsidian first)

## Who this is for

Someone who has never kept notes in a system. Their information lives everywhere: desktop files, chat apps, starred emails, a paper notebook, phone notes. They may never have opened a terminal and do not want to. They pasted the link to their agent because someone told them to.

**The test of success** (after the first session the person can say it in their own words):

> My vault is just my folder of notes. Obsidian is how I look at them. PAROS helps Claude work sensibly with those notes. If PAROS disappears, my notes remain.

## How you work in this playbook (rules for the agent)

- **One action per turn.** Give one thing to do, then ask "what do you see now?" and wait. Never five steps at once.
- **No commands for the person to type.** Everything they do is clicking in apps they can see. You may run commands yourself.
- **Translate every term the first time you use it,** in one short sentence. Prefer their words over yours.
- **A first useful result before structure.** No architecture lecture; no list of principles.
- **Every file you create is shown first and created only after a yes** (AGENTS.md, "Every durable write is a small transaction"). A yes to one file is not a yes to another.
- **Keep one form of address** (formal or informal) for the whole relationship, and write it into `PAROS/ADOPTION.md` when you save the session.
- **Do not ask "where is your vault?"** before they have one. Help create it.

## Steps

### 1. Five words, in plain language

Explain, one short paragraph, then check it landed:

- **Notes** are plain text files on your computer. Any program can open them, even Notepad.
- **A vault** is simply a normal folder with those notes in it. Obsidian calls it a "vault" (the word means a safe), but it is just a folder.
- **Obsidian** is a free app, the window through which you read and write your notes comfortably.
- **Claude** (your agent) is the helper that works in that folder with you: it finds things, keeps order, and remembers through files, not through its own memory.
- **PAROS** is the set of rules this helper follows: never change anything without your yes, never delete, learn from your corrections.

### 2. Install Obsidian

- Go to **obsidian.md** and click **Download**; it offers the version for your computer.
- **Windows:** run the downloaded installer. If Windows asks whether to allow it, the publisher should read *Obsidian* or *Dynalist Inc.* (the company behind Obsidian); then say yes.
- **Mac:** open the downloaded file and drag Obsidian into Applications.
- It is free, also for work, and needs no account.

Ask them to tell you when Obsidian has opened and what they see. Do not go on before that.

### 3. Create the vault

Obsidian's welcome screen offers a few choices:

- **Create new vault**: this is the one for a fresh start. Name it (their name, or "Notes" in their language) and choose the location: **Documents**. Avoid a cloud folder (OneDrive, iCloud, Google Drive) for now unless they already want sync; that comes in step 9.
- **Open folder as vault**: use this instead if a notes folder already exists (for example one you created together a minute ago).
- **Open vault from Obsidian Sync** or **Sign in**: not now.

Ask them to read back the vault name and the location. Then check from your side that the folder exists (list it), and say what you see.

### 4. Open your agent inside the vault

The helper can only see what is in the folder its session runs in. From now on, every conversation about notes starts **in the vault folder**:

- **Claude desktop app:** open the **Code** tab, start a new session, and choose the vault folder as the session's folder (the app asks for a folder when a session starts; if they are unsure, ask them to describe what they see and guide them).
- **Terminal users:** `cd` into the vault and start `claude` (only for people who already use a terminal).

If the current session is somewhere else, you can keep helping now, but say clearly that next time they should start in the vault and type `/paros`.

### 5. One place for the whole of life

Explain why everything goes into one vault, in two or three sentences, with an example from what they told you:

> The note about the accountant, the invoice task and next week's plan make sense together. If they live in one place, you do not have to decide each time where something belongs, and the helper can connect them for you.

Then ask about **two to four areas** of their life (work, home, family, health, money, a hobby). Use their words for the folder names. Do not offer a template list; the areas come from their life.

**Private zones:** ask whether anything should never be read by the helper (health, family matters). Offer two options: keep it **outside** the vault, or keep it in one folder that is declared off-limits (an entry-file rule plus `PAROS/.parosignore`, shown and created only with their yes). Say honestly that "off-limits" is a rule the helper follows and the tools enforce where they can; outside the vault is the stronger choice.

### 6. A minimal structure, each piece with a yes

Propose, show, then create one by one:

1. **A task file with an Inbox** (for example `TODO.md` in their language): Inbox, Now, Waiting, Done. The Inbox takes anything, unformatted; sorting is the helper's job.
2. **The area folders** from step 5.
3. **An entry file** (`AGENTS.md`, plus a one-line `CLAUDE.md` pointing to it) with their rules in their language: never send, delete, pay or handle passwords alone; archive instead of delete; existing notes change only with a yes; the private zone, if any.

Explain the header once, when they first see it: the few lines between `---` marks at the top of a file are its "name card" (title, date, one sentence about the content). Obsidian shows it as **Properties**. They never have to touch it.

### 7. The first useful result

- Ask them to tell you one thing they must not forget. Put it into the Inbox (they can watch it appear in Obsidian).
- Sort it into Now, with a question if something is missing (who, by when).
- Then ask them to ask you about it in their own words ("what did I need to do about the accountant?") and answer from the file.
- Show that ticking the checkbox in Obsidian changes the file itself.

### 8. How it will grow (one sentence each, nothing to do now)

- **Weeks:** you drop things into the Inbox; the helper sorts.
- **Months:** each area gets a few real notes and a short "where things stand" note; meeting notes go to the right area.
- **Later:** your mail and calendar can be connected, so the helper prepares your day; the helper learns from your corrections, always shown to you first.

### 9. Phone, cost, backup, stopping

- **Phone:** the simplest path is the **Obsidian mobile app** with **Obsidian Sync** (paid, end-to-end encrypted, works on Android and iPhone). A cloud folder works too (iCloud on Apple devices; on Android it needs extra setup). Do this only once the computer side feels natural.
- **Cost map:** Obsidian is free; Obsidian Sync is optional and paid (check the current price on obsidian.md); your Claude plan is what you already pay for; PAROS is free.
- **Backup:** sync is not backup. Before real data piles up, follow [`sync-and-backup`](sync-and-backup.md).
- **If you stop:** the notes are plain files in your Documents folder; they open in any text editor. Nothing is locked in.

### 10. Save the session, with a yes

Ask: "May I save where we are, so that next time a new session can continue from here?" Only with a yes, create `PAROS/ADOPTION.md`: a short profile in their words (what they use the notes for, devices), decisions made, the form of address, next steps. Then tell them how to come back: open the agent in the vault and type `/paros`.

## Privacy, said accurately

When privacy comes up (and before connecting anything), separate four things:

1. **Your notes stay as ordinary files on your computer.** Nothing is published.
2. **When you ask the helper to work with a note, it has to read it,** and what it reads is sent to the AI service behind it (for Claude: Anthropic) to produce the answer, under the terms of your plan. This is different from publishing.
3. **PAROS gives its maintainers no access to your vault.** A gap report, if you ever agree to send one, contains no personal data and you see it word for word first.
4. **Sync services and connectors are separate again:** your files then also live with that service (for example encrypted with Obsidian Sync), and the helper tells you before using any connector.

## Pitfalls

- Typing instructions for a terminal to someone who has never used one.
- Five steps in one message.
- Explaining markdown, frontmatter or principles before there is a reason to.
- Choosing their areas for them.
- Saying "nothing leaves your computer" when the AI reads the files.
- Creating "helpful" extra files (a log, an archive folder) without asking.

## Principles behind it

[P00](../principles/P00-constitution-and-boundaries.md) (boundaries), [P01](../principles/P01-persistence.md) (plain files you own), [P02](../principles/P02-presentation.md) (the view is replaceable), [P10](../principles/P10-backup-and-recovery.md) (sync is not backup).

## Related

[`organise-your-knowledge`](organise-your-knowledge.md), [`task-inbox`](task-inbox.md), [`capture`](capture.md), [`sync-and-backup`](sync-and-backup.md), the demo vault in [`starter/`](../starter/README.md).
