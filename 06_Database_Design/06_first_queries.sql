-- MERIDIAN | STEP 06: Three starter queries (run after 06_build_and_check.py)
-- Q1: Which requests exist, how much are they worth and who submitted them?
SELECT r.req_id, u.full_name AS requester, r.department,
       v.vendor_name, r.amount_inr, r.status
FROM requisitions r
JOIN users u ON r.requester_id = u.user_id
JOIN vendors v ON r.vendor_id = v.vendor_id
ORDER BY r.req_id;

-- Q2: Which approval stages are pending? (FR-06)
SELECT r.req_id, r.amount_inr, a.stage_no, a.approver_role,
       a.assigned_at, a.decision
FROM approvals a
JOIN requisitions r ON a.req_id = r.req_id
WHERE a.decision = 'Pending'
ORDER BY a.assigned_at;

-- Q3: Validate approval band boundary cases in the seeded data.
SELECT r.req_id, r.amount_inr, COUNT(a.approval_id) AS required_stages
FROM requisitions r
JOIN approvals a ON r.req_id = a.req_id
WHERE r.req_id IN (1004,1005,1006)
GROUP BY r.req_id, r.amount_inr
ORDER BY r.req_id;
