#!/usr/bin/env python3
"""reel.py: long video to short captioned clips (PAROS kit: reels).

Subcommands (each step runs alone, which is how you debug it):
  check                                          which tools are available
  download URL --out F [--until T]               yt-dlp; --until fetches 0:00..T only
  clip SRC --start T --end T --out F             frame-accurate trim (output seek)
  reframe SRC --aspect 9:16 --out F              vertical or square, blurred bars or fill
  extract-subs FULL_SRT --start T --end T --out F
                                                 slice the full transcript, shift to 0,
                                                 split into short caption fragments
  transcribe SRC --out F                         local Whisper, FALLBACK only
  title TEXT --out F.png                         render the title card (preview it)
  compose VIDEO --subs F [--title T] [--music M] [--outro O] --out F
                                                 burn captions, fade the title, mix music,
                                                 append the outro
  probe-frame SRC --frame N --out F.png          extract exactly frame N
  full URL --slug S --start T --end T --full-srt F [--title T]
  publish REEL --dest DIR --slug S               deliverable folder plus PUBLISH.md

Global options: --theme FILE (a .json, or a LOCAL.md with a ```json block),
--dry-run (print the commands, run nothing). Scratch folder: $PAROS_REEL_SCRATCH
(default ~/reels-scratch), outside the synced vault.

Needs ffmpeg and ffprobe; yt-dlp for download; Pillow for the title card;
openai-whisper only for the transcribe fallback.
"""
from __future__ import annotations

import argparse
import copy
import datetime
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass

DRY = False

# A neutral default theme. Your brand lives in LOCAL.md (see LOCAL.example.md).
# Subtitle sizes are in libass units: without an .ass header the script height
# is 288, scaled to the video (1920 / 288 = 6.67), so Fontsize 18 is about 120 px
# and MarginV 70 is about 466 px above the bottom edge.
DEFAULT_THEME = {
    "subtitle_style": ("Fontname=Arial,Fontsize=18,Bold=1,PrimaryColour=&H00FFFFFF,"
                       "OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=2,"
                       "Alignment=2,MarginV=70"),
    "max_words_per_fragment": 3,
    "title": {
        "font_candidates": [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/Library/Fonts/Arial Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
        ],
        "font_size": 80,
        "max_width": 940,
        "padding": [30, 46],
        "radius": 28,
        "line_gap": 8,
        "bg_rgba": [20, 32, 54, 230],
        "text_rgb": [245, 241, 233],
        "top_frac": 0.07,
        "duration": 3.5,
        "fade_in": 0.3,
        "fade_out": 0.4,
    },
    "fps": 30,
    "outro": None,
    "music_volume": 0.15,
    "hashtags": "",
}

REFRAME = {
    "9:16": (1080, 1920, "blur"), "1:1": (1080, 1080, "blur"),
    "9:16-fill": (1080, 1920, "fill"), "1:1-fill": (1080, 1080, "fill"),
}


# --- helpers ------------------------------------------------------------------

def run(cmd: list[str], cwd: Path | None = None, env_extra: dict | None = None) -> None:
    print("\n$ " + " ".join(shlex.quote(str(c)) for c in cmd) + (f"   (in {cwd})" if cwd else ""))
    if DRY:
        return
    env = dict(os.environ, **env_extra) if env_extra else None
    r = subprocess.run([str(c) for c in cmd], cwd=cwd, env=env)
    if r.returncode != 0:
        sys.exit(f"FAILED: exit {r.returncode}")


def load_theme(path: str | None) -> dict:
    theme = copy.deepcopy(DEFAULT_THEME)
    path = path or os.environ.get("PAROS_REEL_THEME")
    if not path:
        return theme
    text = Path(path).expanduser().read_text(encoding="utf-8")
    if not path.endswith(".json"):
        m = re.search(r"```json\s*\n(.*?)\n```", text, re.S)
        if not m:
            sys.exit(f"ERROR: no ```json block found in {path}")
        text = m.group(1)
    user = json.loads(text)
    for k, v in user.items():
        if isinstance(v, dict) and isinstance(theme.get(k), dict):
            theme[k].update(v)
        else:
            theme[k] = v
    return theme


