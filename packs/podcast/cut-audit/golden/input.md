# Synthetic input

Show: *The Lantern Room* (made up). Episode #44, "Twelve habits for a calmer week", host only, raw recording 01:31:05. An earlier, unchecked audit made four claims. Its transcript was not saved, so a new one was made and saved in `transcript/44-raw.srt`.

Earlier audit's claims:

1. "The host says twelve habits, but there are thirteen segments."
2. "About six minutes can be cut: the morning-walk story appears twice (00:14:10 and 00:52:30)."
3. "A 5.8 second silence at 00:41:02 should be cut."
4. "The sentence at 01:12:40 is unfinished and needs a pickup."

What the new checks found:

- Segments: the thirteenth "segment" at 00:47:15 is the sentence "The next few are about evenings." It introduces habits 7 to 9.
- 00:52:30: "Remember the morning walk from habit two? This is the evening version." The second telling adds what changed after a month.
- Silence: `silencedetect=noise=-30dB:d=1.0` finds no silence near 00:41:02; the longest pause within 30 seconds is 0.9 s. The transcript has no gap there.
- 01:12:40: the sentence continues after a 1.2 s pause and ends at 01:12:47. The audio confirms it.
- Real repetition found: the same three-sentence definition of "a calm week" at 00:03:40 and again at 01:05:12, with nothing added. About 40 seconds.
- Upload check: the uploaded video is 01:31:05 long, and its subtitles match the raw transcript at 00:01:00, 00:45:30 and 01:26:00. The raw recording is what was uploaded.
