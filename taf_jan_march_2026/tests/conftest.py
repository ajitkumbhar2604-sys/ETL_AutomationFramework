import pytest

@pytest.fixture(scope='module')
def read_data(spark_session, read_config):
    pass

@pytest.fixture(scope='module')
def read_config():
    pass

# #@pytest.fixture(scope='module') -> required only when source/target is Database
# def read_sql():
#     pass
#
# #@pytest.fixture(scope='module') -> required only when source/target is File
# def read_schema():
#     pass
#Move above to helpers.py under Utility

@pytest.fixture(scope='session')
def spark_session():
    pass
