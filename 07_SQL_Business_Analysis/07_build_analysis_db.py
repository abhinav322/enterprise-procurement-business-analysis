"""Build a reproducible, SYNTHETIC procurement analytics database from Step 06.

Run: python 07_build_analysis_db.py
Does not modify the original Step 06 demo database.
Uses only the Python standard library.
"""
from __future__ import annotations
import random
import shutil
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
SOURCE = BASE / 'reference' / '06_meridian_demo.db'
OUTPUT = BASE / '07_meridian_analysis.db'
AS_OF = datetime(2026, 11, 9, 12, 0, tzinfo=timezone.utc)
RNG = random.Random(20261109)


def stamp(t: datetime) -> str:
    return t.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def random_between(start: datetime, end: datetime) -> datetime:
    return start + timedelta(seconds=RNG.randint(0, int((end - start).total_seconds())))


def next_dt(base: datetime, min_hours: int, max_hours: int) -> datetime:
    return base + timedelta(hours=RNG.randint(min_hours, max_hours))


def build() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f'Missing seed database: {SOURCE}')
    shutil.copyfile(SOURCE, OUTPUT)
    db = sqlite3.connect(OUTPUT)
    db.execute('PRAGMA foreign_keys = ON;')
    try:
        with db:
            db.executemany('INSERT INTO vendors (vendor_id,vendor_name,category,region,is_active) VALUES (?,?,?,?,1)', [
                (6,'NimbleTech Systems','Hardware','Hyderabad'),
                (7,'Atlas SaaS Solutions','Software','Bengaluru'),
                (8,'Cedar Consulting','Professional Services','Delhi'),
                (9,'Prime Facilities Co','Facilities','Pune'),
                (10,'Spark Creative Agency','Marketing','Bengaluru'),
            ])
            vendor_by_category = {
                'Hardware': [1, 6], 'Software': [2, 7],
                'Professional Services': [3, 8], 'Facilities': [4, 9], 'Marketing': [5, 10],
            }
            people = [
                (1, 'IT'), (2, 'Operations'), (3, 'Marketing'),
                (4, 'Finance'), (5, 'Facilities'), (6, 'Human Resources'), (7, 'IT'),
            ]
            categories = {
                'IT': ['Hardware','Software'],
                'Operations': ['Software','Facilities','Professional Services'],
                'Marketing': ['Marketing','Software','Professional Services'],
                'Finance': ['Software','Professional Services'],
                'Facilities': ['Facilities','Hardware'],
                'Human Resources': ['Professional Services','Software'],
            }
            descriptions = {
                'Hardware': 'IT hardware and peripherals', 'Software': 'Software subscription and licences',
                'Professional Services': 'External consulting engagement',
                'Facilities': 'Office maintenance supplies', 'Marketing': 'Brand and campaign services',
            }
            approval_roles = ['Department Manager','Finance Controller','Head of Procurement']
            approval_id, po_id, receipt_id, invoice_id = 18, 2010, 3010, 4010
            created_start = datetime(2026, 3, 1, 8, 0, tzinfo=timezone.utc)
            created_end = datetime(2026, 10, 17, 17, 0, tzinfo=timezone.utc)
            pending_start = datetime(2026, 11, 1, 8, 0, tzinfo=timezone.utc)
            pending_end = datetime(2026, 11, 5, 7, 0, tzinfo=timezone.utc)
            recent_pending_end = datetime(2026, 11, 8, 18, 0, tzinfo=timezone.utc)

            for req_id in range(1010, 1410):  # exactly 400 additional purchase requests
                requester_id, department = RNG.choice(people)
                category = RNG.choice(categories[department])
                vendor_id = RNG.choice(vendor_by_category[category])
                qty = RNG.randint(1, 12)
                unit_price = RNG.choice([1800, 3000, 4500, 7500, 12000, 20000, 32000, 50000, 75000])
                amount = qty * unit_price
                priority = 'Urgent' if RNG.random() < 0.16 else 'Normal'
                outcome = RNG.choices(['Approved','Rejected','Pending'], weights=[76, 10, 14], k=1)[0]
                required_stages = 1 if amount <= 50000 else (2 if amount <= 250000 else 3)
                pending_at = RNG.randint(1, required_stages) if outcome == 'Pending' else 0
                if outcome == 'Pending':
                    # Some requests are recent; later-stage approvals need time for earlier decisions.
                    created = random_between(pending_start, recent_pending_end if pending_at == 1 else pending_end)
                else:
                    created = random_between(created_start, created_end)
                needed_by = created + timedelta(days=RNG.randint(7, 28))
                db.execute('''INSERT INTO requisitions
                    (req_id,requester_id,vendor_id,department,category,item_description,quantity,unit_price_inr,priority,needed_by,created_at,status)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                    (req_id,requester_id,vendor_id,department,category,descriptions[category],qty,unit_price,
                     priority,needed_by.strftime('%Y-%m-%d'),stamp(created),outcome))
                db.execute('''INSERT INTO audit_log(req_id,event_at,actor,event_type,details) VALUES(?,?,?,?,?)''',
                           (req_id,stamp(created),'Synthetic data generator','REQUEST_CREATED','Synthetic portfolio transaction'))

                reject_at = RNG.randint(1, required_stages) if outcome == 'Rejected' else 0
                assigned = created
                final_decision_time = None
                for stage in range(1, required_stages + 1):
                    # Once rejected/pending, no later approval stage is created.
                    decision = ('Rejected' if stage == reject_at else 'Pending' if stage == pending_at else 'Approved')
                    if decision == 'Pending':
                        decided = None
                    else:
                        # Some review stages deliberately exceed the illustrative 48-hour SLA.
                        decided = next_dt(assigned, 3, 24 if outcome == 'Pending' else 120)
                        if decided >= AS_OF:
                            raise AssertionError('Generated decision after the as-of date')
                        final_decision_time = decided
                    db.execute('''INSERT INTO approvals
                        (approval_id,req_id,stage_no,approver_role,decision,assigned_at,decided_at)
                        VALUES (?,?,?,?,?,?,?)''',
                        (approval_id,req_id,stage,approval_roles[stage - 1],decision,stamp(assigned),
                         stamp(decided) if decided else None))
                    approval_id += 1
                    if decision == 'Pending':
                        break
                    db.execute('''INSERT INTO audit_log(req_id,event_at,actor,event_type,details)
                        VALUES (?,?,?,?,?)''',
                        (req_id,stamp(decided),approval_roles[stage - 1],f'APPROVAL_{decision.upper()}',
                         f'Stage {stage}: simulated {decision.lower()} decision'))
                    if decision == 'Rejected':
                        break
                    assigned = decided

                if outcome != 'Approved':
                    continue
                assert final_decision_time is not None
                ordered = next_dt(final_decision_time, 3, 48)
                promised = ordered + timedelta(days=RNG.randint(4, 15))
                proposed_actual = promised + timedelta(hours=RNG.randint(-120, 30))
                # Historical POs >30 days past promise are resolved in this small case study.
                # Recent POs can remain open (including some overdue).
                resolved_historical = promised < AS_OF - timedelta(days=30)
                delivered = proposed_actual <= AS_OF and (resolved_historical or RNG.random() < 0.77)
                actual = proposed_actual if delivered else None
                db.execute('''INSERT INTO purchase_orders
                    (po_id,req_id,vendor_id,ordered_at,promised_delivery_at,actual_delivery_at,status)
                    VALUES (?,?,?,?,?,?,?)''',
                    (po_id,req_id,vendor_id,stamp(ordered),stamp(promised),stamp(actual) if actual else None,
                     'Delivered' if delivered else 'Open'))
                db.execute('''INSERT INTO audit_log(req_id,event_at,actor,event_type,details)
                    VALUES (?,?,?,?,?)''',
                    (req_id,stamp(ordered),'Procurement','PO_CREATED','Synthetic purchase order issued'))
                if delivered:
                    # Intentionally include acceptance shortfalls for 3-way-match investigation.
                    accepted = qty if RNG.random() < 0.96 or qty == 1 else RNG.randint(1, qty - 1)
                    db.execute('''INSERT INTO goods_receipts(receipt_id,po_id,received_at,received_qty,accepted_qty)
                        VALUES (?,?,?,?,?)''', (receipt_id,po_id,stamp(actual),qty,accepted))
                    receipt_id += 1
                    invoice_date = next_dt(actual, 2, 48)
                    if invoice_date <= AS_OF:
                        mismatch_type = RNG.choices(['none','amount','quantity'], weights=[88, 7, 5], k=1)[0]
                        inv_qty = qty if mismatch_type != 'quantity' else max(1, qty - 1)
                        inv_amt = inv_qty * unit_price
                        if mismatch_type == 'amount':
                            inv_amt += RNG.choice([1200, 3000, 8000])
                        match = ('Matched' if accepted == qty and inv_qty == qty and inv_amt == amount else 'Discrepancy')
                        db.execute('''INSERT INTO invoices
                            (invoice_id,po_id,invoiced_at,invoice_qty,invoice_amount_inr,match_status,paid_at)
                            VALUES (?,?,?,?,?,?,?)''',
                            (invoice_id,po_id,stamp(invoice_date),inv_qty,inv_amt,match,
                             stamp(next_dt(invoice_date, 24, 72)) if match == 'Matched' and
                                  invoice_date + timedelta(hours=72) < AS_OF and RNG.random() < 0.62 else None))
                        invoice_id += 1
                elif RNG.random() < 0.08 and ordered + timedelta(days=2) < AS_OF:
                    # An early invoice has no receipt yet; it must not count as matched.
                    invoice_date = next_dt(ordered, 24, 48)
                    db.execute('''INSERT INTO invoices
                        (invoice_id,po_id,invoiced_at,invoice_qty,invoice_amount_inr,match_status,paid_at)
                        VALUES (?,?,?,?,?,?,NULL)''',
                        (invoice_id,po_id,stamp(invoice_date),qty,amount,'Awaiting Receipt'))
                    invoice_id += 1
                po_id += 1
        db.commit()
        failures = db.execute('PRAGMA foreign_key_check;').fetchall()
        if failures:
            raise AssertionError(f'Foreign-key failures: {failures}')
        count = db.execute('SELECT COUNT(*) FROM requisitions').fetchone()[0]
        assert count == 409, f'Expected 409 requests, got {count}'
        # All approved requests have every necessary approval stage approved.
        bad_approved = db.execute('''SELECT r.req_id FROM requisitions r
            WHERE r.status='Approved' AND (SELECT COUNT(*) FROM approvals a WHERE a.req_id=r.req_id AND a.decision='Approved')
            <> CASE WHEN r.amount_inr<=50000 THEN 1 WHEN r.amount_inr<=250000 THEN 2 ELSE 3 END''').fetchall()
        if bad_approved:
            raise AssertionError(f'Invalid approval histories: {bad_approved[:5]}')
        print('Created:', OUTPUT)
        for table in ['users','vendors','requisitions','approvals','purchase_orders','goods_receipts','invoices','audit_log']:
            print(f'{table:17} {db.execute("SELECT COUNT(*) FROM " + table).fetchone()[0]:>6}')
        print('Foreign-key check: PASS')
        print('Approved routing check: PASS')
        print('Synthetic data only | As-of 2026-11-09 12:00 UTC')
    finally:
        db.close()


if __name__ == '__main__':
    build()
