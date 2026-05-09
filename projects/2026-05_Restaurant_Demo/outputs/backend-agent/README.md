# Backend Implementation Report — Restaurant Demo

## Purpose

The backend MVP is deterministic. It centralizes orders, validates stock and produces daily reports without paid LLM API calls.

## Data Model

- `orders`: order id, source, items, customer contact, requested time, status.
- `catalog`: sku, product name, aliases, active flag.
- `stock`: sku, current quantity, minimum threshold.
- `exceptions`: order id, reason, suggested operator action.
- `daily_report`: date, sales count, low-stock products, exceptions.

## Recommended Flow

1. New order lands in the orders sheet.
2. Validator maps each item to catalog.
3. Stock check marks order as `confirmed`, `needs_review` or `out_of_stock`.
4. Confirmation text is prepared for operator review.
5. Daily report summarizes results at closing time.

## Security

- Keep Google service account credentials outside Git.
- Do not store customer PII in public docs or marketing content.
- No autonomous supplier payments.

## Handoff

Frontend should expose a simple operator queue with filters for `needs_review`, `out_of_stock` and `low_stock`.
