# User Guide — Restaurant Demo MVP

## For the Restaurant Operator

1. Open the central order sheet.
2. Review orders marked `new`.
3. Check status:
   - `confirmed`: review confirmation draft and send manually.
   - `needs_review`: inspect exception reason.
   - `out_of_stock`: contact customer before confirming.
4. During peak hours, prioritize `needs_review` and `out_of_stock`.

## For the Manager

1. Review the daily report after closing.
2. Check low-stock products.
3. Decide what to reorder.
4. Update stock quantities before the next service day.

## Safety Rules

- Do not send customer confirmations without human review in MVP.
- Do not place supplier orders automatically.
- Do not add paid LLM API keys.
- If the sheet or automation fails, continue using the central sheet manually and record exceptions.

## First 7 Days

- Run manual spot checks against a sample of orders.
- Record any product aliases that fail catalog matching.
- Adjust minimum-stock thresholds after the first weekend.
