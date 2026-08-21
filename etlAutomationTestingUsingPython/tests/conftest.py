import pandas as pd
import pytest


@pytest.fixture
def read_data():
    source_data = pd.read_csv(
        r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\source_file_fixture.csv")
    target_data = pd.read_csv(
        r"C:\Users\Admin\PycharmProjects\etlAutomationTestingUsingPython\Input_Files\target_file_fixture.csv")
    return source_data, target_data