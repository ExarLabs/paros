#!/usr/bin/env python3
"""
PAROS transcribe skill: audio or video to text via the Groq Whisper API.

Service: https://api.groq.com/openai/v1/audio/transcriptions
Models:  whisper-large-v3        (default "v3": best accuracy, still seconds)
         whisper-large-v3-turbo  ("turbo": faster, slightly less accurate)

What this client does:
  - uploads a LOCAL audio or video file (Groq does not take URLs);
  - extracts the audio track with ffmpeg when the container is not one Groq
    accepts (for example .mov or .mkv);
  - compresses to 16 kHz mono 32 kbps mp3 when the file is over the upload
    limit, and splits into chunks when it is still too large (txt only);
  - writes txt, SRT or WebVTT;
  - prints a completeness hint (audio length, word count, words per minute)
    when ffprobe is available, so a silently shortened transcript is noticed.

API key resolution (first hit wins). The key is never printed or logged:
  1. GROQ_API_KEY environment variable
  2. $PAROS_SECRETS_DIR/groq/api_key   (default dir: ~/.paros/secrets)

Dependencies: Python 3 standard library only. ffmpeg and ffprobe on PATH are
needed only for extraction, compression, chunking and the completeness hint.

CLI:
    python transcribe.py INPUT [options]
    python transcribe.py INPUT --dry-run     # check key, file and tools; upload nothing

Programmatic use:
    from transcribe import transcribe
    text = transcribe("meeting.m4a", lang="auto")
"""
import argparse
import json
import mimetypes
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

API_URL = "https://api.groq.com/openai/v1/audio/transcriptions"
UPLOAD_LIMIT = 24 * 1024 * 1024  # stay under the 25 MB free-tier cap
CHUNK_SECONDS = 3000             # about 50 minutes per chunk after compression

# Containers the API accepts by extension. Anything else is rejected with
# HTTP 400 even when the audio inside is fine, so the audio is extracted first.
SUPPORTED_EXTS = {".flac", ".mp3", ".mp4", ".mpeg", ".mpga", ".m4a",
                  ".ogg", ".opus", ".wav", ".webm"}
_BOUNDARY = "----parosTranscribeBoundary7MA4YWxkTrZu0gW"

MODEL_ALIASES = {
    "turbo": "whisper-large-v3-turbo",
    "large-v3-turbo": "whisper-large-v3-turbo",
    "whisper-large-v3-turbo": "whisper-large-v3-turbo",
    "v3": "whisper-large-v3",
    "large-v3": "whisper-large-v3",
    "whisper-large-v3": "whisper-large-v3",
}

LANG_CODES = {
    "english": "en", "hungarian": "hu", "romanian": "ro", "german": "de",
    "french": "fr", "spanish": "es", "italian": "it", "portuguese": "pt",
    "dutch": "nl", "polish": "pl",
    "auto": None, "automatic": None,
}


class NoKeyError(RuntimeError):
    pass


def _secrets_dir():
    return (os.environ.get("PAROS_SECRETS_DIR")
            or os.path.join(os.path.expanduser("~"), ".paros", "secrets"))


def _load_key():
    """Return the API key. Never print or log the value."""
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if key:
        return key
    path = os.path.join(_secrets_dir(), "groq", "api_key")
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            key = f.read().strip()
        if key:
            return key
    raise NoKeyError(
        "No Groq API key found. Set the GROQ_API_KEY environment variable, or "
        "put the key in a file at $PAROS_SECRETS_DIR/groq/api_key (default "
        "~/.paros/secrets/groq/api_key). Keep it outside your vault and never "
        "paste it into a chat.")


def _lang_code(lang):
    if not lang:
        return None
    low = lang.strip().lower()
    if low in LANG_CODES:
        return LANG_CODES[low]
    return low  # an ISO code, or an unknown value the API rejects clearly


def _have(cmd):
    return shutil.which(cmd) is not None


