
import sqlite3

# Connect to our API database
conn = sqlite3.connect("meridian_api.db")

# Find the Head of Procurement
cursor = conn.execute("""
    SELECT user_id, role
    FROM users
    WHERE role LIKE '%Procurement%'
""")

for row in cursor.fetchall():
    print("User ID:", row[0], "| Role:", row[1])

conn.close()
