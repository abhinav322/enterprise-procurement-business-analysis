-- MERIDIAN | STEP 06: SMALL, HAND-CHECKED SYNTHETIC DATASET
-- This is only for verifying table relationships and approval boundaries.
-- Step 07 will use a larger dataset for real SQL exploration.
INSERT INTO users (user_id,full_name,department,role) VALUES
 (1,'Asha Raman','IT','Employee'),(2,'Ravi Shah','Operations','Employee'),
 (3,'Meera Rao','Marketing','Employee'),(4,'Karan Nair','Finance','Employee'),
 (5,'Priya Sen','Facilities','Employee'),(6,'Dev Roy','Human Resources','Employee'),
 (7,'Isha Patel','IT','Employee'),(10,'Department Manager Demo','Operations','Department Manager'),
 (11,'Finance Controller Demo','Finance','Finance Controller'),
 (12,'Procurement Head Demo','Procurement','Head of Procurement');
INSERT INTO vendors (vendor_id,vendor_name,category,region,is_active) VALUES
 (1,'ByteBridge Technologies','Hardware','Bengaluru',1),
 (2,'CloudRiver Licensing','Software','Pune',1),
 (3,'Northstar Advisory','Professional Services','Bengaluru',1),
 (4,'UrbanSpace Supplies','Facilities','Bengaluru',1),
 (5,'BrandSpring Studio','Marketing','Mumbai',1);

-- req 1004 = exactly 50,000; req 1005 = exactly 250,000;
-- req 1006 = 250,001: deliberately chosen to verify boundary rules.
INSERT INTO requisitions
 (req_id,requester_id,vendor_id,department,category,item_description,quantity,
  unit_price_inr,priority,needed_by,created_at,status) VALUES
 (1001,1,1,'IT','Hardware','Laptop accessories',2,20000,'Normal','2026-11-16','2026-10-29T09:00:00Z','Approved'),
 (1002,2,2,'Operations','Software','Software licences',2,60000,'Urgent','2026-11-18','2026-11-05T09:00:00Z','Pending'),
 (1003,3,5,'Marketing','Marketing','Campaign production',3,100000,'Normal','2026-11-08','2026-10-24T09:00:00Z','Approved'),
 (1004,4,3,'Finance','Professional Services','Compliance review',1,50000,'Normal','2026-11-23','2026-11-06T09:00:00Z','Approved'),
 (1005,7,1,'IT','Hardware','Workstations',5,50000,'Normal','2026-11-15','2026-10-28T09:00:00Z','Approved'),
 (1006,6,3,'Human Resources','Professional Services','Training programme',1,250001,'Normal','2026-11-28','2026-11-02T09:00:00Z','Pending'),
 (1007,5,4,'Facilities','Facilities','Office supplies',4,6000,'Normal','2026-11-21','2026-11-04T09:00:00Z','Pending'),
 (1008,3,5,'Marketing','Marketing','Event banners',2,30000,'Normal','2026-11-19','2026-10-31T09:00:00Z','Rejected'),
 (1009,1,1,'IT','Hardware','IT peripherals',2,42500,'Normal','2026-11-20','2026-10-30T09:00:00Z','Approved');

INSERT INTO approvals (approval_id,req_id,stage_no,approver_role,decision,assigned_at,decided_at) VALUES
 (1,1001,1,'Department Manager','Approved','2026-10-29T09:00:00Z','2026-10-29T12:00:00Z'),
 (2,1002,1,'Department Manager','Approved','2026-11-05T09:00:00Z','2026-11-05T12:00:00Z'),
 (3,1002,2,'Finance Controller','Pending','2026-11-05T12:00:00Z',NULL),
 (4,1003,1,'Department Manager','Approved','2026-10-24T09:00:00Z','2026-10-24T12:00:00Z'),
 (5,1003,2,'Finance Controller','Approved','2026-10-24T12:00:00Z','2026-10-25T13:00:00Z'),
 (6,1003,3,'Head of Procurement','Approved','2026-10-25T13:00:00Z','2026-10-26T10:00:00Z'),
 (7,1004,1,'Department Manager','Approved','2026-11-06T09:00:00Z','2026-11-06T12:00:00Z'),
 (8,1005,1,'Department Manager','Approved','2026-10-28T09:00:00Z','2026-10-28T12:00:00Z'),
 (9,1005,2,'Finance Controller','Approved','2026-10-28T12:00:00Z','2026-10-29T13:00:00Z'),
 (10,1006,1,'Department Manager','Approved','2026-11-02T09:00:00Z','2026-11-02T12:00:00Z'),
 (11,1006,2,'Finance Controller','Approved','2026-11-02T12:00:00Z','2026-11-03T09:00:00Z'),
 (12,1006,3,'Head of Procurement','Pending','2026-11-03T09:00:00Z',NULL),
 (13,1007,1,'Department Manager','Pending','2026-11-04T09:00:00Z',NULL),
 (14,1008,1,'Department Manager','Approved','2026-10-31T09:00:00Z','2026-10-31T12:00:00Z'),
 (15,1008,2,'Finance Controller','Rejected','2026-10-31T12:00:00Z','2026-11-01T11:00:00Z'),
 (16,1009,1,'Department Manager','Approved','2026-10-30T09:00:00Z','2026-10-30T12:00:00Z'),
 (17,1009,2,'Finance Controller','Approved','2026-10-30T12:00:00Z','2026-10-31T10:00:00Z');

INSERT INTO purchase_orders (po_id,req_id,vendor_id,ordered_at,promised_delivery_at,actual_delivery_at,status) VALUES
 (2001,1001,1,'2026-10-30T11:00:00Z','2026-11-06T18:00:00Z','2026-11-05T14:00:00Z','Delivered'),
 (2003,1003,5,'2026-10-27T10:00:00Z','2026-11-01T18:00:00Z','2026-11-04T11:00:00Z','Delivered'),
 (2004,1004,3,'2026-11-07T10:00:00Z','2026-11-18T18:00:00Z',NULL,'Open'),
 (2005,1005,1,'2026-10-30T10:00:00Z','2026-11-06T18:00:00Z','2026-11-06T11:00:00Z','Delivered'),
 (2009,1009,1,'2026-11-01T10:00:00Z','2026-11-09T18:00:00Z','2026-11-08T15:00:00Z','Delivered');
INSERT INTO goods_receipts (receipt_id,po_id,received_at,received_qty,accepted_qty) VALUES
 (3001,2001,'2026-11-05T14:00:00Z',2,2),
 (3003,2003,'2026-11-04T11:00:00Z',3,2),
 (3005,2005,'2026-11-06T11:00:00Z',5,5),
 (3009,2009,'2026-11-08T15:00:00Z',2,2);
INSERT INTO invoices (invoice_id,po_id,invoiced_at,invoice_qty,invoice_amount_inr,match_status,paid_at) VALUES
 (4001,2001,'2026-11-06T10:00:00Z',2,40000,'Matched',NULL),
 (4003,2003,'2026-11-05T10:00:00Z',3,300000,'Discrepancy',NULL),
 (4005,2005,'2026-11-07T10:00:00Z',5,250000,'Matched',NULL),
 (4009,2009,'2026-11-09T10:00:00Z',2,87000,'Discrepancy',NULL);
INSERT INTO audit_log (req_id,event_at,actor,event_type,details)
 SELECT req_id,created_at,'Sample Data Generator','REQUEST_CREATED','Synthetic request for schema demonstration'
 FROM requisitions;
