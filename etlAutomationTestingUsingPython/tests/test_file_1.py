import pytest


def test_case_first():
    assert 1==1

def test_case_second():
    assert 1==1

@pytest.mark.skip(reason="skip")
def test_case_third():
    assert 1==1

target = 9
@pytest.mark.skipif(target==9, reason="Target matched..")
def test_case_third():
    assert target==8

@pytest.mark.parametrize("source_table, target_table", [(1,11),(2,22),(3,35),(4,44),(5,55)])
def test_case_multiple(source_table, target_table):
    assert source_table*11 == target_table

