data = [
    (101, "Ajit", "Kumbhar", 35, "Pune", 85000, "IT", "Y"),
    (102, "Rahul", "Patil", 30, "Mumbai", 65000, "Finance", "Y"),
    (103, "Amit", "Sharma", 28, "Delhi", 55000, "HR", "N"),
    (104, "Sneha", "Joshi", 32, "Pune", 72000, "IT", "Y"),
    (105, "Priya", "Kulkarni", 27, "Nagpur", 50000, "Marketing", "Y"),
    (106, "Rohit", "Verma", 40, "Bangalore", 98000, "IT", "N"),
    (107, "Neha", "Gupta", 31, "Hyderabad", 67000, "Finance", "Y"),
    (108, "Suresh", "Patel", 45, "Ahmedabad", 105000, "Management", "Y"),
    (109, "Kiran", "Reddy", 29, "Hyderabad", 60000, "HR", "N"),
    (110, "Pooja", "Singh", 33, "Chennai", 75000, "IT", "Y")
]

columns = [
    "emp_id",
    "first_name",
    "last_name",
    "age",
    "city",
    "salary",
    "department",
    "is_active"
]

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ETL Practice") \
    .getOrCreate()

df = spark.createDataFrame(data, columns)

df.show()