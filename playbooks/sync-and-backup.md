---
title: sync-and-backup
date: 2026-10-05
status: active
description: Playbook for keeping a vault available on several devices and safe from loss. Chooses a sync service (Obsidian Sync, iCloud Drive, Google Drive, OneDrive, Dropbox, git) by the person's devices and habits, sets it up, and adds a real backup on top, because sync copies mistakes too. Includes conflict checks and a test restore.
---

# Playbook: keep your vault in sync, and backed up

## What you get

Your notes on every device you use, and a way back in time when something goes wrong. Two different things (P10):
- **Sync** keeps the same notes on several devices, now.
- **Backup** lets you go back to yesterday, last week, or before a mistake. Sync copies a deletion, a bad edit or a ransomware-encrypted file to every device within minutes; a backup is the only thing that does not.

## Before you start

The agent asks you, briefly:
- Which devices do you use (computers, phone, tablet; Windows, Mac, Linux, iOS, Android)?
- Which cloud do you already pay for or use (Apple, Google, Microsoft, Dropbox)?
- Do you need the vault on your phone?
- Is anything in the vault confidential (client data, health, family)?
- Are you comfortable with git, or should it stay invisible?

## Steps

### 1. Choose the sync

| Option | Good for | Watch out for |
|---|---|---|
| **Obsidian Sync** (paid) | the smoothest choice across all devices, including phones; end-to-end encryption; version history per file | merges edits made at the same time on two devices silently: a section can appear twice (see step 4) |
| **iCloud Drive** | Apple-only households (Mac, iPhone, iPad) | Windows support is weak; files can be "offloaded" and missing locally |
| **Google Drive** (desktop app) | people already living in Google; Windows and Mac | the desktop app may stream files instead of keeping them local; set the vault folder to "available offline" |
| **OneDrive** | Microsoft 365 users, Windows | the same online-only risk: mark the vault "always keep on this device" |
| **Dropbox** | mixed devices, reliable desktop sync | phone apps for Obsidian need extra setup |
| **git** (GitHub, GitLab, a private repo) | technical users; full history, works offline, great as a backup layer | not real-time; merge conflicts are explicit; never commit secrets; large media do not belong in it |

The agent recommends **one** sync for daily use, based on your answers. A common, safe combination: **Obsidian Sync (or your cloud drive) for sync, plus git or a snapshot backup for history.**

### 2. Set it up

The agent walks you through the chosen service step by step (you sign in yourself; the agent never handles passwords, P07):
- put the vault folder in the right place (inside the synced folder for cloud drives; a separate local folder for Obsidian Sync);
- make sure files are kept **on the device**, not only in the cloud;
- exclude what should not sync: caches, indexes, `node_modules`, large media (keep media in a separate folder);
- for git: a private repository, a `.gitignore` for caches and secrets, and a commit habit (or a scheduled commit).

### 3. Add a real backup

At least one backup that is **one-way and versioned** (P10):
- **simplest:** the version history of your sync service plus a weekly copy to another disk;
- **better:** a snapshot backup tool (for example restic or your operating system's own backup: Time Machine, File History) to a second disk, daily;
- **best (3-2-1):** three copies, on two kinds of media, one off-site and encrypted.

Back up what cannot be replaced: the vault, your secrets bundle and recovery key (never the secret values in plain text), recordings and media you made, scripts that exist nowhere else. Leave out what can be rebuilt (indexes, installed packages).

### 4. Check sync health now and then

The agent adds small checks (P11) that look at results, not at whether a program runs:
- **is sync alive both ways?** each device writes a tiny marker note; the other device checks it is fresh;
- **silent merge duplicates:** a note with the same section or the whole note twice (a typical sign of two devices editing at once);
- **unpushed work** in git, and **free disk space**.

### 5. Test a restore

A backup counts only once you have restored from it. The agent restores one note from yesterday into a temporary folder and compares it with the live one. Repeat monthly.

## Check that it works

- Edit a note on one device; it appears on the other within minutes.
- Delete a test note, then bring it back from the version history or the backup.
- The health checks show green, and a deliberate duplicate in a test note turns one red.

## Pitfalls

- **"It is in the cloud, so it is backed up."** It is synced. Deleting it deletes it everywhere.
- **Online-only files.** Cloud drives may keep only a placeholder locally; your agent then sees empty or missing notes.
- **Two syncs on one folder** (for example Obsidian Sync and a cloud drive on the same vault). They fight; pick one for sync and use the other as backup.
- **Secrets in the synced vault.** Keep them outside (P07).
- **Huge media in git.** Use a separate media folder with its own backup.

## Principles behind it

[P10](../principles/P10-backup-and-recovery.md) (sync is not backup), [P11](../principles/P11-health-contract.md) (prove it works), [P07](../principles/P07-secrets.md) (secrets outside the vault), [P01](../principles/P01-persistence.md) (plain files you own).

## Related

[`kits/health`](../kits/health/README.md) (sync and backup checks), [`kits/secrets`](../kits/secrets/README.md), [`organise-your-knowledge.md`](organise-your-knowledge.md).
