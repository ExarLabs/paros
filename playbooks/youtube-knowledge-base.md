---
title: youtube-knowledge-base
date: 2026-10-05
status: active
description: Playbook for turning followed YouTube channels (and podcasts) into a searchable knowledge base. Captions harvested with yt-dlp, cleaned with timestamp markers, kept as notebook-ready chunks in the vault plus a local full-text index that deep-links to the second, a registry with required keys, append-only updates, and measured lessons on video ids, rate limits, podcast coverage from RSS, duplicates and clips, broken captions, guest appearances and upload verification.
---

# Playbook: a YouTube knowledge base

## What you get

The channels you follow (a teacher, a podcast, a conference, a topic you study) turned into your own library:
- **search in milliseconds** across every video, with a link that opens the video at the exact second the words were said;
- **notebook-ready chunks** you can load into NotebookLM (or any local tool) and ask questions with citations;
- **a registry** that knows every channel, its language and every video id, so a weekly check finds new uploads and adds only those.

No API cost: captions are downloaded with `yt-dlp`, everything else is plain Python.

## Before you start

- `yt-dlp` installed (and kept up to date: YouTube changes often). `ffmpeg` is not needed for captions.
- Python 3.9 or newer.
- A local media folder **outside the vault** for raw captions and the index (they are large and rebuildable).
- Optional: NotebookLM and the [`notebooklm-experts`](notebooklm-experts.md) playbook, if you want to ask the corpus questions.
- Optional: [`skills/transcribe`](../skills/transcribe/CURRENT.md) for videos or episodes without captions.
- Time: minutes of your attention, hours of unattended harvest for a large channel.

## The shape of it

```
<vault>/<resources>/_transcripts/          source of truth, synced
  _registry.json                           every channel: required keys (step 6)
  <slug>/00_CHANNEL.md                     manifest note: url, language, count, last harvest, updates
  <slug>/notebooklm/<slug>_part_NN.md      the chunks, per-video sections with [HH:MM:SS] markers

<local media>/<slug>-transcripts/          per machine, rebuildable
  captions/<upload_date>__<id>.<lang>.vtt  raw captions
  metadata.jsonl                           lean metadata (not huge .info.json files)
  index.db                                 SQLite full-text (FTS5) index
```

Two homes on purpose: the chunks in the vault are the source; the index can be rebuilt from them on any machine. **Exclude the `_transcripts` folder from your main vault index**, or millions of caption words will drown your own notes.

## Steps

### 1. Name the channel

**Agent:** asks for the channel URL (the `/videos` tab, or a playlist), a short **slug** (`acme-talks`), a readable **label**, and the **caption language**. The language is per channel: a channel in German needs `de`, not the default `en`.

**Agent:** counts the videos first (`yt-dlp --flat-playlist --print "%(id)s" <url> | wc -l`) and tells you the size and the expected time.

**You decide:** go, or narrow to a playlist.

### 2. Harvest (unattended)

**Agent:** runs the harvest in the background with a pause between requests (start with 2 seconds) and a download archive seeded from captions already on disk, so a rerun makes **zero requests** for finished videos.

- **Rate limits:** if the log fills with rate-limit errors, stop and restart with a longer pause (4 seconds). Do not just restart: the archive resumes cleanly, the longer pause is the fix. Drop back to 2 once it is clean.
- **Expect 95 to 98 percent coverage.** Some videos have no captions in that language; they are skipped. Auto-captions are good for search, not verbatim quotes.

### 3. Build the index, and check the markers

**Agent:** cleans each caption into text that **keeps `[HH:MM:SS]` markers**, and builds the full-text index from it.

**Check, do not assume:** run one search. If the result link has no `&t=` part, the markers were lost in cleaning, and the chunks will have none either. The fault is in the cleaner, not in the captions. Fix it before exporting.

### 4. Export the chunks into the vault

**Agent:** writes per-video sections (title, date, link, text with markers) into chunk files, each **under about 470,000 words** (NotebookLM accepts about 500,000 words per source; the free plan allows 50 sources per notebook). Plus the manifest note and the registry entry.

**This full export is for the first time only.** See step 7 for updates.

### 5. Search

**Agent:** a search script reads the registry and searches one channel or all, ranked (bm25), each hit with a `?t=` link to the moment. A small page on top of it is optional ([`build-a-dashboard`](build-a-dashboard.md)).

### 6. The registry: required keys, checked

**Agent:** every registry entry has the same keys: `slug, label, channel_url, language, last_harvest, media_dest, db_path, vault_chunks, video_count, video_ids, enabled`.

A missing or renamed key (`vault_path` instead of `vault_chunks`) made the update check and the search **skip that channel silently**, with no error. After every write to the registry, by script or by hand, compare the entry's keys with an existing entry and fail loudly on any difference.

### 7. Updates: append-only, never a full re-export

New uploads and a full harvest of a new channel are **two different operations**: a weekly check compares each registered channel's current video ids with the registry and lists what is new.

**Agent:** for a channel already loaded into a notebook, makes **one new part** from the new videos only, with the next number and the date range in the name (`<slug>_part_11__2026-09-01_to_2026-10-05.md`). Old parts stay untouched. A full re-export deletes and re-cuts every part, which makes the sources already uploaded to the notebook stale. No new videos, no new part: the update stays idempotent. Then update `video_ids`, `video_count`, `last_harvest` and the manifest's update section.

