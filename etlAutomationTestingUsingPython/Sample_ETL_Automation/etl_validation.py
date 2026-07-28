#print("Sample ETL automation framework")
from idlelib import query

import numpy as np
import pandas as pd
from pandasql import sqldf
from pip._internal.models import target_python


#source_path = "C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\customers_records_S.csv"
#target_path = "C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\customers_records_T.csv"

#Sample ETL validation
def read_file(file_path, file_type):
    file_type = file_type.lower()
    if file_type == "csv":
        df = pd.read_csv(file_path)
    elif file_type == "excel":
        df = pd.read_excel(file_path)
    elif file_type == "parquet":
        df = pd.read_parquet(file_path)
    else:
        print("File type not supported")
    return df


#first check as count check in both source and target file
def check_count(source,target):
    source_count = source.shape[0]
    target_count = target.shape[0]

    if source_count == target_count:
        print("Count is matching in Source and Target")
    else:
        print("Count is not matching in Source and Target")
        print("Difference is :", abs(source_count - target_count))

        #Find records present in Source but missing in Target (Recommended)
        mismatched_records = source[~source['customer_id'].isin(target['customer_id'])]
        print("records present in Source but missing in Target: ")
        print(mismatched_records)

        #Records present in Target but missing in Source
        extra_records = target[~target['customer_id'].isin(source['customer_id'])]
        print("Records present in Target but missing in Source: ")
        print(extra_records)

#column count matching/mismatching
def check_column_count(source, target):
    if source.shape[1] == target.shape[1]:
        print("PASS : Column count is matching")
    else:
        print("FAIL : Column count mismatch")
        print("Source:", source.shape[1])
        print("Target:", target.shape[1])

#unction to check duplicates in target
def check_duplicates(target_df, pkey):
    unique_target_df = target_df.drop_duplicates(subset=pkey).shape[0]
    original_count_df = target_df.shape[0]
    duplicate_count = original_count_df - unique_target_df
    duplicate_df = target_df[target_df.duplicated(subset=pkey, keep=False)]
    if duplicate_count == 0:
        print("No Duplicate records present in Target")
    else:
        print("Duplicate records present in Target")
        print("FAIL : Duplicate Records Found")
        print(f"Duplicate Count : {duplicate_count}")

        #duplicate_df = target_df[target_df.duplicated(subset=pkey, keep=False)]

        print("\nDuplicate Records:")
        print(duplicate_df)
    return duplicate_count, duplicate_df

#NUll check function
def check_null(target_df, null_column):
    null_rows = target_df[target_df[null_column].isnull()]
    if null_rows.shape[0] > 0:
        print("Null rows present in Target")
    else:
        print("NO Null rows present in Target")

#Data compare
#this function is only applicable for 2 identical dataframes, then only .compare() will work
def data_compare(source, target):
    failed = source.compare(target)
    if failed.shape[0] > 0:
        print("Data is not present in Target")
        print("Failed...!!!")
    else:
        print("Data is matching...!!!")

#alternate solution for Data compare,
#using SQLdf
def data_compare_sql(source, target):
    query = """select * from source except select * from target
                union all
                select * from target except select * from source"""
    failed = sqldf(query)
    if failed.shape[0] > 0:
        print("Data is not present in Target")
        print("Failed...!!!")
    else:
        print("Data is matching...!!!")

#function to identify the out of range, as Data quality check not Data validation check
# we can use this kind of functon to identify the range like age>=18 and age<=100, Gender identification like Male and Female only,
# to find date range as well
def check_out_of_range(target_df, column, min_val, max_val):
    query = f"""
    select * from target_df where {column} < {min_val}
    OR {column} > {max_val}"""

    invalid_df = sqldf(query)
    if invalid_df.shape[0] > 0:
        print("Invalid records present in Target")
        print("Failed...!!!")
        print(invalid_df)
    else:
        print("All records are valid...!!!")




#Call the functions from here
source = read_file(r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\customers_records_S.csv", "csv")
#target = read_file(r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\customers_records_S.csv", file_type="csv")
target_duplicate_df = read_file(r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\customers_records_T_with_DuplicateRec.csv", file_type="csv")
target_range = read_file(r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\customers_records_S.csv", file_type="csv")

#check_count(source,target)
#check_column_count(source, target)
#check_duplicates(target_duplicate_df, 'customer_id')
#check_null(target_duplicate_df, 'customer_id')
#data_compare(source, target) #used same source file as target file, for exact comaprision
#data_compare_sql(source, target) # using SQLdf
check_out_of_range(target_range, 'age', 21, 59)
# source_count = len(source)
# print(source_count)
