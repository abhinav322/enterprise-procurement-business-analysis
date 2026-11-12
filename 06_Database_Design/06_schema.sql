-- MERIDIAN | STEP 06: Relational database schema (SQLite)
-- Fictional company and demonstration data; not live procurement records.
-- Enable FK validation for EACH SQLite connection.
PRAGMA foreign_keys = ON;

-- Employees and reviewers. The app will later enforce role access rules (FR-11).
CREATE TABLE users (
    user_id       INTEGER PRIMARY KEY,
    full_name     TEXT NOT NULL,
    department    TEXT NOT NULL,
    role          TEXT NOT NULL CHECK (role IN
                  ('Employee','Department Manager','Finance Controller',
                   'Head of Procurement','Procurement Manager'))
);

-- Vendor category is used to validate requisition selection (FR-01).
CREATE TABLE vendors (
    vendor_id     INTEGER PRIMARY KEY,
    vendor_name   TEXT NOT NULL UNIQUE,
    category      TEXT NOT NULL,
    region        TEXT NOT NULL,
    is_active     INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1))
);

-- A requisition is a purchase request, NOT yet a purchase order.
-- Monetary values are WHOLE INR in this small demo. Future production
-- design must support fixed-precision amounts, tax and multiple currencies.
CREATE TABLE requisitions (
    req_id          INTEGER PRIMARY KEY,
    requester_id    INTEGER NOT NULL REFERENCES users(user_id),
    vendor_id       INTEGER NOT NULL REFERENCES vendors(vendor_id),
    department      TEXT NOT NULL,
    category        TEXT NOT NULL,
    item_description TEXT NOT NULL,
    quantity        INTEGER NOT NULL CHECK (quantity > 0),
    unit_price_inr  INTEGER NOT NULL CHECK (unit_price_inr > 0),
    amount_inr      INTEGER GENERATED ALWAYS AS
                    (quantity * unit_price_inr) STORED,
    priority        TEXT NOT NULL DEFAULT 'Normal'
                    CHECK (priority IN ('Normal','Urgent')),
    needed_by       TEXT NOT NULL,              -- ISO date: YYYY-MM-DD
    created_at      TEXT NOT NULL,              -- ISO UTC timestamp
    status          TEXT NOT NULL DEFAULT 'Pending'
                    CHECK (status IN ('Pending','Approved','Rejected'))
);

-- One row per necessary approval stage, in sequence (FR-03 to FR-07).
CREATE TABLE approvals (
    approval_id   INTEGER PRIMARY KEY,
    req_id        INTEGER NOT NULL REFERENCES requisitions(req_id),
    stage_no      INTEGER NOT NULL CHECK (stage_no > 0),
    approver_role TEXT NOT NULL CHECK (approver_role IN
                  ('Department Manager','Finance Controller','Head of Procurement')),
    decision      TEXT NOT NULL CHECK (decision IN ('Pending','Approved','Rejected')),
    assigned_at   TEXT NOT NULL,
    decided_at    TEXT,
    UNIQUE (req_id, stage_no),
    CHECK ((decision = 'Pending' AND decided_at IS NULL) OR
           (decision <> 'Pending' AND decided_at IS NOT NULL))
);

-- MVP assumption: up to one PO per approved requisition.
CREATE TABLE purchase_orders (
    po_id                INTEGER PRIMARY KEY,
    req_id               INTEGER NOT NULL UNIQUE REFERENCES requisitions(req_id),
    vendor_id            INTEGER NOT NULL REFERENCES vendors(vendor_id),
    ordered_at           TEXT NOT NULL,
    promised_delivery_at TEXT NOT NULL,
    actual_delivery_at   TEXT,
    status               TEXT NOT NULL CHECK (status IN ('Open','Delivered','Cancelled'))
);

-- MVP assumption: up to one receipt per PO (partial deliveries: later scope).
CREATE TABLE goods_receipts (
    receipt_id   INTEGER PRIMARY KEY,
    po_id        INTEGER NOT NULL UNIQUE REFERENCES purchase_orders(po_id),
    received_at  TEXT NOT NULL,
    received_qty INTEGER NOT NULL CHECK (received_qty >= 0),
    accepted_qty INTEGER NOT NULL CHECK
                 (accepted_qty >= 0 AND accepted_qty <= received_qty)
);

-- MVP assumption: at most one supplier invoice per PO.
CREATE TABLE invoices (
    invoice_id         INTEGER PRIMARY KEY,
    po_id              INTEGER NOT NULL UNIQUE REFERENCES purchase_orders(po_id),
    invoiced_at        TEXT NOT NULL,
    invoice_qty        INTEGER NOT NULL CHECK (invoice_qty > 0),
    invoice_amount_inr INTEGER NOT NULL CHECK (invoice_amount_inr > 0),
    match_status       TEXT NOT NULL CHECK
                       (match_status IN ('Matched','Discrepancy','Awaiting Receipt')),
    paid_at            TEXT
);

-- Chronological history, useful for audit and root-cause analysis.
CREATE TABLE audit_log (
    log_id     INTEGER PRIMARY KEY,
    req_id     INTEGER NOT NULL REFERENCES requisitions(req_id),
    event_at   TEXT NOT NULL,
    actor      TEXT NOT NULL,
    event_type TEXT NOT NULL,
    details    TEXT NOT NULL
);

CREATE INDEX idx_requisitions_department_status ON requisitions(department,status);
CREATE INDEX idx_approvals_decision ON approvals(decision,assigned_at);
CREATE INDEX idx_approvals_req ON approvals(req_id,stage_no);
CREATE INDEX idx_purchase_orders_vendor ON purchase_orders(vendor_id);
CREATE INDEX idx_invoices_match_status ON invoices(match_status);
CREATE INDEX idx_audit_req_time ON audit_log(req_id,event_at);
