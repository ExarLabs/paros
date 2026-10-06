# P07. Secrets live outside the vault, travel encrypted, and are inventoried without values

**Principle.** Every connector depends on a secret (an API key, a token, a password). The **value never goes into the vault**, the chat, or the agent's context. Only two things go into the vault: an encrypted transfer bundle and an **inventory** (without values).

**Why.** The vault syncs, gets indexed, and is read by AI; a secret placed there is a leaked secret. In an agent system there is an extra risk: the agent itself could read a secret and send it out (prompt injection).

**Practice: four layers.**

| Layer | Where | What | Syncs |
|---|---|---|---|
| 1. The secret | per machine, outside the vault (for example `~/.paros/secrets/`) | the value | no |
| 2. Transfer | in the vault | an encrypted bundle: a random key (AES-256-GCM) locks it, and that key is encrypted to every machine's public key; on a machine, a passphrase unlocks the machine's own key | yes |
| 3. Inventory | in the vault (`SECRETS.json` plus a generated view) | without values: what it is, what for, who uses it, scope, rotation, where to revoke | yes |
| 4. Monitoring | script plus health check | unknown, missing, overdue secrets; a plain secret in the vault | alerts |

- Agents **read the inventory, never the secret**; scripts fetch the secret by name.
- A new secret means a new inventory row, in the same step.
- A leaked secret is rotated at the provider immediately.
- Recommended: a **recovery recipient** (a key protected by a strong passphrase), so the secrets survive the loss of every machine.

**Check.**
- Scan the vault for secret patterns (API key formats, private key headers).
- Scan beyond the vault too: the Downloads folder, loose scripts next to the vault, project folders (`tools/diagnose.py --also <folder>`). The worst leaks are usually there, not in the notes.
- Does every secret have an inventory row?

**Adopt.** With the first connector: a secrets folder outside the vault, an inventory, and the vault scan in the health checks. The encrypted bundle is needed when the second machine appears (kit: `kits/secrets`).
