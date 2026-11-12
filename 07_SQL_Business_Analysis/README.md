# SQL Business Analysis and Reporting Data

This folder implements repeatable procurement KPI analysis for the fictional **Meridian Global Services** case study. The generated dataset is synthetic and uses a fixed reporting snapshot of **9 November 2026, 12:00 UTC**.

## Contents

| File or folder | Purpose |
| --- | --- |
| `07_build_analysis_db.py` | Expands the seed dataset into an analysis-ready SQLite database |
| `07_business_analysis.sql` | Eight read-only procurement analysis queries |
| `07_run_analysis.py` | Executes the queries and generates reporting outputs |
| `07_validate_dataset.py` | Checks relational integrity and business rules |
| `07_SQL_Results.md` | Query result tables for the reporting snapshot |
| `07_SQL_Walkthrough.md` | Technical explanation of the SQL logic and metrics |
| `07_Insights_and_Actions.md` | Business findings, caveats, and proposed actions |
| `powerbi_import/` | Seven synthetic CSV source tables used in Power BI |
| `reference/06_schema.sql`, `reference/06_sample_data.sql` | Reference copies of the seed schema and data |

Local SQLite databases (`*.db`) are generated when needed and are intentionally not tracked in Git.

## Reproduce the dataset and reports

Run from the **repository root** using Python 3.10+:

```powershell
python 06_Database_Design/06_build_and_check.py
Copy-Item 06_Database_Design/06_meridian_demo.db 07_SQL_Business_Analysis/reference/06_meridian_demo.db
python 07_SQL_Business_Analysis/07_build_analysis_db.py
python 07_SQL_Business_Analysis/07_run_analysis.py
python 07_SQL_Business_Analysis/07_validate_dataset.py
```

These scripts use Python's standard library. The analysis builder copies the seed database before extending it; it does not modify the original Step 6 seed. Running the reporting script refreshes both `07_SQL_Results.md` and the CSV exports.

## Analysis scope and definitions

The snapshot contains 409 requisitions, 305 issued purchase orders, 300 delivered purchase orders, and 301 recorded invoices. Examples of the assessed KPIs include:

- **Committed PO value:** issued purchase order value, not cash paid.
- **Approval duration:** elapsed hours from stage assignment to decision, for completed stages.
- **Approval ageing:** time pending at the fixed reporting snapshot; 48 hours is an illustrative threshold, not a verified company SLA.
- **On-time delivery:** on-time receipts divided by delivered orders; open orders are assessed separately.
- **Invoice exceptions:** mismatch counts and rates using the simplified one-order/one-receipt/one-invoice model.

The CSVs in `powerbi_import/` support the editable [Power BI dashboard](../08_PowerBI_Dashboard/Meridian_Procurement_Analytics.pbix). Results describe a simulated process, not observed organisational performance or achieved benefits.
