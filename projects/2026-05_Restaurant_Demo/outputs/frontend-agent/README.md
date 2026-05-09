# Frontend Implementation Report — Restaurant Demo

## Goal

Create a practical operator dashboard for a busy restaurant team. The UI should be dense, quick to scan and clear under peak-hour pressure.

## Primary Views

### Orders Queue

- Status filters: new, needs review, out of stock, confirmed.
- Order detail panel with items, source, requested time and confirmation draft.
- Clear exception reason when an order cannot be confirmed automatically.

### Stock Exceptions

- Low-stock product list.
- Missing catalog matches.
- Suggested operator action for each exception.

### Daily Report

- Orders processed.
- Items sold.
- Low-stock items.
- Exceptions requiring follow-up.

## UX Rules

- Avoid decorative dashboards.
- Use tables, badges and compact controls.
- No automatic send/payment action without operator confirmation.
- Use Romanian labels for the client-facing/operator-facing UI.