def scratch_root() -> Path:
    return Path(os.environ.get("PAROS_REEL_SCRATCH", str(Path.home() / "reels-scratch"))).expanduser()


def ts_to_s(ts: str) -> float:
    ts = ts.strip().replace(",", ".")
    parts = ts.split(":")
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    if len(parts) == 2:
        return int(parts[0]) * 60 + float(parts[1])
    return float(ts)


def s_to_srt(t: float) -> str:
    t = max(t, 0.0)
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def probe(path: Path) -> dict:
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
                                   "stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate",
                                   "-of", "json", str(path)])
    return json.loads(out)


# --- SRT ----------------------------------------------------------------------

def parse_srt(text: str) -> list[dict]:
    text = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    out = []
    for block in text.strip().split("\n\n"):
        lines = [ln for ln in block.split("\n") if ln.strip()]
        i = next((k for k, ln in enumerate(lines) if "-->" in ln), None)
        if i is None:
            continue
        a, b = [p.strip() for p in lines[i].split("-->")]
        out.append({"start": ts_to_s(a), "end": ts_to_s(b.split()[0]),
                    "text": "\n".join(lines[i + 1:])})
    return out


def slice_srt(entries: list[dict], start: float, end: float) -> list[dict]:
    out = []
    for e in entries:
        if e["end"] <= start or e["start"] >= end:
            continue
        s, t = max(e["start"], start) - start, min(e["end"], end) - start
        if t > s:
            out.append({"start": s, "end": t, "text": e["text"]})
    return out


def fragment(entries: list[dict], max_words: int) -> list[dict]:
    """Split each entry into chunks of at most max_words, timing proportional
    to word count. Short pulses read while scrolling; a full sentence does not."""
    if max_words <= 0:
        return entries
    out = []
    for e in entries:
        words = " ".join(e["text"].split()).split()
        if len(words) <= max_words:
            out.append({**e, "text": " ".join(words)})
            continue
        dur, n = e["end"] - e["start"], len(words)
        for i in range(0, n, max_words):
            chunk = words[i:i + max_words]
            out.append({"start": e["start"] + dur * i / n,
                        "end": e["start"] + dur * (i + len(chunk)) / n, "text": " ".join(chunk)})
    return out


