# Database Design and Seed Dataset

This folder contains the relational data model for the **Meridian Global Services** procurement case study. All entities, users, vendors, and transactions are fictional.

## Data model

The SQLite schema (`06_schema.sql`) defines eight tables: `users`, `vendors`, `requisitions`, `approvals`, `purchase_orders`, `goods_receipts`, `invoices`, and `audit_log`. The ERD is available as an [image](06_Procurement_ERD.png) and an [editable Draw.io file](06_Procurement_ERD.drawio).

The design uses primary and foreign keys to connect procurement transactions. It models one purchase order per requisition and at most one goods receipt and one invoice per purchase order; partial shipments, multiple invoice lines, taxes, multi-currency, and production security controls are outside this prototype's scope.

## Files

| File | Purpose |
| --- | --- |
| `06_schema.sql` | Table definitions, relationships, constraints, and indexes |
| `06_sample_data.sql` | Nine hand-checked synthetic requisitions and related records |
| `06_build_and_check.py` | Builds the seed database and checks integrity and sample row counts |
| `06_first_queries.sql` | Starter SQL queries for inspecting the data |
| `06_Procurement_ERD.png` / `.drawio` | ERD image and editable source |

## Rebuild and validate

From the **repository root**, with Python 3.10 or newer:

```powershell
python 06_Database_Design/06_build_and_check.py
```

This creates `06_meridian_demo.db` locally from the checked-in SQL scripts. The `.db` file is intentionally excluded from Git; no SQLite server or additional Python dependency is required. The script checks foreign keys, expected table counts, and approval-boundary examples.

The seed database is used by the larger synthetic data builder in [`07_SQL_Business_Analysis`](../07_SQL_Business_Analysis/).

## Design assumptions

- Approval routing is enforced in application logic, not solely by the relational schema.
- Monetary values are stored as whole INR amounts for the demonstration; a financial production system should use an appropriate fixed-precision monetary representation.
- Timestamps use UTC and ISO 8601 formatting for reproducible time calculations.
- These records are illustrative test data and do not describe a real organisation.
