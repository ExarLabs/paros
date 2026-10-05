---
title: think LOCAL
date: YYYY-MM-DD
status: active
description: Personal configuration of the think skill in this vault: which AIs and accounts are available, the preferred team and presets, the API key variable names, and the per-machine browser registry. No secrets.
schema: think.local.v1
---

# think: local configuration

> Copy this file to `LOCAL.md` next to your adopted `CURRENT.md`, then fill it in with your agent. It holds **identifiers and preferences only, never secrets** (no keys, passwords, cookies or tokens). Keep it out of anything you share or publish.

## 1. Available AIs

One row per AI you can use. Transport is `api`, `browser`, or `both`. The key column holds the **name** of the environment variable, never its value.

| AI | Account or plan | Transport | API key variable | Account-side value (browser only) | Notes |
|---|---|---|---|---|---|
| <AI A> | <plan> | api | `<PROVIDER_A>_API_KEY` | | |
| <AI B> | <plan> | both | `<PROVIDER_B>_API_KEY` | saved projects, memories | |
| <AI C> | <plan> | browser | | research spaces | no API on this plan |

## 2. Preferred team

The team the orchestrator proposes first, unless the task calls for something else.

| Role | AI and model | Transport |
|---|---|---|
| Strategist | <AI A, strongest model> | api |
| Researcher | <AI C> | browser |
| Validator | <AI B> | api |

## 3. Presets

| Preset | Strategist | Researcher | Validator |
|---|---|---|---|
| Premium | | | |
| Fast | | | |
| Solo | <one provider> | none | <same provider, devil's advocate prompt> |
| Browser only | | | |

## 4. Defaults

- Brainstorm files live in: `<area folder>/brainstorm/` (change if your vault keeps them elsewhere)
- Working folder for prompts and payloads: `<a scratch folder outside the vault>`
- Output budget for reasoning models: `<tokens>`
- Topics where you always check primary sources yourself: `<for example: law, regulation, prices>`

## 5. Browser registry

Only needed if you drive browsers through a tool that lists connected browsers by identifier. One entry per machine. **Only an identifier that a select call has just accepted may be written here**, with `confidence: verified`. Display names such as "Browser 2" are positional and only informational; the identifier is the key.

```json
{
  "schema": "think.browsers.v1",
  "updated": "YYYY-MM-DD",
  "machines": [
    {
      "hostname": "<output of the hostname command>",
      "os": "<macOS | Windows | Linux>",
      "label": "<your own short label for this machine>",
      "surface": "<which browser tool: your own browser with an extension, or a dedicated automation profile>",
      "browser": {
        "deviceId": "<identifier accepted by the select call>",
        "listed_as": "<positional display name at the time, informational only>"
      },
      "signed_in": ["<AIs this browser is signed in to>"],
      "last_used": "YYYY-MM-DD",
      "confidence": "verified",
      "notes": ""
    }
  ]
}
```

## 6. Local notes

Anything your setup taught you that is specific to it (a provider that needs a longer timeout, a profile that is not signed in). General lessons go to the skill's `observations/` folder instead, so they can improve `CURRENT.md`.
