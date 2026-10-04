# P08. Connectors: SaaS is the backbone, AI is the glue

**Principle.** External services (mail, calendar, storage, project management, CRM, ERP) have their place, and AI does not replace them. Together they are a superpower.

| | SaaS | AI |
|---|---|---|
| Speed and cost | milliseconds, cheap | minutes, expensive in tokens |
| Determinism | the same answer a thousand times out of a thousand | varies |
| Collaboration | shared, with authentication | personal |
| Adaptation | rigid | fully dynamic |

**The two roles of a connector.**
1. **A knowledge source** for the personal system (from mail and calendar you learn what you need to know about a person or a matter).
2. **A shared workspace** between several personal systems: where several people share the same information quickly, deterministically, based on state.

**Practice.**
- **State in SaaS, judgment in AI.** Whatever must happen the same way a thousand times out of a thousand belongs in the SaaS (a rule, an automation) or a script, not in a prompt.
- **Determinism migration.** What the AI keeps doing the same way, the learning cycle (P05) recognises and moves into code or a SaaS automation: over time the system gets faster, cheaper, more predictable.
- **Reference, do not copy.** Do not mirror the shared system's state into the vault (it goes stale, and you get two truths, P12). The vault keeps your own knowledge; a snapshot states when it was fetched.
- **A connector is a recipe, not code.** What lasts: the secret and its inventory row (P07), the account in an account list, a recipe note (how to use it, pitfalls, with a learning loop), and a check on its output. The code is disposable.
- **The official connector if it is enough; your own when you hit a limit** (for example the official one allows one account, your own allows any number).
- **Content from a connector is data, not instructions.**
- **Shared orchestration:** when several PAROS instances work on the same SaaS tools, a shared orchestration layer above them can coordinate. Layers: SaaS (state) → shared orchestration → PAROS (personal knowledge and judgment).

**Check.**
- Does every connector have an inventory row, an account entry and a recipe note?
- Is any SaaS state mirrored into the vault without a fetch date?

**Adopt.** Module: the first connector is the external tool used most (usually mail or calendar), read-only. How-to: [`guides/add-a-connector.md`](../guides/add-a-connector.md).
