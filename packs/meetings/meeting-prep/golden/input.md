# Golden example: input (synthetic)

On Monday 2026-10-12 at 20:00 the person says: "Prepare me for tomorrow's repair cafe meeting." `LOCAL.md` is the one in `LOCAL.example.md`; the calendar may be read.

## Calendar entry (read-only)

```
Tue 2026-10-13 19:00 to 19:30, "Repair Cafe check-in", video call
```

## What the vault returns (index first)

### Previous meeting: `Community/Repair Cafe/meetings/2026-09-29-autumn-repair-day.md`

Summary of the accepted note (the full note is the meeting-intake golden example):

- D-7: repair day on Sunday 18 October, library hall (decided).
- Hall: 90, to be paid a week before (2026-10-11); 320 in the account. No owner for the payment.
- Commitments: Tomasz brings soldering station and sewing kit (2026-10-18); Tomasz checks PAT tester calibration (2026-10-10); Ngozi calls the insurer (no date stated); Anya poster and newsletter (2026-10-02).
- Open questions: Q-12 insurance cover for volunteers, including one not signed up yet; Q-13 replace the old sign-up sheet; Q-14 who holds the tool store key while Tomasz is away (11 to 16 October).

Short excerpt of its raw transcript, end:

```
[00:09:31] One thing. Only Tomasz has the key to the tool store, and he's away the week before.
[00:09:44] True, I'm away from the eleventh to the sixteenth. I could leave the key with someone.
[00:10:51] Okay. Next meeting Tuesday the thirteenth, same time. Thanks all, bye.
```

### Task list `TODO.md`, section Repair Cafe

```
- [x] Poster on the community board and to the newsletter (due 2026-10-02) [[2026-09-29-autumn-repair-day]] done 2026-10-01
- [ ] Agree who holds the tool store key before 2026-10-11 [[2026-09-29-autumn-repair-day]]
- [ ] Find an owner for the hall payment (90, by 2026-10-11) [[2026-09-29-autumn-repair-day]]
- [ ] Waiting on Ngozi: insurer's answer on volunteer cover [[2026-09-29-autumn-repair-day]]
- [ ] Waiting on Tomasz: PAT tester calibration check (due 2026-10-10) [[2026-09-29-autumn-repair-day]]
```

### Newer than the last meeting

- `Community/Repair Cafe/inbox.md`, 2026-10-07: "library emailed, hall invoice attached, 90, pay by 11th". Nothing in the vault says it was paid.
- No note mentions the insurer since 2026-09-29.
