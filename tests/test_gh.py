from gh import __main__ as ghm
from gh import version
import glob
import os
import pytest
import tbx


# -----------------------------------------------------------------------------
def test_code_quality():
    """
    Run flake8 to assess the quality of the package per pep8
    """
    pytest.dbgfunc()
    globble = sorted(glob.glob("gh/*.py"))
    globble.extend(sorted(glob.glob("tests/*.py")))
    cmd = "flake8 --ignore \"$FLAKE_IGNORE\" {}".format(" ".join(globble))
    result = tbx.run(tbx.expand(cmd))
    assert result == ""


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("inp, exp", [
    pytest.param("----------", True, id="throw away: hyphen lines"),
    pytest.param("", True, id="throw away: empty lines"),
    pytest.param("# this is a comment", True, id="throw away: comment lines"),
    pytest.param("-- DONE -----", True, id="throw away: -- DONE -----"),
    pytest.param("- == DONE -----", True, id="throw away: - == DONE -----"),
    pytest.param("=== DONE -----", True, id="throw away: === DONE -----"),
    pytest.param("everything else okay", False, id="keep: everything else"),
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
    result = ghm.projects(tmpdir.strpath, sort='alpha')               # payload
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
def test_dodo_filename_x(dodo_existing):
    """
    Run dodo_filename for a file that exists
    """
    pytest.dbgfunc()
    (prjdir, dofile) = dodo_existing
    rval = ghm.dodo_filename(prjdir.strpath)                          # payload
    assert rval == dofile.strpath


# -----------------------------------------------------------------------------
def test_dodo_filename_n(dodo_nosuch):
    """
    Run dodo_filename for a file that does not exist
    """
    pytest.dbgfunc()
    (prjdir, dofile) = dodo_nosuch
    rval = ghm.dodo_filename(prjdir.strpath)                          # payload
    assert not dofile.exists()
    assert rval is None


# -----------------------------------------------------------------------------
def test_alpha_sort(prjdirs):
    """
    A set of projects sorted alphabetically
    """
    pytest.dbgfunc()
    result = ghm.alpha_sort(prjdirs['input'])                         # payload
    assert result == prjdirs['asort']


# -----------------------------------------------------------------------------
def test_new_sort(prjdirs):
    """
    A set of projects sorted new to old DODO file (no DODO file is oldest)
    """
    pytest.dbgfunc()
    result = ghm.new_sort(prjdirs['input'])                           # payload
    assert result == prjdirs['nsort']


# -----------------------------------------------------------------------------
def test_no_sort(prjdirs):
    """
    What we get if we don't sort a list of projects
    """
    pytest.dbgfunc()
    result = ghm.projects(prjdirs['root'].strpath, False)             # payload
    assert set(result) == set([_.strpath for _ in prjdirs['input']])


# -----------------------------------------------------------------------------
def test_old_sort(prjdirs):
    """
    A set of projects sorted old to new DODO file (no DODO file is oldest)
    """
    pytest.dbgfunc()
    result = ghm.old_sort(prjdirs['input'])                           # payload
    assert result == prjdirs['osort']


# -----------------------------------------------------------------------------
def test_version():
    """
    Test for 'gh version'
    """
    result = ghm.gh_version_t()
    assert result == "gh {}".format(version._v)


# -----------------------------------------------------------------------------
@pytest.fixture
def prjdirs(tmpdir):
    """
    Set up some project directories for testing
    """
    pdata = {
        'apple': {'dtime': 1500},
        'zagnut': {'dtime': 1400},
        'frump': {'dtime': 1300},
        'nododo': {'dtime': -1},
        'gh': {'dtime': 1200},
        'tbx': {'dtime': 1000},
    }
    for prj in pdata:
        pd = tmpdir.join(prj)
        pd.ensure(dir=True)
        dot = pd.join('.project')
        dot.ensure()
        if prj != 'nododo':
            dodo = pd.join('DODO')
            dodo.ensure()
            os.utime(dodo.strpath, (dodo.atime(),
                                    dodo.mtime() - pdata[prj]['dtime']))
        pdata[prj]['dir'] = pd
        pdata[prj]['dot'] = dot
        pdata[prj]['dodo'] = dodo

    pfruit = {}
    pfruit['raw'] = pdata
    pfruit['root'] = tmpdir
    pfruit['input'] = [pdata[_]['dir'] for _ in pdata]
    pfruit['asort'] = [pdata[_]['dir']
                       for _ in ['apple',
                                 'frump',
                                 'gh',
                                 'nododo',
                                 'tbx',
                                 'zagnut',
                                 ]]
    pfruit['nsort'] = [pdata[_]['dir']
                       for _ in ['tbx',
                                 'gh',
                                 'frump',
                                 'zagnut',
                                 'apple',
                                 'nododo',
                                 ]]
    pfruit['osort'] = [pdata[_]['dir']
                       for _ in ['nododo',
                                 'apple',
                                 'zagnut',
                                 'frump',
                                 'gh',
                                 'tbx',
                                 ]]
    return pfruit


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
