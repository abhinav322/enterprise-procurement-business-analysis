
import json
from urllib.request import Request, urlopen

API_URL = "http://127.0.0.1:8000/api/requisitions"

test_cases = [
    (50000, ["Department Manager"]),
    (50001, ["Department Manager", "Finance Controller"]),
    (250000, ["Department Manager", "Finance Controller"]),
]

for amount, expected_stages in test_cases:

    payload = {
        "requester_id": 1,
        "vendor_id": 1,
        "category": "Hardware",
        "item_description": f"Boundary test purchase {amount}",
        "quantity": 1,
        "unit_price_inr": amount,
        "priority": "Normal",
        "needed_by": "2026-12-20"
    }

    request = Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urlopen(request) as response:
        result = json.loads(response.read())
        status_code = response.status

    actual_stages = result["required_approval_stages"]

    passed = (
        status_code == 201
        and actual_stages == expected_stages
        and result["amount_inr"] == amount
    )

    print(
        f"Amount: INR {amount:,} | "
        f"HTTP: {status_code} | "
        f"Result: {'PASS' if passed else 'FAIL'}"
    )

    if not passed:
        print("Expected:", expected_stages)
        print("Actual:", actual_stages)
