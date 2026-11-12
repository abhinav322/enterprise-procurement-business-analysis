# Step 07 — SQL Analysis Results

**All observations use synthetic data.** Reporting snapshot: 9 November 2026, 12:00 UTC. Approval SLA threshold of 48 hours is illustrative.

## 01 | Requisition pipeline overview

| status | requisition_count | requested_value_inr |
| --- | --- | --- |
| Approved | 305 | 45975600 |
| Pending | 65 | 8531401 |
| Rejected | 39 | 5744300 |

## 02 | PO committed value by department

| department | purchase_orders | committed_po_value_inr | avg_po_value_inr |
| --- | --- | --- | --- |
| IT | 86 | 13404500 | 155866.0 |
| Human Resources | 53 | 8559200 | 161494.0 |
| Facilities | 34 | 7467600 | 219635.0 |
| Finance | 56 | 6481000 | 115732.0 |
| Operations | 40 | 5265200 | 131630.0 |
| Marketing | 36 | 4798100 | 133281.0 |

## 03 | Completed approval decisions: time and illustrative SLA

| approver_role | completed_decisions | avg_review_hours | reviewed_after_48h | pct_over_48h |
| --- | --- | --- | --- | --- |
| Finance Controller | 174 | 63.1 | 105 | 60.3 |
| Department Manager | 359 | 60.6 | 220 | 61.3 |
| Head of Procurement | 64 | 59.0 | 38 | 59.4 |

## 04 | Pending approval backlog by reviewer role

| approver_role | pending_approvals | avg_pending_hours | pending_over_48h |
| --- | --- | --- | --- |
| Department Manager | 50 | 121.2 | 44 |
| Finance Controller | 11 | 126.7 | 11 |
| Head of Procurement | 4 | 148.4 | 4 |

## 05 | On-time delivery performance by vendor

| vendor_name | delivered_orders | on_time | on_time_pct | avg_late_hours_all_deliveries |
| --- | --- | --- | --- | --- |
| ByteBridge Technologies | 29 | 22 | 75.9 | 4.3 |
| UrbanSpace Supplies | 18 | 14 | 77.8 | 2.1 |
| Northstar Advisory | 39 | 31 | 79.5 | 3.4 |
| Cedar Consulting | 39 | 31 | 79.5 | 3.1 |
| Atlas SaaS Solutions | 59 | 47 | 79.7 | 3.3 |
| BrandSpring Studio | 5 | 4 | 80.0 | 13.0 |
| CloudRiver Licensing | 54 | 45 | 83.3 | 3.4 |
| Spark Creative Agency | 6 | 5 | 83.3 | 2.7 |
| NimbleTech Systems | 39 | 34 | 87.2 | 1.2 |
| Prime Facilities Co | 12 | 12 | 100.0 | 0.0 |

## 06 | Open purchase orders that are overdue at the reporting snapshot

| vendor_name | overdue_open_orders | oldest_overdue_hours |
| --- | --- | --- |
| Cedar Consulting | 2 | 649.5 |
| ByteBridge Technologies | 1 | 621.1 |
| Atlas SaaS Solutions | 1 | 477.9 |

## 07 | Invoice match status summary

| match_status | invoice_count | invoiced_amount_inr | share_of_invoices_pct |
| --- | --- | --- | --- |
| Matched | 256 | 39014000 | 85.0 |
| Discrepancy | 44 | 6321400 | 14.6 |
| Awaiting Receipt | 1 | 82500 | 0.3 |

## 08 | Three-way match investigation: first 12 exceptions

| invoice_id | vendor_name | po_quantity | accepted_qty | invoice_qty | po_value_inr | invoice_amount_inr | first_exception_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4003 | BrandSpring Studio | 3 | 2 | 3 | 300000 | 300000 | Accepted quantity mismatch |
| 4009 | ByteBridge Technologies | 2 | 2 | 2 | 85000 | 87000 | Invoice amount mismatch |
| 4010 | Atlas SaaS Solutions | 5 | 2 | 5 | 22500 | 22500 | Accepted quantity mismatch |
| 4019 | NimbleTech Systems | 12 | 3 | 12 | 600000 | 600000 | Accepted quantity mismatch |
| 4038 | Cedar Consulting | 12 | 12 | 12 | 21600 | 29600 | Invoice amount mismatch |
| 4041 | ByteBridge Technologies | 3 | 3 | 2 | 60000 | 40000 | Invoice quantity mismatch |
| 4078 | Atlas SaaS Solutions | 4 | 4 | 4 | 200000 | 201200 | Invoice amount mismatch |
| 4079 | ByteBridge Technologies | 6 | 6 | 6 | 27000 | 30000 | Invoice amount mismatch |
| 4084 | Cedar Consulting | 4 | 1 | 4 | 12000 | 12000 | Accepted quantity mismatch |
| 4086 | ByteBridge Technologies | 6 | 6 | 6 | 300000 | 301200 | Invoice amount mismatch |
| 4101 | Atlas SaaS Solutions | 8 | 5 | 8 | 400000 | 400000 | Accepted quantity mismatch |
| 4103 | CloudRiver Licensing | 4 | 2 | 4 | 300000 | 300000 | Accepted quantity mismatch |