def write_srt(entries: list[dict], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    blocks = [f"{i}\n{s_to_srt(e['start'])} --> {s_to_srt(e['end'])}\n{e['text']}\n"
              for i, e in enumerate(entries, 1)]
    out.write_text("\n".join(blocks), encoding="utf-8")


def cmd_extract_subs(full_srt: Path, start: str, end: str, out: Path, max_words: int,
                     min_tail: float) -> None:
    s, e = ts_to_s(start), ts_to_s(end)
    entries = slice_srt(parse_srt(full_srt.read_text(encoding="utf-8")), s, e)
    # A block that overlaps the clip end by a few hundredths of a second becomes
    # a garbage micro fragment. Drop slivers under min_tail at the edges.
    dropped = [x for x in entries if x["end"] - x["start"] < min_tail]
    entries = [x for x in entries if x["end"] - x["start"] >= min_tail]
    frags = fragment(entries, max_words)
    if DRY:
        print(f"  [dry run] would write {len(frags)} caption fragments to {out}")
        return
    write_srt(frags, out)
    print(f"  wrote {len(frags)} caption fragments to {out}")
    for d in dropped:
        print(f"  dropped a {d['end'] - d['start']:.2f}s sliver at the clip edge: {d['text'][:50]!r} "
              "(move --start/--end to a block boundary if it matters)")


# --- steps --------------------------------------------------------------------

def cmd_check() -> None:
    for tool in ("ffmpeg", "ffprobe", "yt-dlp", "whisper"):
        print(f"  {tool:<8} {'found' if shutil.which(tool) else 'missing'}")
    try:
        import PIL  # noqa: F401
        print("  Pillow   found")
    except ImportError:
        print("  Pillow   missing (needed for the title card: pip install pillow)")
    print(f"  scratch  {scratch_root()}")


def cmd_download(url: str, out: Path, until: str | None, max_height: int) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    fmt = (f"bv*[height<={max_height}][ext=mp4]+ba[ext=m4a]/"
           f"b[height<={max_height}][ext=mp4]/bv*[height<={max_height}]+ba/b")
    cmd = ["yt-dlp", "-f", fmt, "--merge-output-format", "mp4", "-o", str(out)]
    if until:
        # Always from 0:00: the file then keeps the original timeline, so the
        # clip and caption offsets stay identical to the full transcript's.
        cmd += ["--download-sections", f"*0:00-{until}"]
    run(cmd + [url])


def cmd_clip(src: Path, start: str, end: str, out: Path) -> None:
    # -ss AFTER -i: output seek, decodes from the start and is frame accurate.
    # -ss before -i snaps to the previous keyframe and pulls in earlier frames.
    run(["ffmpeg", "-y", "-i", src, "-ss", start, "-to", end,
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "aac", "-b:a", "192k", out])


def cmd_reframe(src: Path, aspect: str, out: Path) -> None:
    w, h, mode = REFRAME[aspect]
    if mode == "fill":
        flt = f"[0:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
    else:
        flt = (f"[0:v]split=2[bg][fg];[bg]scale={w}:{h}:force_original_aspect_ratio=increase,"
               f"crop={w}:{h},boxblur=20:5,eq=brightness=-0.10[bgb];[fg]scale={w}:-2[fgs];"
               "[bgb][fgs]overlay=(W-w)/2:(H-h)/2")
    run(["ffmpeg", "-y", "-i", src, "-filter_complex", flt,
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "copy", out])


def cmd_transcribe(src: Path, lang: str, model: str, device: str, out: Path) -> None:
    print("NOTE: fallback only. A checked full transcript is the ground truth; "
          "read every line of this output before burning it in.")
    out.parent.mkdir(parents=True, exist_ok=True)
    run(["whisper", src, "--language", lang, "--model", model, "--device", device,
         "--output_format", "srt", "--output_dir", out.parent],
        env_extra={"PYTHONIOENCODING": "utf-8"})
    produced = out.parent / (src.stem + ".srt")
    if not DRY and produced != out:
        produced.replace(out)


def _font(theme: dict, size: int):
    from PIL import ImageFont
    for p in theme["title"]["font_candidates"]:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    print("[warn] no title font found from the theme's font_candidates; using a tiny bitmap font")
    return ImageFont.load_default()


def render_title(text: str, out: Path, theme: dict) -> None:
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        sys.exit("ERROR: the title card needs Pillow: pip install pillow")
    t = theme["title"]
    font = _font(theme, t["font_size"])
    pad_y, pad_x = t["padding"]
    words, lines, cur = text.split(), [], []
    for w in words:
        test = " ".join(cur + [w])
        bb = font.getbbox(test)
        if bb[2] - bb[0] <= t["max_width"] - 2 * pad_x or not cur:
            cur.append(w)
        else:
            lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    ref = font.getbbox("ÁgyÉq")  # tall caps plus descenders, for a stable line height
    line_h = ref[3] - ref[1] + t["line_gap"]
    text_w = max(font.getbbox(ln)[2] - font.getbbox(ln)[0] for ln in lines)
    box_w, box_h = text_w + 2 * pad_x, line_h * len(lines) + 2 * pad_y - t["line_gap"]
    img = Image.new("RGBA", (box_w, box_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([(0, 0), (box_w - 1, box_h - 1)], radius=t["radius"], fill=tuple(t["bg_rgba"]))
    y = pad_y - ref[1]
    for ln in lines:
        bb = font.getbbox(ln)
        d.text(((box_w - (bb[2] - bb[0])) // 2 - bb[0], y), ln, font=font, fill=tuple(t["text_rgb"]))
        y += line_h
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG")
    print(f"  title card {box_w}x{box_h} -> {out}")


def append_outro(main: Path, outro: Path, out: Path) -> None:
    """Concat demuxer with stream copy: fast and frame exact, but only when both
    files share resolution, frame rate and codecs. The concat FILTER failed with
    EINVAL on identical streams in practice; prefer the demuxer."""
    if not DRY:
        try:
            a, b = probe(main), probe(outro)
            key = lambda p: sorted((s["codec_type"], s.get("codec_name"), s.get("width"), s.get("height"),
                                    s.get("r_frame_rate"), s.get("sample_rate")) for s in p["streams"])
            if key(a) != key(b):
                print("[warn] the outro's streams differ from the reel's (size, fps or codec). "
                      "Re-encode the outro once to match, or the joined file may stutter or fail.")
        except Exception:  # noqa: BLE001
            pass
    lst = main.parent / "_concat.txt"
    if not DRY:
        lst.write_text(f"file '{main.resolve().as_posix()}'\nfile '{outro.resolve().as_posix()}'\n",
                       encoding="utf-8")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
         "-movflags", "+faststart", out])
    if not DRY:
        lst.unlink(missing_ok=True)


def cmd_compose(video: Path, subs: Path | None, title: str | None, music: Path | None,
                outro: Path | None, out: Path, theme: dict) -> None:
    """One ffmpeg pass. Inputs are staged into the work folder and referenced by
    bare file name, because a Windows drive colon breaks the subtitles filter."""
    work = video.parent
    t = theme["title"]
    if not DRY:
        shutil.copy(video, work / "stage_in.mp4")
        if subs:
            shutil.copy(subs, work / "stage_subs.srt")
    cmd = ["ffmpeg", "-y", "-i", "stage_in.mp4"]
    parts, v, n = [], "[0:v]", 1
    m_idx = t_idx = None
    if music:
        cmd += ["-stream_loop", "-1", "-i", str(music.resolve())]
        m_idx, n = n, n + 1
    if title:
        render_title(title, work / "stage_title.png", theme) if not DRY else None
        # A still image with a fade must be a looped CLIP: a fade on a single
        # PNG frame leaves alpha near zero and the title disappears.
        cmd += ["-loop", "1", "-framerate", str(theme["fps"]), "-t", str(t["duration"]),
                "-i", "stage_title.png"]
        t_idx, n = n, n + 1
    if subs:
        parts.append(f"{v}subtitles=filename='stage_subs.srt':force_style='{theme['subtitle_style']}'[vs]")
        v = "[vs]"
    if title:
        fo_start = max(t["duration"] - t["fade_out"], 0)
        parts.append(f"[{t_idx}:v]format=rgba,fade=t=in:st=0:d={t['fade_in']}:alpha=1,"
                     f"fade=t=out:st={fo_start}:d={t['fade_out']}:alpha=1[ti]")
        parts.append(f"{v}[ti]overlay=x=(W-w)/2:y=H*{t['top_frac']}:eof_action=pass[vt]")
        v = "[vt]"
    a = "0:a"
    if music:
        parts.append(f"[{m_idx}:a]volume={theme['music_volume']},afade=t=in:st=0:d=0.5[bg]")
        parts.append("[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2[aout]")
        a = "[aout]"
    if parts:
        cmd += ["-filter_complex", ";".join(parts), "-map", v if v != "[0:v]" else "0:v", "-map", a]
    cmd += ["-r", str(theme["fps"]), "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "stage_out.mp4"]
    run(cmd, cwd=work)
    staged = work / "stage_out.mp4"
    if outro:
        append_outro(staged, outro, out)
    elif not DRY:
        staged.replace(out)
    if not DRY:
        for f in ("stage_in.mp4", "stage_out.mp4"):
            (work / f).unlink(missing_ok=True)
    print(f"\n  reel -> {out}")


def cmd_probe_frame(src: Path, frame: int, out: Path) -> None:
    # select=eq(n,N) decodes every frame and keeps exactly frame N.
    # "-ss T -i SRC -frames:v 1" snaps to a keyframe and lies about the boundary.
    run(["ffmpeg", "-y", "-i", src, "-vf", f"select=eq(n\\,{frame})", "-vsync", "0",
         "-frames:v", "1", out])


PUBLISH_TEMPLATE = """\
---
title: {slug}
date: {date}
status: prepared
description: A short captioned clip prepared for publishing, with the source, the title card text and per-platform copy; captions come from the checked full transcript.
---

# {slug}

> **Status:** prepared, not published. The owner publishes.

## Short description

<One or two platform-neutral sentences: what the clip shows. Required.>

## Source

- **Episode or video:** {episode}
- **Clip range:** {clip_range}
- **Title card:** {title}

## Video

`{video}` in this folder.

## Short-form platforms (vertical feeds)

**Caption:**
```
<fill in>
```

**Hashtags:**
```
{hashtags}
```

## Video platform shorts

**Title:**
```
<fill in>
```

**Description:**
```
<fill in>
```

## Checklist

- [ ] Platform 1
- [ ] Platform 2
- [ ] Platform 3

After publishing: archive this folder (the publishing copy is worth keeping) or delete the video file.
"""


def cmd_publish(reel: Path, dest: Path, slug: str, title: str, episode: str, clip_range: str,
                theme: dict) -> None:
    folder = dest / slug
    video = folder / f"{slug}.mp4"
    print(f"  deliverable folder: {folder}")
    if DRY:
        return
    folder.mkdir(parents=True, exist_ok=True)
    shutil.copy(reel, video)
    pub = folder / "PUBLISH.md"
    if pub.exists():
        print(f"  {pub} exists, left untouched")
    else:
        pub.write_text(PUBLISH_TEMPLATE.format(
            slug=slug, date=datetime.date.today().isoformat(), episode=episode or "<episode>",
            clip_range=clip_range or "<start-end>", title=title or "<title card>",
            video=video.name, hashtags=theme.get("hashtags") or "<hashtags>"), encoding="utf-8")
        print(f"  scaffolded {pub}")


def cmd_full(a, theme: dict) -> None:
    wd = scratch_root() / a.slug
    if not DRY:
        wd.mkdir(parents=True, exist_ok=True)
    src, clip, vert, subs = wd / "source.mp4", wd / "clip.mp4", wd / "reframed.mp4", wd / "subs.srt"
    final = wd / f"reel-{a.slug}.mp4"
    if not src.exists() or a.force:
        cmd_download(a.url, src, a.until or a.end_pad, a.max_height)
    else:
        print(f"[skip] {src} exists (use --force to download again)")
    cmd_clip(src, a.start, a.end, clip)
    cmd_reframe(clip, a.aspect, vert)
    if a.full_srt:
        cmd_extract_subs(a.full_srt, a.start, a.end, subs, theme["max_words_per_fragment"], a.min_tail)
    else:
        cmd_transcribe(vert, a.lang, a.model, a.device, subs)
    if not a.yes:
        print(f"\nSTOP: read {subs} line by line before burning it in (names, near-homophones, "
              "nonsense compounds). Then run compose, or rerun full with --yes.")
        return
    cmd_compose(vert, subs, a.title, a.music, _outro(a.outro, theme), final, theme)


def _outro(arg: str | None, theme: dict) -> Path | None:
    val = arg if arg is not None else theme.get("outro")
    if not val or str(val).lower() == "none":
        return None
    p = Path(val).expanduser()
    if not p.exists() and not DRY:
        print(f"[warn] outro {p} not found, skipping it")
        return None
    return p


# --- CLI ----------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="reel", description="Long video to short captioned clips.")
    p.add_argument("--theme", help="theme .json, or LOCAL.md containing a ```json block")
    p.add_argument("--dry-run", action="store_true", help="print the commands, run nothing")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", help="which tools are available")
    x = sub.add_parser("download", help="yt-dlp, from 0:00 to --until (or the whole video)")
    x.add_argument("url"); x.add_argument("--out", type=Path, required=True)
    x.add_argument("--until", help="download 0:00..UNTIL only, for example 12:30")
    x.add_argument("--max-height", type=int, default=1080)
    x = sub.add_parser("clip", help="frame-accurate trim")
    x.add_argument("src", type=Path); x.add_argument("--start", required=True)
    x.add_argument("--end", required=True); x.add_argument("--out", type=Path, required=True)
    x = sub.add_parser("reframe", help="vertical or square")
    x.add_argument("src", type=Path); x.add_argument("--aspect", default="9:16", choices=list(REFRAME))
    x.add_argument("--out", type=Path, required=True)
    x = sub.add_parser("extract-subs", help="slice the full transcript for the clip")
    x.add_argument("full_srt", type=Path); x.add_argument("--start", required=True)
    x.add_argument("--end", required=True); x.add_argument("--out", type=Path, required=True)
    x.add_argument("--max-words", type=int, help="words per caption fragment (theme default 3, 0 = off)")
    x.add_argument("--min-tail", type=float, default=0.15, help="drop edge slivers shorter than this (s)")
    x = sub.add_parser("transcribe", help="local Whisper to SRT (fallback only)")
    x.add_argument("src", type=Path); x.add_argument("--out", type=Path, required=True)
    x.add_argument("--lang", default="English"); x.add_argument("--model", default="medium")
    x.add_argument("--device", default="cpu", choices=["cpu", "cuda"])
    x = sub.add_parser("title", help="render the title card PNG for a preview")
    x.add_argument("text"); x.add_argument("--out", type=Path, required=True)
    x = sub.add_parser("compose", help="captions, title, music, outro")
    x.add_argument("video", type=Path); x.add_argument("--subs", type=Path)
    x.add_argument("--title"); x.add_argument("--music", type=Path)
    x.add_argument("--outro", help="outro mp4, or 'none' (default: the theme's)")
    x.add_argument("--out", type=Path, required=True)
    x = sub.add_parser("probe-frame", help="extract exactly frame N")
    x.add_argument("src", type=Path); x.add_argument("--frame", type=int, required=True)
    x.add_argument("--out", type=Path, required=True)
    x = sub.add_parser("full", help="download, clip, reframe, captions; compose after review")
    x.add_argument("url"); x.add_argument("--slug", required=True)
    x.add_argument("--start", required=True); x.add_argument("--end", required=True)
    x.add_argument("--until", help="download up to here (default: the clip end)")
    x.add_argument("--aspect", default="9:16", choices=list(REFRAME))
    x.add_argument("--full-srt", type=Path, help="the checked full transcript (strongly preferred)")
    x.add_argument("--title"); x.add_argument("--music", type=Path); x.add_argument("--outro")
    x.add_argument("--min-tail", type=float, default=0.15)
    x.add_argument("--lang", default="English"); x.add_argument("--model", default="medium")
    x.add_argument("--device", default="cpu", choices=["cpu", "cuda"])
    x.add_argument("--max-height", type=int, default=1080)
    x.add_argument("--force", action="store_true", help="download again even if source.mp4 exists")
    x.add_argument("--yes", action="store_true", help="captions already reviewed: compose now")
    x = sub.add_parser("publish", help="deliverable folder plus PUBLISH.md")
    x.add_argument("reel", type=Path); x.add_argument("--dest", type=Path, required=True)
    x.add_argument("--slug", required=True); x.add_argument("--title", default="")
    x.add_argument("--episode", default=""); x.add_argument("--clip-range", default="")
    return p


def main(argv: list[str] | None = None) -> None:
    global DRY
    a = build_parser().parse_args(argv)
    DRY = a.dry_run
    theme = load_theme(a.theme)
    c = a.cmd
    if c == "check":
        cmd_check()
    elif c == "download":
        cmd_download(a.url, a.out, a.until, a.max_height)
    elif c == "clip":
        cmd_clip(a.src, a.start, a.end, a.out)
    elif c == "reframe":
        cmd_reframe(a.src, a.aspect, a.out)
    elif c == "extract-subs":
        mw = theme["max_words_per_fragment"] if a.max_words is None else a.max_words
        cmd_extract_subs(a.full_srt, a.start, a.end, a.out, mw, a.min_tail)
    elif c == "transcribe":
        cmd_transcribe(a.src, a.lang, a.model, a.device, a.out)
    elif c == "title":
        render_title(a.text, a.out, theme)
    elif c == "compose":
        cmd_compose(a.video, a.subs, a.title, a.music, _outro(a.outro, theme), a.out, theme)
    elif c == "probe-frame":
        cmd_probe_frame(a.src, a.frame, a.out)
    elif c == "full":
        a.end_pad = a.end
        cmd_full(a, theme)
    elif c == "publish":
        cmd_publish(a.reel, a.dest, a.slug, a.title, a.episode, a.clip_range, theme)


if __name__ == "__main__":
    main()
