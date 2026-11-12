"""Meridian case-study API — Step 9.2, first endpoint only.

Run locally: python -m uvicorn main:app --reload
Visit: http://127.0.0.1:8000/docs

Copy 07_meridian_analysis.db into this folder as meridian_api.db BEFORE running.
This is a learning prototype, without user authentication or production controls.
"""
from datetime import date, datetime, timezone
from pathlib import Path
import sqlite3
from typing import Literal

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

DATABASE = Path(__file__).resolve().parent / "meridian_api.db"
app = FastAPI(title="Meridian Procurement API", version="0.1.0")


class RequisitionCreate(BaseModel):
    requester_id: int = Field(gt=0)
    vendor_id: int = Field(gt=0)
    category: str = Field(min_length=2)
    item_description: str = Field(min_length=3)
    quantity: int = Field(gt=0)
    unit_price_inr: int = Field(gt=0)
    priority: Literal["Normal", "Urgent"] = "Normal"
    needed_by: date


@app.post("/api/requisitions", status_code=status.HTTP_201_CREATED)
def create_requisition(req: RequisitionCreate):
    """Validate and persist a request, starting its first approval stage."""
    if not DATABASE.exists():
        raise HTTPException(500, "Copy your Step 7 database here as meridian_api.db")
    if req.needed_by < date.today():
        raise HTTPException(400, "needed_by must not be in the past")

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        requester = conn.execute(
            "SELECT department, role FROM users WHERE user_id = ?", (req.requester_id,)
        ).fetchone()
        if requester is None:
            raise HTTPException(404, "Requester not found")
        if requester["role"] != "Employee":
            raise HTTPException(400, "Requester must have the Employee role")

        vendor = conn.execute(
            "SELECT category, is_active FROM vendors WHERE vendor_id = ?", (req.vendor_id,)
        ).fetchone()
        if vendor is None:
            raise HTTPException(404, "Vendor not found")
        if not vendor["is_active"]:
            raise HTTPException(400, "Vendor is inactive")
        if req.category != vendor["category"]:
            raise HTTPException(400, "Category must match the selected vendor")

        amount = req.quantity * req.unit_price_inr
        stages = ["Department Manager"]
        if amount > 50_000:
            stages.append("Finance Controller")
        if amount > 250_000:
            stages.append("Head of Procurement")
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        # The transaction saves the request, first approval stage and audit event together.
        with conn:
            cursor = conn.execute(
                """INSERT INTO requisitions
                   (requester_id, vendor_id, department, category, item_description,
                    quantity, unit_price_inr, priority, needed_by, created_at, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending')""",
                (req.requester_id, req.vendor_id, requester["department"],
                 req.category, req.item_description, req.quantity,
                 req.unit_price_inr, req.priority, req.needed_by.isoformat(), now),
            )
            req_id = cursor.lastrowid
            conn.execute(
                """INSERT INTO approvals
                   (req_id, stage_no, approver_role, decision, assigned_at, decided_at)
                   VALUES (?, 1, ?, 'Pending', ?, NULL)""",
                (req_id, stages[0], now),
            )
            conn.execute(
                """INSERT INTO audit_log (req_id, event_at, actor, event_type, details)
                   VALUES (?, ?, ?, 'REQUEST_CREATED', ?)""",
                (req_id, now, f"Requester {req.requester_id}", "Created via prototype API"),
            )

        return {
            "req_id": req_id,
            "status": "Pending",
            "amount_inr": amount,
            "next_approver_role": stages[0],
            "required_approval_stages": stages,
        }
    finally:
        conn.close()


@app.get("/api/requisitions/{req_id}")
def get_requisition(req_id: int):

    if not DATABASE.exists():
        raise HTTPException(
            status_code=500,
            detail="Database not found"
        )

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    try:
        requisition = conn.execute(
            """
            SELECT *
            FROM requisitions
            WHERE req_id = ?
            """,
            (req_id,)
        ).fetchone()

        if requisition is None:
            raise HTTPException(
                status_code=404,
                detail="Requisition not found"
            )

        approvals = conn.execute(
            """
            SELECT stage_no, approver_role,
                   decision, assigned_at, decided_at
            FROM approvals
            WHERE req_id = ?
            ORDER BY stage_no
            """,
            (req_id,)
        ).fetchall()

        return {
            "requisition": dict(requisition),
            "approvals": [dict(a) for a in approvals]
        }

    finally:
        conn.close()



class ApprovalDecision(BaseModel):
    actor_user_id: int = Field(gt=0)
    decision: Literal["Approved", "Rejected"]


@app.patch("/api/requisitions/{req_id}/decision")
def decide_requisition(req_id: int, action: ApprovalDecision):
    """Demo approval routing. actor_user_id is NOT authentication."""
    if not DATABASE.exists():
        raise HTTPException(500, "Database not found")

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        actor = conn.execute(
            "SELECT role FROM users WHERE user_id = ?", (action.actor_user_id,)
        ).fetchone()
        if actor is None:
            raise HTTPException(404, "Approver not found")

        requisition = conn.execute(
            "SELECT amount_inr, status FROM requisitions WHERE req_id = ?", (req_id,)
        ).fetchone()
        if requisition is None:
            raise HTTPException(404, "Requisition not found")
        if requisition["status"] != "Pending":
            raise HTTPException(409, "Requisition is already finalized")

        stage = conn.execute(
            """SELECT approval_id, stage_no, approver_role
               FROM approvals WHERE req_id = ? AND decision = 'Pending'
               ORDER BY stage_no LIMIT 1""",
            (req_id,),
        ).fetchone()
        if stage is None:
            raise HTTPException(409, "No pending approval stage")
        if actor["role"] != stage["approver_role"]:
            raise HTTPException(403, "This user role cannot decide this stage")

        required_roles = ["Department Manager"]
        if requisition["amount_inr"] > 50_000:
            required_roles.append("Finance Controller")
        if requisition["amount_inr"] > 250_000:
            required_roles.append("Head of Procurement")

        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        next_role = None
        new_status = "Pending"
        with conn:
            updated = conn.execute(
                """UPDATE approvals SET decision = ?, decided_at = ?
                   WHERE approval_id = ? AND decision = 'Pending'""",
                (action.decision, now, stage["approval_id"]),
            )
            if updated.rowcount != 1:
                raise HTTPException(409, "Approval stage already decided")

            if action.decision == "Rejected":
                new_status = "Rejected"
            elif stage["stage_no"] < len(required_roles):
                next_role = required_roles[stage["stage_no"]]
                conn.execute(
                    """INSERT INTO approvals
                       (req_id, stage_no, approver_role, decision, assigned_at, decided_at)
                       VALUES (?, ?, ?, 'Pending', ?, NULL)""",
                    (req_id, stage["stage_no"] + 1, next_role, now),
                )
            else:
                new_status = "Approved"

            conn.execute(
                "UPDATE requisitions SET status = ? WHERE req_id = ?",
                (new_status, req_id),
            )
            conn.execute(
                """INSERT INTO audit_log (req_id, event_at, actor, event_type, details)
                   VALUES (?, ?, ?, ?, ?)""",
                (req_id, now, f"User {action.actor_user_id}",
                 "APPROVAL_DECIDED", f"Stage {stage['stage_no']}: {action.decision}"),
            )

        return {
            "req_id": req_id,
            "decision": action.decision,
            "status": new_status,
            "next_approver_role": next_role,
        }
    finally:
        conn.close()