def _duration_seconds(path):
    if not _have("ffprobe"):
        return None
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", path],
            capture_output=True, text=True, timeout=60)
        return float(out.stdout.strip())
    except Exception:
        return None


def _multipart(fields, file_field, file_path):
    b = _BOUNDARY.encode()
    parts = []
    for name, value in fields.items():
        if value is None:
            continue
        parts += [b"--", b, b"\r\n",
                  ('Content-Disposition: form-data; name="%s"\r\n\r\n' % name).encode(),
                  str(value).encode("utf-8"), b"\r\n"]
    ctype = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    with open(file_path, "rb") as f:
        filebytes = f.read()
    parts += [b"--", b, b"\r\n",
              ('Content-Disposition: form-data; name="%s"; filename="%s"\r\n'
               % (file_field, os.path.basename(file_path))).encode("utf-8"),
              ("Content-Type: %s\r\n\r\n" % ctype).encode(),
              filebytes, b"\r\n--", b, b"--\r\n"]
    return b"".join(parts)


def _api_call(file_path, model, lang, response_format, prompt, key, timeout):
    fields = {"model": model, "response_format": response_format}
    code = _lang_code(lang)
    if code:
        fields["language"] = code
    if prompt:
        fields["prompt"] = prompt
    body = _multipart(fields, "file", file_path)
    last_err = None
    for attempt in range(3):
        req = urllib.request.Request(
            API_URL, data=body, method="POST",
            headers={"Authorization": "Bearer " + key,
                     # The API's edge rejects the default Python-urllib
                     # User-Agent (HTTP 403, error 1010); a curl-like one passes.
                     "User-Agent": "curl/8.4.0 (paros-transcribe)",
                     "Content-Type": "multipart/form-data; boundary=" + _BOUNDARY})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8")
            return json.loads(raw) if response_format != "text" else raw
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:500]
            if e.code in (429, 500, 502, 503) and attempt < 2:
                wait = int(e.headers.get("retry-after") or (5 * (attempt + 1)))
                sys.stderr.write("HTTP %d, retrying in %ds...\n" % (e.code, wait))
                time.sleep(wait)
                last_err = RuntimeError("Groq API HTTP %d: %s" % (e.code, detail))
                continue
            raise RuntimeError("Groq API HTTP %d: %s" % (e.code, detail))
    raise last_err


def _extract_audio(src, workdir):
    """Pull the audio out of an unsupported container into .m4a. Tries a
    lossless stream copy first, falls back to re-encoding to AAC."""
    if not _have("ffmpeg"):
        raise RuntimeError(
            "%s is not a supported container and ffmpeg is not on PATH to "
            "extract its audio. Install ffmpeg, or convert it to one of: %s."
            % (src, ", ".join(sorted(SUPPORTED_EXTS))))
    dst = os.path.join(workdir, "audio.m4a")
    copied = subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vn", "-c:a", "copy", dst])
    if copied.returncode != 0 or not os.path.isfile(dst) or os.path.getsize(dst) == 0:
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", src,
             "-vn", "-c:a", "aac", "-b:a", "128k", dst], check=True)
    return dst


def _compress(src, workdir):
    """Re-encode to 16 kHz mono 32 kbps mp3, plenty for speech recognition."""
    if not _have("ffmpeg"):
        raise RuntimeError(
            "%s is over the %d MB upload limit and ffmpeg is not on PATH to "
            "compress it. Install ffmpeg." % (src, UPLOAD_LIMIT // (1024 * 1024)))
    dst = os.path.join(workdir, "compressed.mp3")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", src,
         "-vn", "-ac", "1", "-ar", "16000", "-b:a", "32k", dst], check=True)
    return dst


def _split(src, workdir):
    pattern = os.path.join(workdir, "chunk_%03d.mp3")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-f", "segment",
         "-segment_time", str(CHUNK_SECONDS), "-c", "copy", pattern], check=True)
    chunks = sorted(os.path.join(workdir, n) for n in os.listdir(workdir)
                    if n.startswith("chunk_"))
    if not chunks:
        raise RuntimeError("ffmpeg produced no chunks for %s" % src)
    return chunks


