import pytest


# -----------------------------------------------------------------------------
def test_passes():
    """
    Verifying that pytest works
    """
    assert 5 == 5


# -----------------------------------------------------------------------------
def test_fails():
    """
    Verifying that pytest works
    """
    pytest.fail('construction')
