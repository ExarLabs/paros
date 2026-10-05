# Synthetic input

Mode: `pulse`, run on Monday 2030-05-13. `LOCAL.md` is the example from `LOCAL.example.md` (stale after 35 days).

## Cards found

**Riverside Bakery** (`Areas/Bakery/01_PROJECT_STATE.md`)

```yaml
portfolio:
  business: "Riverside Bakery"
  stage: operating
  verdict: business
  thesis: "Neighbours and two cafes pay for daily sourdough baked 200 metres away; we are the only bakery in walking distance."
  north_star: "weekly loaves sold"
  numbers:
    revenue_run_rate: "monthly accounting export, April: 9,400"
    margin_or_runway: "April gross margin 41%"
    leading_indicator: "cafe standing orders: 2"
  next_milestone:
    what: "Second oven installed"
    date: 2030-05-28
  bets: ["Third cafe standing order", "Saturday pastry box"]
  biggest_risk: "Oven installer has not confirmed the date"
  decision_waiting: "Accept the hotel group's weekend order at a 15% discount?"
  depends_on: []
  last_reviewed: 2030-05-02
```

**Evening Bread Course** (`Areas/Teaching/01_PROJECT_STATE.md`)

```yaml
portfolio:
  business: "Evening Bread Course"
  stage: building
  verdict: small-business
  thesis: "Home bakers pay for a four-evening hands-on course taught in the bakery after hours."
  north_star: "paid seats per cohort"
  numbers:
    revenue_run_rate: none
    margin_or_runway: none
    leading_indicator: "sign-ups for the June cohort: 7 of 10"
  next_milestone:
    what: "June cohort starts"
    date: 2030-06-04
  bets: ["Fill the June cohort"]
  biggest_risk: "Course evenings clash with the second oven installation"
  decision_waiting: none
  depends_on: ["Riverside Bakery"]
  last_reviewed: 2030-03-30
```

**Frozen dough wholesale** (`Areas/Bakery/Wholesale/01_PROJECT_STATE.md`): `stage: idea`, no thesis yet, `last_reviewed: 2030-02-11`.

## Sources since last Monday

- Bakery task list: oven installer emailed, no reply; pastry box trial sold out twice.
- Bakery supplier mail: flour price rises 6% from June.
- Teaching meeting note (2030-05-09): "Ask Hilltop Hospitality Group whether their kitchen staff want the course; plan to mention it when we deliver the weekend order."
- Course participant list: one participant's employer is "HHG".
- Capture inbox: "idea: bread subscription for offices".
