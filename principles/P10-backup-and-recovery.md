# P10. Backup: sync is not backup (proposal)

**Principle.** Sync (Obsidian Sync, iCloud, Drive, git across machines) is for being in two places at once; backup is for going back in time. Sync faithfully copies a deletion, a bad agent write or a ransomware-encrypted file to every machine. You need a **one-way, versioned backup that is independent of your machines**, and **a backup only counts once you have restored from it.**

**Why.** In an agent system, fast bulk writing is normal operation; one bad write reaches every machine in minutes.

**Practice.**
- **Back up only what cannot be replaced:** the vault, the secrets bundle and recovery key, session transcripts (the system learns from them), your own media, scripts that exist nowhere else. Rebuildable things (indexes, installed packages, remote repositories) stay out.
- **3-2-1:** three copies, on two kinds of media, one off-site (for example: your live machines, an encrypted snapshot store on another disk, an encrypted store in the cloud). The backup password goes into the secrets mechanism (P07).
- **Test restores** regularly and automatically; the health checks watch the age of the latest snapshot and the success of the test (P11).
- **A one-page recovery guide:** a new machine from zero, from the backup and one passphrase.
- **Watch for sync failures too:** is it alive in both directions (is the other machine's canary fresh), are there silent duplicates inside files, is there unpushed work, is there enough free disk.

**Check.**
- Can you restore the vault to yesterday's state? Have you tried?
- What exists in only one place?

**Adopt.** An encrypted, snapshot-based backup tool (for example restic), scheduled daily, with a local and a cloud target, and a monthly test restore (kit: `kits/backup`, planned).
