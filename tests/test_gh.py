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
def test_projects_alpha(tmpdir):
    """
    Test for ghm.projects()
    """
    pytest.dbgfunc()
    plist = ['one', 'two', 'three', 'four']
    for prj in plist:
        pdir = tmpdir.join(prj)
        pdir.ensure(dir=True)
        pdir.join('.project').ensure()
    exp = ["{}/{}".format(tmpdir.strpath, _) for _ in sorted(plist)]
    result = ghm.projects(tmpdir.strpath, False, sort='alpha')        # payload
    assert result == exp


# -----------------------------------------------------------------------------
def test_omit_list():
    """
    Check that ghm.omit_list() returns a set of strings
    """
    result = ghm.omit_list()                                          # payload
    for item in result:
        assert type(item) == str


# -----------------------------------------------------------------------------
@pytest.fixture
def dodo_existing(tmpdir):
    """
    Set up a project with a DODO file
    """
    prjdir = tmpdir.join('projdir')
    prjdir.ensure(dir=True)
    prjdir.join('.project').ensure()
    dofile = prjdir.join('DODO')
    dofile.write("\n - this is a task\n")
    return (prjdir, dofile)


# -----------------------------------------------------------------------------
@pytest.fixture
def dodo_nosuch(tmpdir):
    """
    Set up a project without a DODO file
    """
    prjdir = tmpdir.join('projdir')
    prjdir.ensure(dir=True)
    prjdir.join('.project').ensure()
    dofile = prjdir.join('DODO')
    return (prjdir, dofile)
