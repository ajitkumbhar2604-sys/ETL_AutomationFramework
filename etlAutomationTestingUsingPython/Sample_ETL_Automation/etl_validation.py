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


#Call the fucntions from here
source = read_file(r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\customers_records_S.csv", "csv")
target = read_file(r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\customers_records_T.csv", file_type="csv")

check_count(source,target)
check_column_count(source, target)