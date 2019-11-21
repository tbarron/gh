from gh import __main__ as ghm
import pytest


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("inp, exp", [
    pytest.param("----------", True, id="throw away hyphen lines"),
    pytest.param("", True, id="throw away empty lines"),
    pytest.param("# this is a comment", True, id="throw away comment lines"),
    pytest.param("-- DONE -----", True, id="-- DONE -----"),
    pytest.param("- == DONE -----", True, id="- == DONE -----"),
    pytest.param("=== DONE -----", True, id="=== DONE -----"),
    pytest.param("everything else okay", False, id="everything else"),
])
def test_is_throw_away(inp, exp):
    """
    Test function ghm.is_throw_away()
    """
    pytest.dbgfunc()
    assert ghm.is_throw_away(inp) == exp


# -----------------------------------------------------------------------------
def test_fails():
    """
    Verifying that pytest works
    """
    pytest.fail('construction')
