# Golden example: input (synthetic)

> Synthetic example. No real people, businesses or data.

## The question

A small neighbourhood bike repair workshop is considering a mobile repair van that visits office parks two days a week. Should it start, and if so, how?

## Local context the orchestrator read first

- `01_PROJECT_STATE.md`: workshop at capacity on Saturdays, idle on Tuesday and Wednesday mornings; budget for a new initiative up to 15 000.
- `decisions.md`: "No debt-financed vehicle purchases" (decided by the owner, 2026-03-02).

## Team (confirmed by the person)

| AI | Role | Transport |
|----|------|-----------|
| AI A | Strategist | API |
| AI B | Researcher | browser (uses a saved research space) |
| AI C | Validator | API |

## The fat prompt (shared core, role block differs per member)

```
CONTEXT: Neighbourhood bike workshop, idle Tue/Wed mornings, budget 15 000,
no debt-financed vehicles. Considering a mobile repair van at office parks 2 days a week.

Q1. Is there demand for on-site bike repair at office parks? (sources required)
Q2. What is the cheapest credible way to test it before buying or leasing a van?
Q3. What is the main risk that would make this fail?

<role block>

RESPONSE FORMAT (REQUIRED): ... findings block ... END_OF_RESPONSE
```
