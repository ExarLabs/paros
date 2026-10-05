# Kit: reels (P01 and P11, short captioned clips from a long video)

A working reference for turning a long video (a podcast episode, a talk, a recorded class) into short vertical clips with burned-in captions, a title card and an outro. One script, `reel.py`, built on `ffmpeg` and `yt-dlp`, plus the working rules that keep a burned-in caption from saying something the speaker never said.

Optional. Read it, then rebuild or adapt it for the vault.

## Why your own pipeline

Clip services are fast, but three things go wrong with them, all seen in practice:

- **They invent.** An AI clipping tool put a title on a clip that named the wrong family member; nothing in the recording said it. Burned-in text is irreversible once published.
- **They mishear.** Speech recognition is very good on average and wrong exactly where it matters: names, rare words, emotional sentences. One misheard sentence turned "I saw her then for the last time" into a phrase with a different meaning and a different person in it.
- **They lose quality and control.** A pipeline you own keeps the source resolution, costs nothing per clip, and runs the same way every time.

A visual tool is still fine for **finding** moments. The rendering and the words are yours.

## The working rules

These are the procedure. The agent applies them without being asked.

1. **The full transcript is the ground truth.** Before any clip, get the checked transcript of the whole video (SRT). Captions are sliced from it, the title is written from it, the description comes from it. If there is none, ask for it. Running speech recognition on the clip is a fallback, and its output is read line by line before anything is burned in.
2. **Review the captions before `compose`.** List the suspicious places with a proposed fix: names, near-homophones, compounds that make no sense, a word that changes the meaning. The owner decides. Only then compose.
3. **The title comes from the transcript and gets its own review.** Never copy a title an AI tool generated. Prefer a short, real quote from the clip.
4. **Choose the clip by its hook.**
   - The first 1 to 3 seconds stop the scroll on their own.
   - It stands alone: no need for the rest of the episode to understand it.
   - The ending loops back to the opening if it can.
   - Length: about 13 seconds for a punchy reveal, or about 60 seconds for a story or a method. The 30 to 45 second middle tends to underperform.
   - Something changes on screen at least every 3 seconds (a cut in the source, a caption, a zoom).
   - From one episode, the strongest hook goes out first; the rest follow two or three days apart.
5. **Cut at transcript block boundaries.** If the next caption block overlaps the clip end by a few hundredths of a second, it becomes a garbage fragment. `extract-subs` drops edge slivers under 0.15 s and tells you; move `--start` or `--end` to a boundary when it matters.
6. **Scratch outside the vault, deliverables in the area.** Source files are gigabytes; keep the working folder outside the synced vault (`PAROS_REEL_SCRATCH`, default `~/reels-scratch`). The finished clip and its `PUBLISH.md` go into the folder of the area it belongs to (for example `<area>/<episode>/Clips/<slug>/`), never into the kit's folder.
7. **Every `PUBLISH.md` has a "Short description":** one or two platform-neutral sentences on what the clip shows, next to the per-platform copy.
8. **Life cycle questions.** When all clips from a source are done, ask before deleting the source video (state its size; it can be downloaded again). When everything is published, ask whether to archive the deliverable folder (recommended: the publishing copy is useful later) or delete the video.
9. **Publishing is the owner's.** The kit prepares; it never uploads (P00).
10. **After a non-trivial run, write down what you learned** (a new failure, a better default) in the kit's `LEARNINGS.md` in your vault, or as a learning packet (P05).

## Setup

- `ffmpeg` and `ffprobe` on PATH.
- `yt-dlp` (`python -m pip install -U yt-dlp`) for downloads.
- Pillow (`pip install pillow`) for the title card.
- Optional fallback: `openai-whisper`, or any transcription you trust (see the `transcribe` skill).
- `python reel.py check` lists what was found.
- Copy [`LOCAL.example.md`](LOCAL.example.md) to `LOCAL.md` in your vault and set your theme (fonts, colours, outro, hashtags). `reel.py --theme LOCAL.md` reads its `json` block.

## Commands

```bash
python reel.py check
python reel.py download URL --out ~/reels-scratch/ep12/source.mp4 --until 14:00
python reel.py clip SOURCE --start 12:34 --end 13:22 --out clip.mp4
python reel.py reframe clip.mp4 --aspect 9:16 --out reframed.mp4        # or 9:16-fill, 1:1, 1:1-fill
python reel.py extract-subs full-episode.srt --start 12:34 --end 13:22 --out subs.srt
#   review subs.srt now (rule 2)
python reel.py --theme LOCAL.md title "A real quote from the clip" --out title.png   # preview
python reel.py --theme LOCAL.md compose reframed.mp4 --subs subs.srt --title "A real quote" --out reel.mp4
python reel.py publish reel.mp4 --dest "<area>/<episode>/Clips" --slug clip-01-topic --title "A real quote"
python reel.py probe-frame reel.mp4 --frame 120 --out check.png         # look at an exact frame

# all at once: stops before compose so the captions get reviewed; rerun with --yes
python reel.py --theme LOCAL.md full URL --slug ep12-topic-01 --start 12:34 --end 13:22 \
    --full-srt full-episode.srt --title "A real quote"
```

