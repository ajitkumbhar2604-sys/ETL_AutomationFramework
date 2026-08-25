# Read the snowflake table using plain python

import snowflake.connector

conn = snowflake.connector.connect(
    user="AjitKumbhar",
    password="Greenstone@2026",
    account="jbafxgg-ic22052",
    warehouse="COMPUTE_WH",
    database="ETL_DB",
    schema="ETL_SCHEMA"
)

cursor = conn.cursor()

cursor.execute("""
    SELECT *
    FROM ETL_DB.ETL_SCHEMA.CUSTOMER_RECORDS
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
conn.close()