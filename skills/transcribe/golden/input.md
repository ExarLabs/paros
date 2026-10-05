# Synthetic input

A 2 minute 10 second voice memo, `2026-10-03-shed-roof.m4a`, recorded by the person after talking to a roofer. `LOCAL.md` says: language `english`, vocabulary hint `Kestrel, EPDM`, raw transcripts in `Home/raw/`, processed notes in `Home/`.

Command run:

```bash
python transcribe.py 2026-10-03-shed-roof.m4a --lang english --prompt "Kestrel, EPDM" --download-dir "$TMPDIR"
```

Client output on stderr:

```
[whisper-large-v3] done in 2.1s
completeness: 130 s audio, 268 words, 124 words/min
```

Raw text returned:

```
Okay so quick note after the call with the roofer from Kestrel Roofing. He says the shed roof felt is done, it's not worth patching, water's getting under it at the back edge. Two options. One is new felt, about four hundred, done in a day. Two is an EPDM rubber membrane, about six fifty, but he says it lasts twenty years and not eight. He can't come before the twentieth either way. I think EPDM makes more sense but I want to check with Sam first because it's half Sam's shed. Also he said, and this is funny, ignore the gutter quote I sent you last week, he wants to redo it. Need to ask him to resend the gutter quote. And before the twentieth I should clear the bikes out of there and put a tarp over the back edge if it rains. That's it.
```
