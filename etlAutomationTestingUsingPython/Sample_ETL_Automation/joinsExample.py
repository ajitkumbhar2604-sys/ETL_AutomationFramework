from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("JOIN Practice") \
    .getOrCreate()

source_data = [
    (101, "Ajit", "Pune"),
    (102, "Rahul", "Mumbai"),
    (103, "Amit", "Delhi"),
    (104, "Sneha", "Pune"),
    (105, "Priya", "Nagpur")
]

source_columns = ["customer_id", "name", "city"]

source_df = spark.createDataFrame(source_data, source_columns)

source_df.show()

target_data = [
    (101, "Ajit", "Pune"),
    (102, "Rahul", "Mumbai"),
    (104, "Sneha", "Pune"),
    (105, "Priya", "Nagpur")
]

target_df = spark.createDataFrame(target_data, source_columns)

target_df.show()

left_Anti = source_df.join(target_df, on = "customer_id", how = "anti")
left_Anti.show()