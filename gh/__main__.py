"""
Usage:
    gh projects [-d] [-v] [-s SORT]
    gh tasks [-d] [PROJECT]

Options:
    -s SORT       determine project order ('alpha', 'old', or 'new')

gh tasks
    Show tasks for projects located in $GH_ROOT

gh projects [-d] [-v] [-s SORT]
    Produce a list of projects in $GH_ROOT. SORT can be 'alpha' to sort
    projects alphabetically, 'old' to sort from oldest to newest, or 'new' to
    sort from oldest to newest. The project 'age' is based on the mod time of
    the project's DODO file (or 0 if the project has no DODO file). Thus, the
    'old' sort will put projects with no DODO file at the top of the list.
"""
from docopt_dispatch import dispatch
import glob
import os
import os.path as osp
import pdb
import re


# -----------------------------------------------------------------------------
@dispatch.on('projects')
def gh_projects(**kw):
    """
    List projects in $GH_ROOT
    """
    if kw['d']:
        pdb.set_trace()
    files = projects(os.getenv("GH_ROOT"), kw['v'], kw['s'])
    for item in files:
        print("    {}".format(item))


# -----------------------------------------------------------------------------
@dispatch.on('tasks')
def gh_tasks(**kw):
    """
    Show tasks for projects located in $GH_ROOT
    """
    if kw['d']:
        pdb.set_trace()
    files = projects(os.getenv("GH_ROOT"), False)
    if kw['PROJECT']:
        for path in [_ for _ in files if kw['PROJECT'] in _]:
            show_tasks(path)
    else:
        for path in files:
            show_tasks(path)


# -----------------------------------------------------------------------------
def show_tasks(path):
    """
    Show the tasks in dodo file *path*
    """
    task = ""
    task_l = []
    throw_away = True
    dofile = dodo_filename(path)
    if dofile is None:
        return
    with open(dofile) as rbl:
        for line in rbl:
            if line.startswith(" + "):
                throw_away = True
            elif line.startswith(" - "):
                task_l.append(task)
                throw_away = False
                task = line
            elif not is_throw_away(line) and not throw_away:
                task += line
        task_l.append(task)

    task_l = [_ for _ in task_l if _]
    if task_l:
        print("----------- {} ------------\n".format(path))
        for task in task_l:
            print(task)
        

# -----------------------------------------------------------------------------
def dodo_filename(path):
    """
    Find a 'DODO*' file in *path* and return its full pathname
    """
    globble = glob.glob("{}/DODO*".format(path))
    if globble:
        return globble[0]
    else:
        return None

    
# -----------------------------------------------------------------------------
def is_throw_away(line):
    """
    Return True if the line is a throw_away, otherwise False
    """
    rval = any([line.startswith("------------"),
                line.strip() == "",
                line.startswith("#"),
                re.search("^ *-+\s+DONE", line),
                re.search("^-\s+=+\s+DONE", line),
                re.search("^=+\s+DONE", line),
                ])
    return rval


# -----------------------------------------------------------------------------
def show_one(task):
    """
    Display the task
    """
    if task:
        print(task)


# -----------------------------------------------------------------------------
def omit_list():
    """
    Return a list of projects to omit from the lists
    """
    rval = ["tbarron.github.io", "_site", "evernote_helpers"]
    return rval


# -----------------------------------------------------------------------------
def projects(root, verbose, sort=None):
    """
    Return a list of project directories. To represent a project, the directory
    must contain a marker file named '.project'.

    walking everything: 6.468
    """
    rval = []
    omits = ['venv',
             '__pycache__',
             'test',
             'attic',
             'egg-info',
             '.git',
             '.cache',
             ]
    for (path, dirs, files) in os.walk(root):
        rmables = [d for d in dirs if any(o in d for o in omits)]
        [dirs.remove(item) for item in rmables]
        if '.project' in files:
            rval.append(path)
    if sort == 'alpha':
        rval = sorted(rval)
    elif sort == 'old':
        rval = old_sort(rval)
    elif sort == 'new':
        rval = new_sort(rval)
    return rval


# -----------------------------------------------------------------------------
def old_sort(projs):
    """
    Sort projects from oldest to newest by mtime of DODO file. Projects with no
    DODO file are considered oldest.
    """
    pdict = {}
    for prj in projs:
        dofile = dodo_filename(prj)
        if dofile:
            pdict[prj] = os.path.getmtime(dofile)
        else:
            pdict[prj] = 0
    rval = [_[0] for _ in sorted(pdict.items(), key=lambda k: k[1])]
    return rval


# -----------------------------------------------------------------------------
def new_sort(projs):
    """
    Sort projects from most to least recently updated by mtime of DODO file.
    Projects with no DODO file are considered oldest.
    """
    rval = old_sort(projs)
    return list(reversed(rval))


# -----------------------------------------------------------------------------
def dodo_files(root):
    """
    Get a list of DODO files from *root*
    """
    rval = []
    omits = omit_list()
    for (path, dirs, files) in os.walk(root):
        if any([_ in path for _ in omits]):
            continue
        dodo_files = [_ for _ in files
                      if _.startswith('DODO') and '~' not in _]
        for item in dodo_files:
            rval.append("{}/{}".format(path, item))
    return rval


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    dispatch(__doc__)
