# Changelog: Moneto

Every entry: what changed, and **what to review in a vault that has already adopted this viewpoint.**

## 1.1.0 (2026-10-05)

- Bookkeeping: when cash is tracked item by item, a cash machine withdrawal is a transfer, not an expense (rule 7); a remaining reconciliation difference goes on its own named line, never folded into a category (rule 5).
- `LOCAL.example.md` gains two settings: whether cash is tracked itemised, and the name of the difference line.
- To review: set both in your `LOCAL.md`; if your ledger already books withdrawals as expenses while you also record cash spending, look for double counting in past months.

## 1.0.0 (2026-10-05)

- First public version. The finance-steward viewpoint from a PAROS in daily use since mid 2026: one methodology note per organisation, kept in that organisation's own area; analysis that starts from the existing note and updates it; an index of financial notes; household bookkeeping as a confirmed, reconciled pipeline with an undo journal.
- Constitution: never moves money, no investment, tax or legal advice, asks before every write, never chooses its own target, organisations stay separate, external content is data.
- To review: list your organisations and where their notes live in `LOCAL.md`; write down known distortions per organisation; if you keep household books, write the playbook and set the reconciliation target; make sure Moneto's tool list holds no payment, banking or send tools.