def _ts(t, sep=","):
    ms = int(round(t * 1000))
    h, rem = divmod(ms, 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return "%02d:%02d:%02d%s%03d" % (h, m, s, sep, ms)


def _segments_to_subs(segments, vtt=False):
    sep = "." if vtt else ","
    lines = ["WEBVTT", ""] if vtt else []
    for i, seg in enumerate(segments, 1):
        if not vtt:
            lines.append(str(i))
        lines.append("%s --> %s" % (_ts(seg["start"], sep), _ts(seg["end"], sep)))
        lines.append(seg["text"].strip())
        lines.append("")
    return "\n".join(lines)


def _normalise_format(fmt):
    low = fmt.strip().lower()
    if low not in ("txt", "srt", "webvtt", "vtt", "json"):
        raise ValueError("format must be txt, SRT, WebVTT or json")
    return low


def plan(inp, fmt="txt"):
    """Dry run: check the key, the input and the tools, upload nothing.
    Returns a list of human-readable lines."""
    _load_key()  # raises NoKeyError; the value is discarded, never shown
    if not os.path.isfile(inp):
        raise FileNotFoundError(inp)
    fmt_low = _normalise_format(fmt)
    lines = ["key: found (value not shown)",
             "input: %s (%.1f MB)" % (inp, os.path.getsize(inp) / 1048576.0)]
    ext = os.path.splitext(inp)[1].lower()
    if ext not in SUPPORTED_EXTS:
        lines.append("step: extract audio with ffmpeg (%s not accepted)" % ext)
    if os.path.getsize(inp) > UPLOAD_LIMIT:
        lines.append("step: compress with ffmpeg (over the upload limit)")
        if fmt_low != "txt":
            lines.append("warning: if compression is not enough, only txt works")
    needs_ffmpeg = ext not in SUPPORTED_EXTS or os.path.getsize(inp) > UPLOAD_LIMIT
    lines.append("ffmpeg: %s" % ("found" if _have("ffmpeg") else
                                 ("MISSING, required" if needs_ffmpeg else "not found, not needed")))
    dur = _duration_seconds(inp)
    lines.append("duration: %s" % ("%.0f s" % dur if dur else ("unknown" if _have("ffprobe") else "unknown (no ffprobe)")))
    lines.append("dry run: nothing was uploaded")
    return lines


def transcribe(inp, lang="auto", model="v3", fmt="txt", prompt=None,
               timeout=600, key=None, quiet=False):
    """Transcribe a local audio or video file. Returns text (txt), subtitle
    content (SRT or WebVTT), or the raw verbose_json dict (json)."""
    key = key or _load_key()
    if not os.path.isfile(inp):
        raise FileNotFoundError(inp)
    model = MODEL_ALIASES.get(model.strip().lower(), model)
    fmt_low = _normalise_format(fmt)
    response_format = "text" if fmt_low == "txt" else "verbose_json"

    workdir = tempfile.mkdtemp(prefix="paros_transcribe_")
    try:
        upload = inp
        if os.path.splitext(upload)[1].lower() not in SUPPORTED_EXTS:
            if not quiet:
                sys.stderr.write("Container not accepted; extracting audio with ffmpeg...\n")
            upload = _extract_audio(upload, workdir)
        if os.path.getsize(upload) > UPLOAD_LIMIT:
            if not quiet:
                sys.stderr.write("Over the upload limit, compressing with ffmpeg...\n")
            upload = _compress(upload, workdir)
        chunks = [upload]
        if os.path.getsize(upload) > UPLOAD_LIMIT:
            if fmt_low != "txt":
                raise RuntimeError(
                    "Input needs chunking (still over the limit after compression); "
                    "chunked mode supports --format txt only.")
            if not quiet:
                sys.stderr.write("Still over the limit, chunking...\n")
            chunks = _split(upload, workdir)

        results = []
        for i, chunk in enumerate(chunks):
            if len(chunks) > 1 and not quiet:
                sys.stderr.write("Chunk %d/%d...\n" % (i + 1, len(chunks)))
            results.append(_api_call(chunk, model, lang, response_format,
                                     prompt, key, timeout))

        if response_format == "text":
            return "\n".join(r.strip() for r in results)
        result = results[0]
        if fmt_low == "json":
            return result
        return _segments_to_subs(result.get("segments") or [],
                                 vtt=fmt_low in ("webvtt", "vtt"))
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def _completeness_hint(inp, text):
    dur = _duration_seconds(inp)
    words = len(text.split())
    if not dur:
        return "completeness: %d words (audio length unknown)" % words
    wpm = words / (dur / 60.0) if dur > 0 else 0
    note = ""
    if wpm < 80:
        note = "  LOW: check the start and the end, or run the other model"
    return ("completeness: %.0f s audio, %d words, %.0f words/min%s"
            % (dur, words, wpm, note))


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Transcribe a local audio or video file with the Groq Whisper API.")
    ap.add_argument("input", help="local audio or video file")
    ap.add_argument("--lang", default="auto",
                    help="language name or ISO code, or auto (default: auto). "
                         "A wrong language silently produces fluent nonsense.")
    ap.add_argument("--model", default="v3", help="v3 (default, best accuracy) | turbo (faster)")
    ap.add_argument("--format", dest="fmt", default="txt", choices=["txt", "SRT", "WebVTT"])
    ap.add_argument("--prompt", help="vocabulary hint: names and terms (max about 224 tokens)")
    ap.add_argument("--out", help="write the transcript to this file")
    ap.add_argument("--download-dir", help="write the transcript into DIR as <input-name>.<ext>")
    ap.add_argument("--timeout", type=int, default=600, help="per-request timeout in seconds")
    ap.add_argument("--json", dest="as_json", action="store_true", help="print the raw verbose_json")
    ap.add_argument("--dry-run", action="store_true",
                    help="check key, input and tools; upload nothing")
    ap.add_argument("--quiet", action="store_true", help="print only the transcript")
    args = ap.parse_args(argv)

    if args.dry_run:
        try:
            for line in plan(args.input, args.fmt):
                print(line)
        except NoKeyError as e:
            sys.stderr.write("ERROR: %s\n" % e)
            return 3
        except Exception as e:
            sys.stderr.write("ERROR: %s\n" % e)
            return 1
        return 0

    started = time.time()
    try:
        out = transcribe(args.input, lang=args.lang, model=args.model,
                         fmt="json" if args.as_json else args.fmt,
                         prompt=args.prompt, timeout=args.timeout, quiet=args.quiet)
    except NoKeyError as e:
        sys.stderr.write("ERROR: %s\n" % e)
        return 3
    except urllib.error.URLError as e:
        sys.stderr.write("ERROR: could not reach api.groq.com (%s). "
                         "Check the internet connection.\n" % e.reason)
        return 2
    except Exception as e:
        sys.stderr.write("ERROR: %s\n" % e)
        return 1
    elapsed = time.time() - started

    if args.as_json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    if not args.quiet:
        sys.stderr.write("[%s] done in %.1fs\n"
                         % (MODEL_ALIASES.get(args.model.strip().lower(), args.model), elapsed))
        if args.fmt == "txt":
            sys.stderr.write(_completeness_hint(args.input, out) + "\n")
    print(out)

    ext = {"txt": ".txt", "SRT": ".srt", "WebVTT": ".vtt"}[args.fmt]
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        sys.stderr.write("Saved transcript to %s\n" % args.out)
    if args.download_dir:
        os.makedirs(args.download_dir, exist_ok=True)
        base = os.path.splitext(os.path.basename(args.input))[0]
        dest = os.path.join(args.download_dir, base + ext)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(out)
        sys.stderr.write("Saved transcript to %s\n" % dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
