"""Non-destructive validation for Step 07 synthetic case study. Run: python 07_validate_dataset.py."""
from pathlib import Path
import sqlite3

DB = Path(__file__).resolve().parent / '07_meridian_analysis.db'
if not DB.exists():
    raise SystemExit('Run python 07_build_analysis_db.py first')
c = sqlite3.connect(DB)
c.execute('PRAGMA foreign_keys = ON;')
checks = {
    'exactly 409 requests': 'SELECT COUNT(*)-409 FROM requisitions',
    'all foreign keys valid': 'SELECT COUNT(*) FROM pragma_foreign_key_check',
    'approved requests have fully approved stage count': '''
       SELECT COUNT(*) FROM requisitions r WHERE r.status='Approved' AND
       (SELECT COUNT(*) FROM approvals a WHERE a.req_id=r.req_id AND a.decision='Approved')
       <> CASE WHEN r.amount_inr<=50000 THEN 1 WHEN r.amount_inr<=250000 THEN 2 ELSE 3 END''',
    'approved requests have a PO': '''SELECT COUNT(*) FROM requisitions r
       LEFT JOIN purchase_orders po ON po.req_id=r.req_id
       WHERE r.status='Approved' AND po.po_id IS NULL''',
    'non-approved requests have no PO': '''SELECT COUNT(*) FROM purchase_orders po
       JOIN requisitions r ON r.req_id=po.req_id WHERE r.status<>'Approved' ''',
    'PO vendor matches request vendor': '''SELECT COUNT(*) FROM purchase_orders po
       JOIN requisitions r ON r.req_id=po.req_id WHERE po.vendor_id<>r.vendor_id''',
    'delivered order has a receipt': '''SELECT COUNT(*) FROM purchase_orders po
       LEFT JOIN goods_receipts gr ON gr.po_id=po.po_id
       WHERE po.status='Delivered' AND gr.receipt_id IS NULL''',
    'open order has no actual delivery': '''SELECT COUNT(*) FROM purchase_orders
       WHERE status='Open' AND actual_delivery_at IS NOT NULL''',
    'invoice statuses agree with simplified 3-way match': '''
       SELECT COUNT(*) FROM invoices i
       JOIN purchase_orders po ON po.po_id=i.po_id
       JOIN requisitions r ON r.req_id=po.req_id
       LEFT JOIN goods_receipts gr ON gr.po_id=po.po_id
       WHERE (i.match_status='Matched') !=
       (gr.receipt_id IS NOT NULL AND gr.accepted_qty=r.quantity AND
        i.invoice_qty=r.quantity AND i.invoice_amount_inr=r.amount_inr)
       OR (i.match_status='Awaiting Receipt' AND gr.receipt_id IS NOT NULL)''',
    'no future decisions': '''SELECT COUNT(*) FROM approvals
       WHERE decided_at>'2026-11-09T12:00:00Z' ''',
    'no future purchase orders': '''SELECT COUNT(*) FROM purchase_orders
       WHERE ordered_at>'2026-11-09T12:00:00Z' ''',
    'no future invoices': '''SELECT COUNT(*) FROM invoices
       WHERE invoiced_at>'2026-11-09T12:00:00Z' OR paid_at>'2026-11-09T12:00:00Z' ''',
    'requisition status matches approval outcome': '''SELECT COUNT(*) FROM requisitions r WHERE
       (r.status='Pending' AND NOT EXISTS (SELECT 1 FROM approvals a WHERE a.req_id=r.req_id AND a.decision='Pending'))
       OR (r.status='Rejected' AND NOT EXISTS (SELECT 1 FROM approvals a WHERE a.req_id=r.req_id AND a.decision='Rejected'))
       OR (r.status='Approved' AND EXISTS (SELECT 1 FROM approvals a WHERE a.req_id=r.req_id AND a.decision<>'Approved'))''',
}
failed = False
for name, query in checks.items():
    issues = c.execute(query).fetchone()[0]
    print(('PASS' if issues == 0 else 'FAIL') + f'  {name} (issues={issues})')
    failed |= issues != 0
c.close()
if failed:
    raise SystemExit('VALIDATION FAILED — check issues above')
print(f'\nALL CHECKS PASSED ({len(checks)} checks)')
