# Step 07 — SQL Business Analysis

## Our goal

Use the database designed in Step 06 to calculate **business KPIs** for procurement. We are analysing a fictional company with **synthetic** transactions. The SQL queries are read-only and the sample dataset is repeatable.

## Your Windows / VS Code steps

1. Inside `Enterprise Procurement BA Project`, create a folder called `07_SQL_Business_Analysis`.
2. Extract all files from the ZIP into that folder. Keep the `reference` and `powerbi_import` subfolders.
3. Open `07_SQL_Business_Analysis` as a folder in VS Code.
4. In the terminal, run:

```powershell
python 07_build_analysis_db.py
python 07_run_analysis.py
```

Both scripts use Python's built-in modules; **no pip install, SQLite server or Power BI installation** is needed for Step 07.

5. Open `07_SQL_Results.md` to see the actual result tables. Open `07_business_analysis.sql` and read **Query 02** alongside `07_SQL_Walkthrough.md` for the line-by-line explanation.

## Main files

| File | Why it exists |
|---|---|
| `07_build_analysis_db.py` | Adds 400 reproducible synthetic purchase requests and related records to a **copy** of the Step 06 demo DB. |
| `07_meridian_analysis.db` | Prebuilt analysis-ready SQLite database (409 requisitions total). |
| `07_business_analysis.sql` | Eight annotated SQL investigations: statuses, PO value, approval delays, delivery, invoice exceptions. |
| `07_run_analysis.py` | Executes SQL and exports results + Power BI import tables. |
| `07_SQL_Results.md` | Actual query output tables. |
| `07_SQL_Walkthrough.md` | Understand the SQL and KPI definitions without a quiz. |
| `07_Insights_and_Actions.md` | BA-style analysis, business implications, and proposed actions. |
| `07_validate_dataset.py` | Runs integrity and business-rule checks. |
| `powerbi_import/*.csv` | Seven related CSV tables for our next Power BI step. |
| `reference/06_meridian_demo.db` | **Unchanged** seed database from Step 06. |

## Validation

Run `python 07_validate_dataset.py` and look for `ALL CHECKS PASSED`. This verifies relationships, approval stage completeness, status alignment, and invoice matches.

## What we've completed

A working SQL evidence base, not just documentation. In Step 08 we will import the CSVs into Power BI, set the relationships, and build the dashboard using exactly the same KPI definitions. We will tackle Power BI next, rather than build it all in advance.
