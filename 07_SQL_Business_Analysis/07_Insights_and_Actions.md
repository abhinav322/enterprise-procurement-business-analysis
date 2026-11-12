# Meridian | Step 07 — Findings and BA Action Register

> **SIMULATED DATA NOTICE:** Meridian is fictional; all transactions and results are synthetic. Findings below illustrate how a BA would turn SQL output into recommendations, not actual operational performance or verified causal relationships.

**Reporting as of:** 9 November 2026, 12:00 UTC. **Scope:** 409 purchase requests, 305 purchase orders, 300 delivered orders, 301 recorded invoices. The nine records carried over from Step 06 are included in these totals.

| Priority | SQL-backed observation in this simulation | BA interpretation / follow-up | Proposed response (not yet implemented) |
|---|---|---|---|
| High | **59 of 65 pending approval stages** have been waiting more than an illustrative 48 hours. | Potential approval backlog. Validate whether delay is due to missing information, availability, or approval policy. | Add manager work queues and overdue notifications; track approval ageing by role. |
| High | Completed approval stages average **61.2 elapsed hours**; **363 of 597** exceeded 48 hours. | Review turnaround time is above the illustrative target for many stages. | Confirm actual SLA with stakeholders, clarify ownership and escalation rules. |
| Medium | **44 of 301 invoices (14.6%)** show a discrepancy, with **1** more awaiting receipt. | Exception review is a meaningful part of the case-study workflow. | Add three-way match exception categories and a finance review queue. |
| Medium | **245 of 300 delivered POs (81.7%)** arrived on time; **4 open POs** were overdue at the snapshot. | Vendor performance merits segmented investigation before drawing conclusions. | Add vendor scorecard and a separate open-overdue-order report. |
| Medium | IT department accounts for **₹1,34,04,500 in issued PO value** across **86 purchase orders**. | IT is the highest committed-value department in this data. | Monitor PO commitments by department; obtain a separate payment source before calculating cash expenditure. |

## Causation caution

These numbers do **not** prove the root cause of delays or that automation will improve them. In a real project, the BA would validate findings with process owners, check sample quality, review approval policy, and establish pre/post implementation measurement.

## Requirements linkage

- **BR-02 / BR-03; FR-03–07:** approval routing, status and review-time investigation (Queries 03–04).
- **BR-05; FR-08:** supplier and delivery performance (Queries 05–06).
- **BR-06; FR-09:** invoice exception analysis (Queries 07–08).
- **BR-07:** management performance visibility (Queries 01–02).

## Dashboard KPI Specifications

1. Issued PO Value (INR) — sum of requisition amounts linked to purchase orders.
2. Pending Approval Count — count of approval records with `decision='Pending'`.
3. Pending Approvals >48h — count of pending approval stages older than the assumed threshold at the reporting snapshot.
4. On-Time Delivery % — on-time ÷ delivered purchase orders; open excluded.
5. Invoice Discrepancy Rate — discrepancy invoices ÷ all invoices; awaiting receipt displayed separately.

## Data limitations (disclose in portfolio)

- The company and dataset are fictional; results are simulated for technical practice.
- Single currency INR, whole-unit amounts, no tax or exchange-rate handling.
- MVP structure supports one PO per requisition, one goods receipt and one invoice per PO.
- No verified budgets or cost centres, and no distinct cash-payment ledger.
- Fixed reporting snapshot protects reproducibility but is **not** a live operational report.
