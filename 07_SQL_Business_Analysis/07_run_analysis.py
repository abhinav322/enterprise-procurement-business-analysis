"""Run Step 07 SQL investigations; export results and Power BI input CSVs.

Requires Python 3.10+; no pip installation. Run in Step 07 folder:
    python 07_build_analysis_db.py
    python 07_run_analysis.py
"""
from __future__ import annotations
import csv
import re
import sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent
DB = BASE / '07_meridian_analysis.db'
SQL = BASE / '07_business_analysis.sql'
OUTPUT_MD = BASE / '07_SQL_Results.md'
EXPORTS = BASE / 'powerbi_import'


def markdown_cell(value):
    if value is None:
        return '—'
    return str(value).replace('|', r'\|').replace('\n', ' ')


def markdown_table(columns, rows):
    if not rows:
        return '_No rows._'
    out = ['| ' + ' | '.join(columns) + ' |', '| ' + ' | '.join(['---'] * len(columns)) + ' |']
    out += ['| ' + ' | '.join(map(markdown_cell, row)) + ' |' for row in rows]
    return '\n'.join(out)


def run():
    if not DB.exists():
        raise FileNotFoundError(f'{DB.name} missing. First run: python 07_build_analysis_db.py')
    EXPORTS.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB)
    try:
        source = SQL.read_text(encoding='utf-8')
        blocks = re.split(r'(?=^-- QUERY: )', source, flags=re.MULTILINE)
        reports = []
        for block in blocks:
            if not block.startswith('-- QUERY: '):
                continue
            heading = block.splitlines()[0].replace('-- QUERY: ', '', 1)
            query = '\n'.join(block.splitlines()[1:]).strip()
            if not query:
                continue
            cursor = conn.execute(query)
            cols = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            reports.append((heading, cols, rows))
        text = ['# Step 07 — SQL Analysis Results',
                '\n**All observations use synthetic data.** Reporting snapshot: 9 November 2026, 12:00 UTC. '
                'Approval SLA threshold of 48 hours is illustrative.\n']
        for heading, columns, rows in reports:
            text.append(f'## {heading}\n')
            text.append(markdown_table(columns, rows) + '\n')
        OUTPUT_MD.write_text('\n'.join(text), encoding='utf-8')
        print(f'Executed {len(reports)} analytical SQL queries.\n')
        for heading, columns, rows in reports:
            print(heading, f'({len(rows)} rows)')
            for row in rows[:4]:
                print('   ', ' | '.join(map(str, row)))
        print('\nDetailed tables saved to', OUTPUT_MD.name)

        # Flat tables preserve identifiers so we can model relationships in Power BI next.
        exports = ['users','vendors','requisitions','approvals', 'purchase_orders','goods_receipts','invoices']
        for table in exports:
            cursor = conn.execute(f'SELECT * FROM {table} ORDER BY 1')
            columns = [d[0] for d in cursor.description]
            rows = cursor.fetchall()
            path = EXPORTS / f'{table}.csv'
            with path.open('w', encoding='utf-8-sig', newline='') as output:
                writer = csv.writer(output)
                writer.writerow(columns)
                writer.writerows(rows)
        print(f'Exported {len(exports)} related CSV tables to powerbi_import/')
    finally:
        conn.close()


if __name__ == '__main__':
    run()
