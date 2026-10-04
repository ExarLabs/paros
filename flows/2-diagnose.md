# Flow 2: Diagnosis

Goal: an honest picture of where the vault stands, principle by principle, with evidence. **Read-only.** Nothing in the vault changes, except that the result is written to `PAROS/DIAGNOSIS.md` at the end (ask first).

## Steps

1. **Measure.** Run the scanner from the vault root (Python 3.8+, no dependencies):
   ```bash
   python <path-to-paros>/tools/diagnose.py . --json PAROS/diagnosis.json
   ```
   It measures what can be measured without judgment: file counts, frontmatter and description coverage, entry files, skills and agents, learning files, archive, version control and sync, secret-like patterns (names only, never values), possible sync duplicates. If Python is not available, do the same checks by hand with the file tools you have.
2. **Ask** what cannot be measured. Keep it short, at most five questions, for example:
   - Which areas of your life and work does this vault cover?
   - How many machines do you use it on, and how does it sync?
   - Which external tools do you use daily (mail, calendar, tasks, CRM)?
   - Which agent platform do you use?
   - What annoys you most about working with your notes today? (This is the friction PAROS should remove first.)
3. **Judge.** For each principle, read its **Check** section and give a maturity level, with one line of evidence:

   | Level | Meaning |
   |---|---|
   | 0 | Not present |
   | 1 | Started: some pieces exist, not consistent |
   | 2 | In place: works for most of the vault |
   | 3 | Self-sustaining: checked automatically, improves with use |

   Also mark each principle `now`, `later` or `not needed` for this person (connectors can wait if they use no external tools; backup is never `not needed`).
4. **Write** `PAROS/DIAGNOSIS.md` (template: `templates/DIAGNOSIS.md`): date, reference version, the table, the three biggest gaps, and the one change that would remove the most friction.
5. **Present** the result in a few lines in the chat: a small text map (one line per principle, level as blocks, for example `P01 Persistence  ██░  2`), the biggest gaps, and the suggested first step. Then offer the personal guide (flow 3) or going straight to adoption (flow 4).

## Rules

- Never print or store a secret value; the scanner reports file and pattern type only.
- Say what you measured and what you assumed. A diagnosis is evidence, not an impression.
- Repeat the diagnosis after adoption steps; the change in levels over time is the person's progress.
