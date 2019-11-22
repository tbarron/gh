from gh import __main__ as ghm
from gh import version
import glob
import os
import pytest
import re
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
def test_task_separation(tasks):
    """
    Given some tasks, report them and verify that they have whitespace between
    them
    """
    pytest.dbgfunc()
    tmpdir = tasks['tmpdir']
    kw = {'PROJECT': None, 'count': False, 'd': False, 's': None,
          'projects': False, 'tasks': True, 'version': False}
    with tbx.envset(GH_ROOT=tmpdir.strpath):
        result = ghm.gh_tasks_t(**kw)
        assert "\n\n - " in result


# -----------------------------------------------------------------------------
def test_task_count(tasks):
    """
    Given some tasks, report them and verify that they have whitespace between
    them
    """
    pytest.dbgfunc()
    tmpdir = tasks['tmpdir']
    kw = {'PROJECT': 'myproj', 'count': True, 'd': False, 's': None,
          'projects': False, 'tasks': True, 'version': False}
    with tbx.envset(GH_ROOT=tmpdir.strpath):
        result = ghm.gh_tasks_t(**kw)
        rgx = r"\s+{}\s+4\n".format(tasks['prj'])
        assert re.search(rgx, result)
        assert re.search(r"\s+Total\s+4\n", result)


# -----------------------------------------------------------------------------
def test_task_proj(tasks):
    """
    Given some tasks, report them and verify that they have whitespace between
    them
    """
    pytest.dbgfunc()
    tmpdir = tasks['tmpdir']
    kw = {'PROJECT': 'myproj', 'count': False, 'd': False, 's': None,
          'projects': False, 'tasks': True, 'version': False}
    with tbx.envset(GH_ROOT=tmpdir.strpath):
        result = ghm.gh_tasks_t(**kw)
        assert "\n\n - " in result

    kw = {'PROJECT': 'nosuch', 'count': False, 'd': False, 's': None,
          'projects': False, 'tasks': True, 'version': False}
    with tbx.envset(GH_ROOT=tmpdir.strpath):
        result = ghm.gh_tasks_t(**kw)
        assert result == ""


# -----------------------------------------------------------------------------
def test_task_markers(tasks, capsys):
    """
    Use all potential task markers to identify tasks
    """
    pytest.dbgfunc()
    path = tasks['prj'].strpath
    task_l = ghm.get_tasks(path)
    assert len(task_l) == 4


# -----------------------------------------------------------------------------
def test_get_tasks_empty(tasks_empty):
    """
    Make get_tasks() return an empty list because no tasks are present
    """
    pytest.dbgfunc()
    path = tasks_empty['prj'].strpath
    task_l = ghm.get_tasks(path)
    assert task_l == []


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
def test_projects_t(prjdirs):
    """
    Test for ghm.gh_projects_t(), verifying that projects with no dodo file are
    identified
    """
    pytest.dbgfunc()
    tmpdir = prjdirs['root']
    kw = {'PROJECT': None, 'count': False, 'd': False, 's': None,
          'projects': True, 'tasks': False, 'version': False}
    with tbx.envset(GH_ROOT=tmpdir.strpath):
        result = ghm.gh_projects_t(**kw)
        assert "nododo (no DODO)" in result
        assert "tbx" in result
        assert "tbx (no DODO)" not in result


