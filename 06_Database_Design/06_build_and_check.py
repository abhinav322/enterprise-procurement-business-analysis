"""STEP 06 — Creates a local SQLite database without extra pip installs.
Run from this folder: python 06_build_and_check.py
Every run starts from the clean schema and small synthetic sample data.
"""
from pathlib import Path
import sqlite3
ROOT = Path(__file__).resolve().parent
DB = ROOT / '06_meridian_demo.db'
if DB.exists():
    DB.unlink()
with sqlite3.connect(DB) as conn:
    conn.execute('PRAGMA foreign_keys = ON')
    conn.executescript((ROOT / '06_schema.sql').read_text(encoding='utf-8'))
    conn.executescript((ROOT / '06_sample_data.sql').read_text(encoding='utf-8'))
    issues = conn.execute('PRAGMA foreign_key_check').fetchall()
    assert not issues, f'Foreign-key problems: {issues}'
    expected = {'users':10,'vendors':5,'requisitions':9,'approvals':17,
                'purchase_orders':5,'goods_receipts':4,'invoices':4,'audit_log':9}
    print('MERIDIAN DATABASE — TABLE COUNTS')
    for table, correct in expected.items():
        n = conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
        assert n == correct, f'Unexpected number of {table}: {n}'
        print(f'  {table:18s} {n}')
    print('\nAPPROVAL THRESHOLD EXAMPLES (request / amount / stages)')
    for row in conn.execute("""SELECT r.req_id, r.amount_inr, COUNT(a.approval_id)
                               FROM requisitions r JOIN approvals a ON r.req_id=a.req_id
                               WHERE r.req_id IN (1004,1005,1006)
                               GROUP BY r.req_id ORDER BY r.req_id"""):
        print(' ', *row, sep='  ')
    print('\nPASSED: foreign keys, sample row counts, and amount boundaries.')
    print('Database created:', DB)
