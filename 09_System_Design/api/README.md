# Procurement Requisition API Prototype

This is a **local FastAPI/SQLite prototype** implementing selected requirements for the fictional Meridian Global Services procurement workflow. It is not a deployed enterprise application.

## Supported endpoints

| Method | Route | Behaviour |
| --- | --- | --- |
| `POST` | `/api/requisitions` | Validates and creates a requisition and starts the approval workflow |
| `GET` | `/api/requisitions/{req_id}` | Retrieves a requisition and its approval history |
| `PATCH` | `/api/requisitions/{req_id}/decision` | Records an authorised-role stage approval or rejection |

Approval policy in this case study:

- Amount up to ₹50,000: Department Manager
- ₹50,001–₹250,000: Department Manager, then Finance Controller
- Above ₹250,000: Department Manager, Finance Controller, then Head of Procurement

Stage ordering, finalised-request protection, requester/vendor existence checks, and positive quantity/unit-price validation are implemented in `main.py`.

## Run locally

After rebuilding the analysis database as described in the [repository README](../../README.md), run from the **repository root**:

```powershell
python -m pip install -r requirements.txt
Copy-Item 07_SQL_Business_Analysis/07_meridian_analysis.db 09_System_Design/api/meridian_api.db
Set-Location 09_System_Design/api
python -m uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` for Swagger UI. See `example_request.json` for an example request payload; its `needed_by` date must be a future date when the request is submitted.

The dedicated `meridian_api.db` is a copy: API requests do **not** modify the fixed SQL/Power BI reporting baseline.

## Test scripts

- `test_approval_boundaries.py` checks routing at selected monetary thresholds.
- `test_invalid_requisitions.py` checks invalid requester/vendor IDs and verifies that no record was created.
- `check_approver.py` inspects the demo approver-role records.

The two HTTP test scripts expect a running local API and contain example request dates, which must remain in the future when tests are executed.

## Limitations

The submitted approver ID is compared with the user's stored role, but **there is no authentication of the caller**. This prototype is not suitable for exposure to the public internet. Production access control, comprehensive audit security, notifications, ERP integration, deployment, and end-user sign-off are outside the implemented scope.