# -----------------------------------------------------------------------------
def test_projects_count(prjdirs):
    """
    Test for ghm.gh_projects_t(), verifying that projects with no dodo file are
    identified
    """
    pytest.dbgfunc()
    tmpdir = prjdirs['root']
    kw = {'PROJECT': None, 'count': True, 'd': False, 's': None,
          'projects': True, 'tasks': False, 'version': False}
    with tbx.envset(GH_ROOT=tmpdir.strpath):
        result = ghm.gh_projects_t(**kw)
        exp = "{} projects found\n".format(len(prjdirs['input']))
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
@pytest.mark.parametrize("stype, sname", [
    pytest.param('alpha', 'asort'),
    pytest.param('new', 'nsort'),
    pytest.param('old', 'osort'),
])
def test_projects_sorts(prjdirs, stype, sname):
    """
    Test an alpha sort through ghm.projects()
    """
    pytest.dbgfunc()
    result = ghm.projects(prjdirs['root'], sort=stype)                # payload
    for path in prjdirs[sname]:
        dirstat = '(no DODO)' if 'nododo' in path.strpath else ''
        try:
            exp.append((path, dirstat))
        except NameError:
            exp = [(path, dirstat)]
    assert result == exp


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("func, sname", [
    pytest.param(ghm.alpha_sort, 'asort', id='alpha'),
    pytest.param(ghm.new_sort, 'nsort', id='new'),
    pytest.param(ghm.old_sort, 'osort', id='old'),
])
def test_sorts(prjdirs, func, sname):
    """
    Test the sort routines
    """
    pytest.dbgfunc()
    result = func(prjdirs['input'])                                   # payload
    assert result == prjdirs[sname]


# -----------------------------------------------------------------------------
def test_no_sort(prjdirs):
    """
    What we get if we don't sort a list of projects
    """
    pytest.dbgfunc()
    tup_l = ghm.projects(prjdirs['root'].strpath, False)              # payload
    result = [_[0] for _ in tup_l]
    assert set(result) == set([_.strpath for _ in prjdirs['input']])


# -----------------------------------------------------------------------------
def test_version():
    """
    Test for 'gh version'
    """
    result = ghm.gh_version_t()
    assert result == "gh {}".format(version._v)


# -----------------------------------------------------------------------------
def test_deploy():
    """
    Check that 1) no untracked files are hanging out, 2) no staged but
    uncommitted updates are outstanding, 3) no unstaged, uncommitted changes
    are outstanding, 4) the most recent git tag matches HEAD, and 5) the most
    recent git tag matches the current version.
    """
    pytest.dbgfunc()
    staged, changed, untracked = tbx.git_status()
    assert untracked == [], "You have untracked files"
    assert changed == [], "You have unstaged updates"
    assert staged == [], "You have updates staged but not committed"

    if tbx.git_current_branch() != 'master':
        return True

    last_tag = tbx.git_last_tag()
    msg = "Version ({}) does not match tag ({})".format(version._v,
                                                        last_tag)
    assert version._v == last_tag, msg
    assert tbx.git_hash() == tbx.git_hash(last_tag), "Tag != HEAD"


# -----------------------------------------------------------------------------
@pytest.fixture
def tasks(tmpdir):
    """
    Set up a project with some tasks that we can test displaying
    """
    task_l = [
        "",
        " ^ this is the first task (released)",
        "   and it has a second line",
        " > this is the second task (committed)",
        " . this is the third task (changed, not yet committed)",
        " - this is the fourth task (not yet made)",
        "   and this one has a second line also",
        " + fifth task -- completed",
        " < sixth task -- moved elsewhere",
        " x seventh task -- abandoned",
        "",
    ]
    # project dir
    prjdir = tmpdir.join("myproj")

    # .project file
    prjdir.join(".project").ensure()

    # DODO file with content
    dodo = prjdir.join("DODO")
    dodo.write("\n".join(task_l) + "\n")

    data = {
        'tmpdir': tmpdir,
        'prj': prjdir,
        'dodo': dodo,
    }
    return data


# -----------------------------------------------------------------------------
@pytest.fixture
def tasks_empty(tmpdir):
    """
    Set up a project with some tasks that we can test displaying
    """
    # project dir
    prjdir = tmpdir.join("myproj")

    # .project file
    prjdir.join(".project").ensure()

    # this project doesn't have a DODO file
    data = {
        'tmpdir': tmpdir,
        'prj': prjdir,
        'dodo': None,
    }
    return data


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
