# Synthetic input

Show: *The Lantern Room* (made up). Episode #42, guest Priya Anand, raw file `42-raw.wav`, length 01:23:17,400. The editor's timeline starts 4 seconds before the file's zero.

Blocklist from the owner at step 0: the guest's former employer is not named.

Variant G (thesis) chosen by the owner after listening to the audio of the top three. Clips from the hook pool, with speech-recognition times:

| Clip | Raw IN | Raw OUT | Transcript text |
|---|---|---|---|
| C2 | 00:06:41,200 | 00:06:49,900 | "A washing machine used to be a thirty-year decision. Now it's a seven-year subscription you didn't sign." |
| C5 | 00:07:12,300 | 00:07:19,100 | "And it's not that they can't build it to last. It's that nobody is paid to." |
| C9 | 01:18:02,600 | 01:18:09,000 | "Repair is the cheapest thing you'll ever buy." |

Waveform check (25 ms windows, level relative to the local peak, quiet floor measured over 3 s):

| Point | Raw | Level | Verdict | Nearest pauses |
|---|---|---|---|---|
| C2 IN | 00:06:41,200 | 3 % | in a pause | keep |
| C2 OUT | 00:06:49,900 | 41 % | **in speech** | 00:06:50,620 (380 ms), 00:06:51,900 (120 ms) |
| C5 IN | 00:07:12,300 | 28 % | **in speech** | 00:07:11,740 (450 ms) |
| C5 OUT | 00:07:19,100 | 5 % | in a pause | keep |
| C9 IN | 01:18:02,600 | 4 % | in a pause | keep |
| C9 OUT | 01:18:09,000 | 19 % | **in speech** | 01:18:09,450 (600 ms) |

Re-transcription of the rendered clips, first render with raw times:

- C2: "...thirty-year decision. Now it's a seven-year subscription you didn't" (last word cut off)
- C5: "it's not that they can't build it to last..." (the opening "And" is missing; acceptable, but the cut is inside a word on the waveform)

Second render with corrected times: all three clips re-transcribe as whole sentences.
