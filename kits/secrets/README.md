# Kit: secrets (P07, an inventory without values)

A working reference for [P07](../../principles/P07-secrets.md): secrets live outside the vault, and the vault holds only an **inventory** of them, without values, plus (once there is a second machine) an encrypted transfer bundle. This kit gives the inventory, the per-machine presence check, and the health check hook. The encrypted bundle itself is a separate tool; this script only reads the plain file list a bundle carries, if bundles exist.

Optional. Read it, then rebuild or adapt it for the vault.

## The four layers

| Layer | Where | What | Syncs |
|---|---|---|---|
| 1. The secret | per machine, outside the vault (default `~/.paros/secrets/`) | the value | no |
| 2. Transfer | in the vault | an encrypted bundle per machine (`bundle-<machine>.enc.json`): a random key locks it, that key is encrypted to every machine's public key; the bundle also carries a plain list of the file names inside | yes |
| 3. Inventory | in the vault: `SECRETS.json` (canonical) and `SECRETS.md` (generated view) | without values: what it is, what for, who uses it, access, rotation, where to revoke | yes |
| 4. Monitoring | `secrets_inventory.py check` plus the health check | unknown, missing and overdue secrets | alerts |

## The rule for agents

**Agents read the inventory, never the secret.** The inventory tells an agent which secret serves which purpose and which script uses it. The agent never opens, prints or pastes a value: the script that needs the secret fetches it by name from the secrets folder. This also means a prompt injection that reaches the agent has no value to send out.

This script follows the same rule: it lists file names and modification dates in the secrets folder and never opens a file there.

## Files

| What | Where |
|---|---|
| The script | `secrets_inventory.py` (standard library only) |
| The schema, with three fictional entries | [`SECRETS.example.json`](SECRETS.example.json) |
| Your inventory | `SECRETS.json`, in the vault, for example next to the connectors folder |
| The generated view | `SECRETS.md`, next to the inventory |

### Fields of a secret

| Field | Meaning |
|---|---|
| `path` | the file, relative to the secrets folder (the identity of the row) |
| `provider`, `account` | who issued it, for which account |
| `kind` | API key, OAuth token, app password, private key, ... |
| `purpose` | what it is for, in one line |
| `used_by` | the scripts, connectors or skills that use it |
| `access` | its scope: how much damage a leak would do |
| `sensitivity` | personal, work, family, critical, ... |
| `first_seen` | when it appeared |
| `rotate_by` | the rotation date, or `null` |
| `revoke` | where and how to revoke it at the provider |
| `status` | `active`, `paused`, `rotate` (rotate now), `config` (not a secret, not checked), `noise` or `to-retire` (to clean up) |
| `notes` | anything else, never the value |
| `env_keys` | for env files: the variable names inside (names only) |
| `no_file` | `true` if it lives only at the provider (nothing to find on disk) |
| `per_machine` | `true` if each machine has its own (a machine's private key): checked only locally |

Top level: `machines` (the machine names that should hold the secrets), optional `machine_labels` (short column names for the view), `policy`, `secrets`, and `removed` (cleaned-up secrets with `path`, `date`, `reason`, `where`).

## Configuration

| Variable | Default |
|---|---|
| `PAROS_SECRETS_DIR` | `~/.paros/secrets` |
| `PAROS_SECRETS_INVENTORY` | `SECRETS.json` next to the script |
| `PAROS_SECRETS_BUNDLES` | `keyring/` next to the inventory (optional; without bundles, other machines show `?`) |
| `PAROS_HOST` | the machine's host name |

## Commands

```bash
python secrets_inventory.py          # status: entries, files per machine, and every difference
python secrets_inventory.py render   # rewrite SECRETS.md
python secrets_inventory.py check    # one JSON line for the health check: {"ok": ..., "detail": ...}
```

Status reports: unknown files (on disk, not in the inventory), secrets missing on a machine, secrets to rotate now or within 30 days, noise to clean up, and removed secrets still present somewhere.

## Onboarding a new secret, in one step

A new connector and its inventory row are one change, never two:

1. The owner puts the value into the secrets folder (a file, mode 600), typed or pasted by them into a hidden prompt or file, never into the chat.
2. In the same step the agent adds the row to `SECRETS.json`: path, provider, kind, account, purpose, used_by, access, sensitivity, first_seen, rotate_by, revoke, status.
3. `python secrets_inventory.py render`, and (with more than one machine) re-export the transfer bundle.

If a file appears in the secrets folder without a row, `check` turns red until the row exists.

## Health check integration

`check` prints a single JSON line and is meant to be one weighted check in the health kit (P11):

- **red** when there is an unknown secret or one overdue for rotation;
- **detail** names the first few, and reports secrets missing on another machine (informational).

Alert only on state change, like every other check. Pair it with the vault scan for plain secrets (API key formats, private key headers), which belongs to the health checks, not to this script.

## Not in this kit

- The encrypted transfer bundle (key generation, export, peek, apply). The principle is in P07; this kit reads only the plain file list of a bundle.
- Rotation itself: that happens at the provider, by the owner.
