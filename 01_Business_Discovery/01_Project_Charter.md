# Project Charter — Meridian Procurement Process Transformation

**Version:** 0.1 (working draft)  
**Date:** 9 November 2026  
**Organisation:** Meridian Global Services *(fictional case-study organisation)*  
**Project:** Procure-to-Pay (P2P) Visibility & Approval Improvement  
**Your project role:** Technical Business Analyst  
**Status:** Initiation / business discovery

> **Portfolio disclosure:** This is a simulated business transformation case study. Business challenges, stakeholders, and operating rules are starting assumptions, not findings from real interviews. Analysis will use synthetic transaction data. Proposed targets are not achieved outcomes.

## 1. Why the project exists — business problem
Meridian hypothetically relies on email, spreadsheets, and disconnected tools to request purchases, route approvals, track suppliers, and reconcile invoices. As a result, teams **may** struggle to identify who owns pending approvals, where orders are delayed, and which invoices require attention. The project will investigate these potential bottlenecks before recommending changes.

## 2. Desired business outcomes
| Objective | How we will assess it |
|---|---|
| Faster purchase approvals | Compare average elapsed hours from requisition submission to final approval |
| Clear accountability | Track the current approval stage and owner for each open request |
| Better procurement visibility | Report spend, approval ageing, on-time deliveries, and invoice exceptions |
| Fewer unresolved exceptions | Identify requisitions or invoices requiring investigation |

**Illustrative target for evaluation:** a 25% reduction in average approval turnaround time *after a hypothetical future rollout*, subject to baseline validation. It is not an achieved result.

## 3. Scope for the portfolio MVP
**In scope**
- Define business requirements and map current-state (AS-IS) and proposed (TO-BE) procurement flows.
- Build a relational dataset for requisitions, approvals, purchase orders, goods receipts, invoices, and suppliers.
- Analyse process performance with SQL and present management KPIs in a dashboard.
- Prototype request submission, rule-based approval routing, and audit-history visibility.
- Document technical interfaces, Agile user stories, and UAT scenarios.

**Out of scope**
- Live ERP integrations (e.g., SAP/Oracle), real vendor or employee records, actual payments.
- Enterprise authentication / production-grade access controls, production hosting or deployment.
- Claims of verified cost savings or real stakeholder sign-off.

## 4. Key stakeholders — initial hypotheses
| Stakeholder | Expected interest / responsibility |
|---|---|
| Head of Procurement | Business sponsor; owns intended outcomes |
| Procurement Manager | Process owner; defines purchasing rules |
| Department Manager | Reviews and approves requisitions |
| Finance Controller | Reviews higher-value requests and invoice exceptions |
| Requesting employees | Create requisitions and need status visibility |
| IT / Integration team | Evaluates data model, interfaces, and security needs |

## 5. How we will know whether the solution helps
| KPI | Working definition / evaluation approach |
|---|---|
| Approval turnaround | Hours between request submission and final approval for approved requests |
| Pending approval ageing | Hours since current stage became actionable |
| On-time vendor delivery | Delivered POs on/before promised date ÷ all delivered POs with known promised date |
| Invoice exception rate | Invoices flagged for mismatched value/quantity ÷ all invoices evaluated |

**Measurement note:** First establish the baseline using the project's dataset. Synthetic data can demonstrate KPI calculations but cannot verify actual operational improvement.

## 6. Assumptions, risks, and dependencies
- Initial assumed approval policy: **up to ₹50,000:** Department Manager; **over ₹50,000 to ₹250,000:** add Finance; **over ₹250,000:** add Head of Procurement. Validate during requirements work.
- Approval-stage overdue flag: **more than 48 elapsed hours** (initial design assumption).
- Risks: incomplete or inconsistent data, unclear approval ownership, adoption barriers, missing permissions and ERP connectivity.
- Dependencies: stakeholder validation of policy and definitions; access to procurement records and system interfaces in a real deployment.

## 7. Deliverables and current gate
**Planned artifacts:** Charter → stakeholder/RACI map → BRD/FRD → AS-IS/TO-BE diagrams → SQL/BI analysis → workflow prototype → UAT → portfolio write-up.

**Approval gate:** This charter is a **draft**; in a real project, the executive sponsor would review its objectives and boundaries before detailed requirements discovery. No actual approval is claimed.

**Immediate next activity:** Stakeholder identification and a short requirements elicitation plan.
