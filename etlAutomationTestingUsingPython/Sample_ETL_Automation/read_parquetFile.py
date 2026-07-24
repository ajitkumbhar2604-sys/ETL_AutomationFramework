from Sample_ETL_Automation.etl_validation import*
from Sample_ETL_Automation.etl_validation import read_file as old_read_file
import os

def read_file(file_path):

    print(os.path.splitext(file_path)[1])
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".csv":
        file_type = "csv"

    elif extension in [".xlsx", ".xls"]:
        file_type = "excel"

    elif extension == ".parquet":
        file_type = "parquet"

    else:
        raise ValueError(f"Unsupported file extension: {extension}")

    return old_read_file(file_path, file_type)


source = read_file(r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\customers_records_S.parquet")
target = read_file(r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\customers_records_T.csv")
check_count(source,target)
check_column_count(source, target)