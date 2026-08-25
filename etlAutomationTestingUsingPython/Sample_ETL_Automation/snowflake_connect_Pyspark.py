# Connect with snowflake df and access the  records from
#table which is already created in snowflake
#ETL_DB -> ETL_Schema -> CUTOMER_RECORDS

from pyspark.sql import SparkSession
import snowflake.connector


# Create Spark session
spark = SparkSession.builder \
    .appName("Snowflake Data") \
    .getOrCreate()

# Snowflake connection
conn = snowflake.connector.connect(
    user="AjitKumbhar",
    password="Greenstone@2026",
    account="jbafxgg-ic22052",
    warehouse="COMPUTE_WH",
    database="ETL_DB",
    schema="ETL_SCHEMA"
)

cursor = conn.cursor()

# Read data
cursor.execute("""
    SELECT *
    FROM ETL_DB.ETL_SCHEMA.CUSTOMER_RECORDS
""")

# Get records
rows = cursor.fetchall()

# Get column names
columns = [column[0] for column in cursor.description]

print("Columns:", columns)
print("All data in Rows:", rows)

# Create PySpark DataFrame
customer_df = spark.createDataFrame(rows, columns)

# Display
customer_df.show()

# Schema
#customer_df.printSchema()

print("Record Count:", customer_df.count())

cursor.close()
conn.close()

spark.stop()