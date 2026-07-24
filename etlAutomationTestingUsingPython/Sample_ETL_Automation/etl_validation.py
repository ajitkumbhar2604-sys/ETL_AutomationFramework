#print("Sample ETL automation framework")
import pandas as pd
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

#Call the functions from here
source = read_file(r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\customers_records_S.csv", "csv")
#target = read_file(r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\customers_records_T.csv", file_type="csv")
target_duplicate_df = read_file(r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\customers_records_T_with_DuplicateRec.csv", file_type="csv")

#check_count(source,target)
#check_column_count(source, target)
check_duplicates(target_duplicate_df, 'customer_id')
# source_count = len(source)
# print(source_count)
