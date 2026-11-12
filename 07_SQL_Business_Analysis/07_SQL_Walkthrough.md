# Step 07 | SQL Business Analysis — Guided Walkthrough

**Company:** Meridian Global Services (fictional)  
**Your role:** Technical Business Analyst  
**Data:** 409 synthetic requisitions (9 test records from Step 06 + 400 new records), snapshot 09 Nov 2026 12:00 UTC.

## What we're doing and why

Step 06 gave us a relational **data structure**. Step 07 uses SQL to investigate business questions set out in our BRD: are approvals delayed, where is purchase value concentrated, how reliable are vendors, and how often do invoices require attention? These queries produce evidence that informs the Power BI dashboard and proposed process changes.

## How to read and run the SQL

The file `07_business_analysis.sql` has **eight labelled, read-only SELECT queries**. Open it in VS Code. You can execute everything without installing a separate SQL server by running `python 07_run_analysis.py`. The output is saved as `07_SQL_Results.md`. Read the results while comparing each query's business question with the output table.

## Walkthrough: our first substantive JOIN and GROUP BY

From **Query 02: PO committed value by department**:

```sql
SELECT
  r.department,
  COUNT(po.po_id) AS purchase_orders,
  SUM(r.amount_inr) AS committed_po_value_inr
FROM purchase_orders AS po
JOIN requisitions AS r ON po.req_id = r.req_id
GROUP BY r.department
ORDER BY committed_po_value_inr DESC;
```

- `FROM purchase_orders AS po` starts with issued purchase orders, *not* every request. This avoids counting pending or rejected requests as committed procurement value.
- `JOIN requisitions AS r ON po.req_id = r.req_id` uses the shared requisition ID to attach each PO to the department and approved amount.
- `COUNT(po.po_id)` counts purchase orders in each department.
- `SUM(r.amount_inr)` totals the committed purchase-order value. It's **not** payment or cash-outflow data.
- `GROUP BY r.department` gives one summary row per department.
- `ORDER BY ... DESC` displays the departments with the largest committed value first.

**Why BA recruiters care:** the SQL is tied to a business definition. A technically correct `SUM` on the wrong population can produce a misleading KPI.

## What each remaining query answers

| Query | Business question | SQL techniques |
|---|---|---|
| 01 | How many requests are Approved, Pending or Rejected? | `GROUP BY`, `COUNT`, `SUM` |
| 03 | Which review stage takes the longest? | Date arithmetic, `AVG`, conditional aggregation |
| 04 | Who has a pending approval backlog? | `WITH` (CTE), `JOIN`, case expression, snapshot date |
| 05 | Which vendors have the lowest on-time delivery %? | Join, `CASE WHEN`, rate calculation |
| 06 | Which vendors have open overdue purchase orders? | Date comparison, `MAX`, filtering |
| 07 | What share of invoices need exception handling? | Aggregation, scalar subquery |
| 08 | Why is an invoice flagged? | Multi-table joins, `LEFT JOIN`, `CASE` |

## Essential definitions used in this case study

- **Requisition amount:** value requested by an employee (can be pending or rejected).
- **PO committed value:** amount on an issued purchase order. **Do not call this paid spend.**
- **Approval review time:** `decided_at − assigned_at` for decisions that are completed. Pending stages are excluded.
- **Pending approval age:** reporting snapshot − `assigned_at`. We use a fixed snapshot so repeated runs are comparable.
- **Illustrative review SLA:** 48 elapsed hours. This is a modelling assumption, not a company policy.
- **On-time delivery %:** delivered orders received by their promised date ÷ all delivered orders. Open orders are analysed separately.
- **Three-way match:** compare purchase order, goods receipt, and supplier invoice. This demo assumes **one PO, one receipt and one invoice**.

## Boundaries and honest interpretation

The data is **fully synthetic**. Our observations describe only the simulated scenario; they are not findings about a real procurement organisation. This database is a deliberately simplified case study (no tax, exchange rates, multi-line POs, split receipts, credit notes, or production authentication). It shows BA analytics methods and should not be represented as real business experience.
