STEP 9.2 — FIRST API ENDPOINT (hands-on exercise)

1. Create the folder 09_System_Design/api in your main Enterprise Procurement BA Project folder.
2. Put main.py and example_request.json in that api folder.
3. From your extracted Step 7 folder, COPY 07_meridian_analysis.db into the api folder.
4. Rename the copied database meridian_api.db (do not rename or modify the original database used for Power BI).
5. In VS Code, open a terminal in api and run:
   python -m pip install fastapi uvicorn
   python -m uvicorn main:app --reload
6. In your browser open http://127.0.0.1:8000/docs
7. Expand POST /api/requisitions -> Try it out.
8. Paste the JSON from example_request.json and select Execute.
9. Check for HTTP 201 and req_id/status/approval stages in the response.

This is a learning prototype with no authentication or production-grade safeguards.
The first approval stage is immediately pending; later stages activate after earlier approvals.
Next step: implement an API for reading back a requisition, then approval decisions.
