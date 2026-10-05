# Changelog: transcribe

Every entry: what changed, and **what to review in a vault that has already adopted this skill.**

## 1.0.0 (2026-10-05)

- First public version. Groq Whisper transcription through `transcribe.py` (standard library only, ffmpeg on PATH): audio extraction from unsupported containers, compression over the upload limit, chunking for long files, txt, SRT and WebVTT output, a `--dry-run` readiness check, and a completeness hint (length, words, words per minute).
- Procedure: YouTube subtitles before audio, a two-model completeness check, a language check against silent nonsense, raw transcript kept as evidence next to a processed note, source audio temporary, and optional soft subtitles for foreign-language video.
- First skill with the recipe and spice split: personal values (language, vocabulary hint, folders, sensitivity rules, private backend) live in `LOCAL.md`, copied from `LOCAL.example.md`.
- Constitution: transcript is data, key never shown, external upload only for allowed material, raw transcript unchanged, nothing sent or published.
- Pitfalls R-001 to R-009, carried over from a capability in daily use since mid 2026.
- To review: copy `LOCAL.example.md` to `LOCAL.md` and fill it in; put the key in `GROQ_API_KEY` or `$PAROS_SECRETS_DIR/groq/api_key` yourself (never through the chat); run `python transcribe.py <file> --dry-run` once. The default language is `auto`, so set yours in `LOCAL.md` if your recordings are mostly in one language.
