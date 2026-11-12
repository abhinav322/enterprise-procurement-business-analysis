
import json
import sqlite3
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from datetime import date, timedelta


DATABASE = Path(__file__).resolve().parent / "meridian_api.db"
API_URL = "http://127.0.0.1:8000/api/requisitions"

def count_requisitions():
    with sqlite3.connect(DATABASE) as conn:
        return conn.execute(
            "SELECT COUNT(*) FROM requisitions"
        ).fetchone()[0]

def test_invalid_request(field, invalid_id, expected_error):
    payload = {
        "requester_id": 1,
        "vendor_id": 1,
        "category": "Hardware",
        "item_description": "Invalid ID test",
        "quantity": 2,
        "unit_price_inr": 15000,
        "priority": "Normal",
        "needed_by": (date.today() + timedelta(days=30)).isoformat()

    }

    payload[field] = invalid_id

    before = count_requisitions()

    request = Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urlopen(request) as response:
            status = response.status
            result = json.loads(response.read())
    except HTTPError as error:
        status = error.code
        result = json.loads(error.read())

    after = count_requisitions()

    passed = (
        400 <= status < 500
        and result.get("detail") == expected_error
        and before == after
    )

    print(
        f"{field}: {'PASS' if passed else 'FAIL'} "
        f"| HTTP {status} "
        f"| Records created: {after - before}"
    )

test_invalid_request(
    "requester_id", 99999, "Requester not found"
)

test_invalid_request(
    "vendor_id", 99999, "Vendor not found"
)
