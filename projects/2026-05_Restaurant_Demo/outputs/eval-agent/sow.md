# SOW Draft — Restaurant Demo

## Scope

Build a deterministic MVP for order and inventory workflow support:

- central order intake table in Google Sheets;
- product catalog and minimum-stock thresholds;
- stock validation for each order;
- low-stock alerts for the operator;
- Gmail-ready confirmation drafts;
- daily report with sales count, stock changes, low-stock products and exceptions.

## Out of Scope

- Autonomous WhatsApp sending.
- Supplier payments or autonomous purchases.
- Paid LLM runtime.
- Historical data migration beyond the initial catalog import.

## Timeline

- Week 1: catalog cleanup, workflow capture, data model.
- Week 2: backend scripts and Google Sheets workflow.
- Week 3: dashboard/manual operator view and SOP.
- Week 4: QA, handover and 7-day pilot monitoring plan.

## Estimate

- 48 hours.
- 3360 EUR setup.
- Optional maintenance after delivery: 250-350 EUR/month, approved separately.

## Acceptance Criteria

- Order rows can be validated against stock.
- Low-stock products are flagged.
- Daily report is generated.
- QA score is at least 7/10.
- No paid LLM API is used.
