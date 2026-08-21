from pandasql import sqldf
import pandas as pd
import pytest


#Add fixture for read
# @pytest.fixture
# def read_data():
#     source_data = pd.read_csv(
#         r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\source_file_fixture.csv")
#     target_data = pd.read_csv(
#         r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\target_file_fixture.csv")
#     return source_data, target_data


def test_count_check(read_data):
    source_data, target_data = read_data
    assert len(source_data) == len(target_data), f"Source and Target data are not equal"


def test_duplicat_check(read_data):
    sourcedata,target_data = read_data
    #target_data = pd.read_csv(r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\target_file_fixture.csv")
    # #duplicate_df = target_data.groupBy("customer_id").count().filter(col("count") > 1)
    # duplicate_df = target_data[
    #     target_data.duplicated(
    #         subset=["customer_id"],
    #         keep=False)]

    duplicate_df = sqldf("""
        SELECT *
        FROM target_data
        WHERE customer_id IN (
            SELECT customer_id
            FROM target_data
            GROUP BY customer_id
            HAVING COUNT(*) > 1)
    """)

    print("Duplicate data at Target",duplicate_df)
    #duplicate_count= duplicate_df.count()
    duplicate_count = len(duplicate_df)
    print("Duplicate count at Target",duplicate_count)
    assert duplicate_count == 0, \
        f"Duplicate records found: {duplicate_count}"


def test_null_check(read_data):
    target_data = read_data[1]
    #target_data = pd.read_csv(
    #    r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\target_file_fixture.csv")
    query = """
        SELECT *
        FROM target_data
        WHERE customer_id IS NULL
    """
    null_df = sqldf(query)
    null_count = null_df.shape[0]
    assert null_count == 0, \
        f"NULL customer_id found: {null_count}"

def test_unique_check(read_data):
    target_data = read_data[1]
    # target_data = pd.read_csv(
    #     r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\target_file_fixture.csv")
    total_count = target_data["customer_id"].count()

    unique_count = target_data["customer_id"].nunique()

    assert total_count == unique_count, \
        f"customer_id is not unique. Total={total_count}, Unique={unique_count}"

    print("PASS: Column is unique")

def test_data_compare(read_data):
    source_data, target_data = read_data
    # source_data = pd.read_csv(
    #     r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\source_file_fixture.csv")
    # target_data = pd.read_csv(
    #     r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\target_file_fixture.csv")

    query = """
        SELECT * FROM source_data

        EXCEPT

        SELECT * FROM target_data
    """

    source_difference = sqldf(query)

    assert source_difference.empty, \
        f"Records present in Source but missing in Target:\n{source_difference}"