`--dry-run` before the subcommand prints every command and runs nothing. Debug step by step: when one step fails, rerun only that step, not `full`.

## What each step does

| Step | Default | Why |
|---|---|---|
| `download` | best mp4 up to 1080p; `--until T` fetches 0:00 to T only | a section download of a long 4K episode took 5 MB and under a minute instead of over a gigabyte |
| `clip` | output seek, re-encode CRF 18 | frame accurate |
| `reframe` | 9:16 with a blurred copy behind the original | works for any source; `-fill` crops to cover, for a single centred speaker |
| `extract-subs` | slice, shift to 0, fragments of at most 3 words | short pulses read while scrolling; a sentence does not |
| `compose` | captions, title card faded in and out, optional music at 0.15, outro appended | one ffmpeg pass plus a stream-copy join |
| `publish` | `<dest>/<slug>/` with the video and `PUBLISH.md` | the deliverable lives with the work it belongs to |

## Pitfalls (measured)

- **Keyframe snapping.** `-ss` before `-i` jumps to the previous keyframe: a cut meant for 36.65 s began on a frame of the speaker, not the outro. Put `-ss` after `-i` (output seek) for exact cuts.
- **Probing frames lies the same way.** `ffmpeg -ss N -i SRC -frames:v 1` also snaps. To find an exact boundary use `select=eq(n,N)` (`probe-frame`). A transition located this way sat between frame 917 and 918.
- **Section downloads must start at 0:00.** A section starting later resets the file's timestamps, and every clip and caption offset is then wrong.
- **Joining the outro.** The concat *filter* failed with an invalid-argument error on streams that were identical; the concat *demuxer* with stream copy worked and took well under a second instead of several. The demuxer requires matching size, frame rate and codecs: encode the outro once to match your reels. The script warns when they differ.
- **A faded still image disappears.** A fade on a single PNG frame leaves alpha near zero after the first frame. Feed the title as a looped clip (`-loop 1 -framerate 30 -t 3.5`) and overlay with `eof_action=pass`.
- **Subtitle sizes are not pixels.** Without an `.ass` header libass uses a 288-line script height, scaled to the video: on 1920 px, `Fontsize=18` is about 120 px and `MarginV=70` is about 466 px from the bottom. `Fontsize=14` with full sentences wrapped into three or four lines; `MarginV=180` sat on the speaker's face.
- **Converting captions to `.ass` broke the layout** (no wrapping, wrong size) until the play resolution and wrap style matched the old `force_style` geometry exactly. Keep `force_style` unless you need per-word effects.
- **Windows paths in the subtitles filter.** The drive colon breaks the filter's argument parsing. The script copies inputs into the work folder and uses bare file names.
- **Windows console encoding.** Non-ASCII output crashes a cp1252 console; the script switches to UTF-8 at start. Whisper's own printing died on accented letters and then silently skipped writing the SRT; the fallback sets `PYTHONIOENCODING=utf-8` for it.
- **Whisper on a GPU** failed with "no kernel image is available" when the installed PyTorch build did not match the card. The fallback runs on CPU by default (`--device cuda` to try).
- **Missing title font.** If none of the theme's `font_candidates` exists (different OS), Pillow falls back to a tiny bitmap font. List paths for every OS you use.
- **Light captions on a bright blurred background** stay hard to read with an outline alone. A dark box behind the line (`BorderStyle=3` or a box in a code-native renderer) and a slight overall tint work.
- **The title must be the largest text on screen.** A small title above huge captions reads as a footnote.
- **Fill reframe on a two-person wide shot** shows the empty middle of the table. Use fill only for a single centred speaker until you have face tracking.
- **A focused range must apply to every step.** A tool that limited frame extraction to a range but still transcribed the whole 1 h 44 min episode spent over twenty minutes on CPU. Cut the audio too.
- **Sensitive subjects.** For grief or illness, avoid jump cuts on silences and loud colours; the tone matters more than retention tricks.

## Upgrades, when you need them

- **Word-level timing.** Caption timing here is proportional to word count, which can drift over a second from the voice. The proven fix is *baseline plus overlay*: keep the words from the transcript, run a word-timestamp recognizer (for example faster-whisper) on the clip audio only for timing, align the two word lists (difflib), take the measured time where words match and the proportional time elsewhere, and fall back entirely when under half the words align. Measured: average offset 0.37 s, maximum 1.6 s, all words kept. Run the recognizer as a separate process if it needs a different Python version.
- **A code-native renderer** (Revideo, Remotion) for karaoke highlighting, a gentle punch-in zoom on the footage only (captions stay still, scale never below 1.0), and caption pops timed from each word's own length.
- **Face tracking** for the fill reframe.

## Principles

- **P01, retrieve, do not recall.** The checked transcript is the record; recognition output and AI titles are claims to verify against it.
- **P11, look at the output.** Probe exact frames, read every caption, watch the result before calling it done.
- **P00, prepare, never publish.** The deliverable is "prepared"; the owner uploads.
- **Capability holds templates, the area holds the work.** Scripts and theme are reusable; each clip lives with its episode.
