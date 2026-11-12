# Step 06 — Database Design (Meridian Procurement)

## What this step does
We turn our functional requirements into a relational data model: tables, primary keys (PK), foreign keys (FK), and validation rules. We then create a small **synthetic** test database. The SQL investigation and larger dataset follow in Step 07.

## Files in this folder
- `06_Procurement_ERD.png`: visual map of the 8 tables and relationships.
- `06_Procurement_ERD.drawio`: editable equivalent for diagrams.net.
- `06_schema.sql`: table definitions, keys, constraints, and indexes.
- `06_sample_data.sql`: 9 hand-checked fictional purchase requests plus related rows.
- `06_meridian_demo.db`: already-built SQLite database; open in a SQLite viewer.
- `06_build_and_check.py`: builds the database from SQL scripts and tests the main relationships.
- `06_first_queries.sql`: three starter queries for inspecting the data.

## Your practical action (Windows + VS Code)
1. Extract this ZIP into your project's `06_Database_Design` folder.
2. Open the folder in VS Code. Open `06_Procurement_ERD.png` to understand the table relationships.
3. In VS Code Terminal / PowerShell, run: `python 06_build_and_check.py`
4. You should see **8 table counts**, three approval-threshold cases, and `PASSED`.
5. Open `06_schema.sql` to inspect table structure. To browse the `.db`, use any trusted SQLite database viewer; installing one is optional. Do **not** double-click the `.db` expecting a text document.

No PostgreSQL, server, account, or extra Python library is required for this step.

## How this maps to our requirements
- BR-01 / FR-01–02: `users`, `vendors`, `requisitions`.
- BR-02/03/04 / FR-03–07: `approvals` and `audit_log`.
- BR-05 / FR-08: `purchase_orders`, `goods_receipts`, `vendors`.
- BR-06 / FR-09: `purchase_orders`, `goods_receipts`, `invoices`.
- BR-07 / FR-11–12: `users` and reference keys define design foundations; actual role checks/API integration come later.

## Notes & limits
- Our 9 transactions are synthetic test cases, **not real company findings**.
- Approval routing and access rules are not automatically enforced by a database diagram; application logic must enforce them and UAT must verify them.
- The demo uses one PO per requisition, one receipt and one invoice per PO. Multi-line orders, partial shipments, split invoices, taxes, and multi-currency are later-scope enhancements.
- Sample monetary amounts are whole INR integers; a production design needs fixed-precision values supporting paise and financial controls.
- Timestamps are ISO 8601 in UTC; elapsed-hours SLAs can be calculated from these.

**Next step:** expand to a realistic synthetic transaction dataset and use SQL for approval ageing, spend, supplier reliability, and invoice exceptions.
