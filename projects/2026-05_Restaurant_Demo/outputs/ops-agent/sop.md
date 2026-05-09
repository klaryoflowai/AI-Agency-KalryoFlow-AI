# SOP — Restaurant Demo Order and Stock MVP

## Daily Start

1. Open the central orders sheet.
2. Check that catalog and stock tabs are available.
3. Confirm the operator can see orders marked `needs_review`.

## During Service

1. New order appears or is manually entered.
2. Automation checks catalog and stock.
3. If status is `confirmed`, operator reviews confirmation draft.
4. If status is `needs_review`, operator checks the exception reason.
5. If status is `out_of_stock`, operator calls customer before confirming.

## Exception Handling

- Unknown product: map product alias to catalog or escalate to manager.
- Low stock: confirm only if stock is physically available.
- Missing customer contact: hold confirmation until contact is complete.
- WhatsApp order: manually enter into the order sheet in phase 1.

## Daily Close

1. Run or review daily report.
2. Check low-stock list.
3. Confirm exceptions are resolved or carried to next day.
4. Share replenishment recommendations with manager.

## Human Approval Rules

- No supplier order is placed automatically.
- No payment is initiated automatically.
- No customer message is sent without operator confirmation in MVP.
