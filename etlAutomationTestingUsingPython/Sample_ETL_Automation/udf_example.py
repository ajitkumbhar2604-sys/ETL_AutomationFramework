from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

spark = SparkSession.builder \
    .appName("UDF Example") \
    .getOrCreate()

data = [
    (101, "Ajit", 35),
    (102, "Rahul", 28),
    (103, "Amit", 42)
]

columns = ["emp_id", "emp_name", "age"]

df = spark.createDataFrame(data, columns)

#df.show()

#python function to verify the age category
def age_category(age):
    if age >= 40:
        return "Senior"
    elif age >= 30:
        return "Mid"
    else:
        return "Junior"

# Convert above Python funtion into spark UDF

age_category_udf = udf(age_category, StringType())

age_cat_df = df.withColumn("age_Category", age_category_udf(df.age))
age_cat_df.show()