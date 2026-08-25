import pandas as pd
import pytest


@pytest.fixture(scope='session')
def read_data():
    source_data = pd.read_csv(
        r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\source_file_fixture.csv")
    target_data = pd.read_csv(
        r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\target_file_fixture.csv")
    print("This is the cleanup/TearDown method after the YIELD keyword")
    yield source_data, target_data
    print("This is the cleanup/TearDown method after YIELD keyword")