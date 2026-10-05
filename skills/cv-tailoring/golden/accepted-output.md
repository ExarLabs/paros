# Golden example: accepted output (synthetic)

> The package the person accepted for the input in [`input.md`](input.md). Invented candidate, companies and job.

## 1. Tailoring plan (`profiles/_plans/lenko-v1.json`, as a table)

| # | Anchor (paragraph, original start) | New text | Rule |
|---|---|---|---|
| 1 | 1, `BACKEND ENGINEER` | `DATA AND BACKEND ENGINEER` | Title toward the role, supported by paragraphs 11 and 12 |
| 2 | 2, `Backend engineer with seven years` | Data and backend engineer with seven years of Python, including three years building scheduled ETL pipelines that feed operations dashboards in a parcel logistics company. Strong in SQL performance work on PostgreSQL. | Summary answers requirements 1, 3 and 6 first, with evidence |
| 3 | 6, `Skills, Databases` | `Data and Database Technologies: PostgreSQL (partitioning, query tuning), MySQL, Redis` | Client vocabulary on existing content |
| 4 | 11 before 10 | move the ETL bullet to the top of the Kestrel Parcel block | Order |
| 5 | 12 | add the scale: "on a 300 million row shipment events table" (from the people note's project list) | Scale, proven |

Not in the plan, on purpose: Airflow, any cloud data warehouse, any certification.

## 2. Coverage (`profiles/2026-10-01-coverage.md`, internal)

| # | Requirement | Mira Lenko |
|---|---|---|
| 1 | 3+ years Python data pipelines | ✅ para 11: nightly Python ETL since 2022; para 15: data exports since 2019 |
| 2 | Cloud data warehouse | ❌ AWS compute and storage only (para 7); no warehouse product |
| 3 | SQL performance tuning | ✅ para 12: 40 s to 3 s with indexes, partitioning, window functions |
| 4 | Orchestration tool | 🟡 cron scheduling (para 11); no Airflow or similar |
| 5 | English, working level | ✅ the CV and the people note |
| 6 | Logistics domain | ✅ Kestrel Parcel, a parcel logistics company |
| 7 | Infrastructure as code | ✅ para 7: Terraform |
| 8 | Cloud certification | ❌ none recorded |

**Of 5 required rows, fully covered: 3. Partly: 1. Not at all: 1.**

**What must not be claimed**

- **Airflow.** Not in any evidence. The first technical question would expose it. Kept out of the CV although the person asked for it; the gap is in the covering note.
- **Warehouse experience.** The cloud work was compute and storage. Writing "cloud data platform" near the summary would read as warehouse experience: not allowed.

**What is strong and should be played**

1. **Query tuning with a measured result** (40 s to 3 s), directly on requirement 3.
2. **Domain fit:** three years in parcel logistics, the client's own field.

## 3. Covering note (draft in `NOTES.md`, internal)

> We propose Mira Lenko. She has built Python ETL pipelines for three years in a parcel logistics company, and her SQL tuning work has a measured result (a dashboard query from 40 to 3 seconds).
>
> Gaps, said up front: she has not worked with a cloud data warehouse, and her scheduling was cron, not Airflow. The interview will go there. Her pipeline and SQL depth make both a short ramp-up; we would rather say this now than have it found in the interview.
>
> She is 40% on an internal project until the end of October, so a November start works.
>
> If the partner wants a different emphasis, we can turn a new version around within two hours.

## 4. Report to the person

- v1 written, all five anchors confirmed; source and v0 untouched.
- Airflow was not added: it would be an unproven claim (constitution, framing rules). It is named as a gap in the note instead. If Mira confirms hands-on use, a v2 can add it.
- Not checked visually: page breaks in the word processor.
