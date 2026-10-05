# Golden example: raw responses and how they parse (synthetic)

Three responses, one per parser branch.

## AI A (Strategist, API): canonical fenced block, parser branch 1

````
```findings
{
  "summary": "Test with a rented cargo bike and a fixed weekly slot at one office park before committing to a van.",
  "answers": [
    {"q_id": "Q1", "answer": "Likely, where secure bike parking and showers exist; demand concentrates in spring and summer.", "confidence": "medium", "sources": ["general commuter-cycling patterns"]},
    {"q_id": "Q2", "answer": "Rent a cargo bike with a tool kit, partner with one office park's facilities team, run 8 Tuesdays.", "confidence": "high", "sources": []},
    {"q_id": "Q3", "answer": "Repairs that need workshop tools cannot be done on site, so the visit turns into a pick-up service.", "confidence": "medium", "sources": []}
  ],
  "open_questions": ["Will office parks allow a vendor on site without a fee?"],
  "flags": []
}
```
END_OF_RESPONSE
````

## AI B (Researcher, browser): fence lost in rendering, parser branch 2

The web interface rendered the code block with a plain `text` label, so no `findings` fence was found. Decoding from the first `{` consumed the whole object with nothing left over: the payload is whole, **not** a contract violation, no re-prompt.

```
text
{"summary": "Demand exists but is seasonal; most comparable services run as pick-up and return, not on-site repair.", "answers": [{"q_id": "Q1", "answer": "Comparable services report most bookings in April to September.", "confidence": "medium", "sources": ["industry blog post, 2024", "trade association survey, 2021"]}, {"q_id": "Q2", "answer": "A booking page plus a pick-up and return slot tests demand without any vehicle.", "confidence": "high", "sources": []}, {"q_id": "Q3", "answer": "Low winter demand.", "confidence": "high", "sources": []}], "open_questions": [], "flags": ["The survey source is from 2021 and may be out of date."]}
END_OF_RESPONSE
```

## AI C (Validator, API): flat shape, parser branch 3

````
```findings
{
  "Q1": "Unproven. Office workers may prefer to drop the bike at the workshop near home.",
  "Q2": "Pre-sell: offer 20 prepaid service slots by email at one office park; if fewer than 10 sell, stop.",
  "Q3": "The van and its running costs would conflict with the no-debt rule and eat most of the 15 000 budget."
}
```
END_OF_RESPONSE
````

Normalized into `answers` with `q_id` Q1 to Q3, confidence not given (treated as medium), and the flag `normalized from flat shape`.
