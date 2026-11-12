-- MERIDIAN | STEP 07 | BUSINESS ANALYSIS USING SQL (SQLite)
-- All figures are from SIMULATED procurement transactions, not operational company data.
-- Consistent reporting snapshot: 2026-11-09 12:00 UTC.
-- Run queries individually in a SQLite editor, or run all using 07_run_analysis.py.

-- QUERY: 01 | Requisition pipeline overview
SELECT
  status,
  COUNT(*) AS requisition_count,
  SUM(amount_inr) AS requested_value_inr
FROM requisitions
GROUP BY status
ORDER BY requisition_count DESC;

-- QUERY: 02 | PO committed value by department
-- IMPORTANT: This is the value of POs issued, NOT cash paid to vendors.
SELECT
  r.department,
  COUNT(po.po_id) AS purchase_orders,
  SUM(r.amount_inr) AS committed_po_value_inr,
  ROUND(AVG(r.amount_inr), 0) AS avg_po_value_inr
FROM purchase_orders AS po
JOIN requisitions AS r ON po.req_id = r.req_id
GROUP BY r.department
ORDER BY committed_po_value_inr DESC;

-- QUERY: 03 | Completed approval decisions: time and illustrative SLA
-- Elapsed hours are measured between assignment and decision.
-- 48 hours is a CASE-STUDY target, not an agreed contractual SLA.
SELECT
  approver_role,
  COUNT(*) AS completed_decisions,
  ROUND(AVG((julianday(decided_at) - julianday(assigned_at)) * 24), 1) AS avg_review_hours,
  SUM(CASE WHEN (julianday(decided_at) - julianday(assigned_at)) * 24 > 48 THEN 1 ELSE 0 END)
    AS reviewed_after_48h,
  ROUND(100.0 * SUM(CASE WHEN (julianday(decided_at) - julianday(assigned_at)) * 24 > 48
    THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_over_48h
FROM approvals
WHERE decision IN ('Approved', 'Rejected')
GROUP BY approver_role
ORDER BY avg_review_hours DESC;

-- QUERY: 04 | Pending approval backlog by reviewer role
-- Snapshot date is FIXED so results are reproducible and match the portfolio case study.
WITH pending_age AS (
  SELECT a.approval_id, a.approver_role, r.req_id,
    ROUND((julianday('2026-11-09T12:00:00Z') - julianday(a.assigned_at)) * 24, 1) AS age_hours
  FROM approvals AS a
  JOIN requisitions AS r ON r.req_id = a.req_id
  WHERE a.decision = 'Pending'
)
SELECT
  approver_role,
  COUNT(*) AS pending_approvals,
  ROUND(AVG(age_hours), 1) AS avg_pending_hours,
  SUM(CASE WHEN age_hours > 48 THEN 1 ELSE 0 END) AS pending_over_48h
FROM pending_age
GROUP BY approver_role
ORDER BY pending_over_48h DESC, pending_approvals DESC;

-- QUERY: 05 | On-time delivery performance by vendor
-- Only delivered orders enter the on-time delivery denominator.
SELECT
  v.vendor_name,
  COUNT(*) AS delivered_orders,
  SUM(CASE WHEN po.actual_delivery_at <= po.promised_delivery_at THEN 1 ELSE 0 END) AS on_time,
  ROUND(100.0 * SUM(CASE WHEN po.actual_delivery_at <= po.promised_delivery_at
    THEN 1 ELSE 0 END) / COUNT(*), 1) AS on_time_pct,
  ROUND(AVG(CASE WHEN po.actual_delivery_at > po.promised_delivery_at
    THEN (julianday(po.actual_delivery_at) - julianday(po.promised_delivery_at)) * 24
    ELSE 0 END), 1) AS avg_late_hours_all_deliveries
FROM purchase_orders AS po
JOIN vendors AS v ON v.vendor_id = po.vendor_id
WHERE po.status = 'Delivered' AND po.actual_delivery_at IS NOT NULL
GROUP BY v.vendor_id, v.vendor_name
ORDER BY on_time_pct ASC, delivered_orders DESC;

-- QUERY: 06 | Open purchase orders that are overdue at the reporting snapshot
-- An overdue order is OPEN and its promised date has already passed.
SELECT
  v.vendor_name,
  COUNT(*) AS overdue_open_orders,
  ROUND(MAX((julianday('2026-11-09T12:00:00Z') - julianday(po.promised_delivery_at)) * 24), 1)
    AS oldest_overdue_hours
FROM purchase_orders AS po
JOIN vendors AS v ON v.vendor_id = po.vendor_id
WHERE po.status = 'Open'
  AND po.promised_delivery_at < '2026-11-09T12:00:00Z'
GROUP BY v.vendor_id, v.vendor_name
ORDER BY overdue_open_orders DESC, oldest_overdue_hours DESC;

-- QUERY: 07 | Invoice match status summary
-- 'Awaiting Receipt' is a separate exception category, not treated as a confirmed mismatch.
SELECT
  match_status,
  COUNT(*) AS invoice_count,
  SUM(invoice_amount_inr) AS invoiced_amount_inr,
  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM invoices), 1) AS share_of_invoices_pct
FROM invoices
GROUP BY match_status
ORDER BY invoice_count DESC;

-- QUERY: 08 | Three-way match investigation: first 12 exceptions
-- Simplified one-PO / one-receipt / one-invoice business rule.
-- We compare PO quantity & value, received accepted quantity, and invoiced quantity & value.
SELECT
  i.invoice_id,
  v.vendor_name,
  r.quantity AS po_quantity,
  gr.accepted_qty,
  i.invoice_qty,
  r.amount_inr AS po_value_inr,
  i.invoice_amount_inr,
  CASE
    WHEN gr.receipt_id IS NULL THEN 'Missing goods receipt'
    WHEN gr.accepted_qty <> r.quantity THEN 'Accepted quantity mismatch'
    WHEN i.invoice_qty <> r.quantity THEN 'Invoice quantity mismatch'
    WHEN i.invoice_amount_inr <> r.amount_inr THEN 'Invoice amount mismatch'
    ELSE 'No mismatch found'
  END AS first_exception_reason
FROM invoices AS i
JOIN purchase_orders AS po ON i.po_id = po.po_id
JOIN requisitions AS r ON r.req_id = po.req_id
JOIN vendors AS v ON v.vendor_id = po.vendor_id
LEFT JOIN goods_receipts AS gr ON gr.po_id = po.po_id
WHERE i.match_status <> 'Matched'
ORDER BY i.invoice_id
LIMIT 12;
