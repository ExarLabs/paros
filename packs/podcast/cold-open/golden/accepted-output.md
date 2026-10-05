# Cold open #42, variant G (synthetic example)

What was verified: three of six raw cut points were in speech and were moved to measured pauses; every rendered clip was transcribed again and the text below is that re-transcription. The final stack audio `42-G-stack.mp3` (23.6 s) is attached in the chat.

```
EPISODE 42 - COLD OPEN - CUT INSTRUCTIONS

SOURCE FILE: 42-raw.wav  (length 01:23:17,400)
WARNING: all timecodes are measured from the zero point of THIS file.
Your timeline starts 4 s earlier: add 4 s to every value.

TOTAL: 23.6 s, 3 clips, HARD CUT (no fade, no crossfade)

==================================================================
CLIP 1
IN:     00:06:41,200   (401.200 s)
OUT:    00:06:50,620   (410.620 s)
LENGTH: 9.4 s
TEXT:
"A washing machine used to be a thirty-year decision. Now it's a
seven-year subscription you didn't sign."

==================================================================
CLIP 2
IN:     00:07:11,740   (431.740 s)
OUT:    00:07:19,100   (439.100 s)
LENGTH: 7.4 s
TEXT:
"And it's not that they can't build it to last. It's that nobody is
paid to."

==================================================================
CLIP 3
IN:     01:18:02,600   (4682.600 s)
OUT:    01:18:09,450   (4689.450 s)
LENGTH: 6.9 s
TEXT:
"Repair is the cheapest thing you'll ever buy."

==================================================================
ORDER: CLIP 1 > CLIP 2 > CLIP 3
Clip 3 comes from the last minutes of the episode. That is intended.

==================================================================
TRANSITION
- Music and title card: 6 s
- Host introduction: at most 35 s, IN 00:00:12,000 OUT 00:00:47,000
- Cut 00:00:31,000 to 00:00:38,500 from the introduction: it repeats
  the washing machine line from clip 1.

==================================================================
DO NOT CUT IN
- The sentence after clip 2 (00:07:19,100 onward) explains who pays.
  It answers the open loop; it must stay in the episode, not the
  cold open.
- Blocklist: the guest's former employer is never named in the
  cold open.

==================================================================
SUBTITLES
- "seven-year" with a hyphen.
- "nobody is paid to" ends there on purpose; do not complete it.

==================================================================
REFERENCE AUDIO: 42-G-stack.mp3 (23.6 s), this is how it should sound
```

Raw times that were wrong: C2 OUT by 720 ms (cut off "sign"), C5 IN by 560 ms (inside "And"), C9 OUT by 450 ms (inside "buy").