### 8. Upload, and verify the upload

**Agent:** the update has two halves: the part in the vault, and the part in the notebook. The second can fail silently: in practice two parts were never uploaded while the registry showed the channel as fresh.

After each upload, check the **notebook's source list** for the part's name, not only that the upload command finished. Record "uploaded on <date>" or "NOT uploaded" in the manifest. Before each update, compare the vault's parts with the notebook's source list and upload what is missing.

If you use an unofficial command-line tool for NotebookLM: its sign-in session lives for a variable time (observed from 20 minutes to 90), so test it before a batch, and **check the status or error field of every JSON answer**. An expired session showed up as an error field inside a normal answer, not as a failing exit code.

### 9. Podcasts: the YouTube channel is not the whole show

**Agent:** for a podcast, after the harvest:
1. **Coverage from the RSS feed.** The feed is the truth for the episode list. In one measured case the feed had 240 episodes and YouTube 154; in another, 16 videos had no captions and most of the rest were short clips. Transcribe missing or caption-less episodes from the feed's audio ([`skills/transcribe`](../skills/transcribe/CURRENT.md)).
2. **Duplicates and clips by content, not title.** Compare 5-word shingles: overlap divided by the shorter text. **0.9 or more** is the same episode; **0.7 or more with a partner three times longer** is a clip contained in it. Move the losers to a `_duplicates/` folder; never delete.
3. **Broken captions:** under about 60 words per minute (for example 217 words for 30 minutes) the caption is broken. Re-transcribe from audio.
4. **Mixed sources need a title round.** When existing parts are audio transcripts and new candidates are YouTube auto-captions (or the reverse), the same episode scores below 0.5 overlap. After the shingle check, compare candidate titles with existing section titles (guest name and the main title words, not generic words like "Interview"). A title match is a suspicion, not a decision: check date, length and content by eye, because false matches happen.

### 10. A person, not a channel

**Agent:** if the corpus is about one person, their newest material is often a **guest appearance** on someone else's show. Search for it (a YouTube results page, plus a podcast guest list site), get each video's date individually, and filter hard: only the hosting show's own channel; leave out fan re-uploads, AI-voiced imitations, audiobook and compilation channels (those are not their words). If an appearance exists both in parts and whole, take one. Put guest appearances in a **separate, marked part**, and note that the host's words are in it too, without speaker labels.

### 11. A topic, not a channel (curated corpus)

**Agent:** when no single channel covers a topic, collect video URLs from several channels into a list and feed that list to the harvest. Export **one file per source channel**, so a notebook citation names the channel. Mark the registry entry `curated: true` with a `source_channels` list. The new-upload check skips curated entries: growing them is a new hand selection, never an automatic extension.

## Check that it works

1. A search for a phrase you remember returns the video, and the link opens at the right second.
2. A video id that starts with `_` or contains `__` appears intact in the registry and the chunks (see Pitfalls).
3. Run the harvest again: zero new requests, no new part.
4. After an update, the notebook's source list contains every part in the vault.
5. Your main vault search does not return caption text.

## Pitfalls

- **Splitting the file name at the last `__`.** Caption files are named `<upload_date>__<id>.<lang>.vtt`, and a YouTube id can itself contain `__` or start with `_`. Split at the **first** `__` (`name.split("__", 1)[1]`, then strip the language suffix). Splitting at the last one turned an id into a fragment, dropped the video from the parts and made a naive diff report ten false new videos.
- **Losing the timestamp markers** in cleaning. Test for `&t=` in a search result.
- **A full re-export after upload.** It invalidates the notebook's sources. Append a part.
- **Registry entries with a shortened schema.** Silently skipped. Check keys after every write.
- **"Uploaded" because the command ran.** Check the source list.
- **Restarting on rate limits** instead of slowing down.
- **The wrong caption language.** Zero captions, no error.
- **Captions in the vault index.** They bury your own notes.
- **A podcast taken from YouTube alone.** Use the feed.
- **Fan channels in a person's corpus.** Not their words.

## Principles behind it

- [P01](../principles/P01-persistence.md): the chunks are plain files you own; the index is rebuildable from them.
- [P06](../principles/P06-search.md): a ranked local index with deep links.
- [P09](../principles/P09-forgetting-and-archiving.md): duplicates moved aside, never deleted; parts appended, never rewritten.
- [P11](../principles/P11-health-contract.md): check the output (markers, registry keys, the notebook's source list), not that a script ran.
- [P12](../principles/P12-one-fact-one-owner.md): the registry is the one list of what is in the library.

## Related

- Playbook: [`notebooklm-experts`](notebooklm-experts.md) (the corpus as a consultable expert, with a knowledge map).
- Skill: [`transcribe`](../skills/transcribe/CURRENT.md) (audio for missing captions and podcast episodes).
- Agent: [Librarian](../agents/librarian/CURRENT.md) (the new-upload check across registered channels).
- Kit: [`search`](../kits/search/README.md) (the same index-first idea for the vault).
