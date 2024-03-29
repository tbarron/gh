"""
Usage:
    gh projects [-d] [-s SORT] [--count]
    gh tasks [-d] [-s SORT] [--count] [PROJECT]
    gh version [-d]

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

This is free and unencumbered software released into the public domain.
For more details, please visit <http://unlicense.org/>.
"""
from docopt_dispatch import dispatch
from gh import version
import glob
import os
import os.path as osp
import pdb
import re


# -----------------------------------------------------------------------------
def main():
    """
    Main entry point
    """
    dispatch(__doc__)


# -----------------------------------------------------------------------------
@dispatch.on('projects')
def gh_projects_d(**kw):                                     # pragma: no cover
    """
    List projects in $GH_ROOT
    """
    if kw['d']:
        pdb.set_trace()
    print(gh_projects_t(**kw))


# -----------------------------------------------------------------------------
def gh_projects_t(**kw):
    """
    Heavy lifting
    """
    rval = ""
    files = projects(os.getenv("GH_ROOT"), kw['s'])
    if kw['count']:
        rval += "{} projects found\n".format(len(files))
    else:
        for path, do_stat in files:
            rval += "    {} {}\n".format(path, do_stat)
    return rval


# -----------------------------------------------------------------------------
@dispatch.on('tasks')
def gh_tasks_d(**kw):                                        # pragma: no cover
    """
    Show tasks for projects located in $GH_ROOT
    """
    if kw['d']:
        pdb.set_trace()
    print(gh_tasks_t(**kw))


# -----------------------------------------------------------------------------
def gh_tasks_t(**kw):
    """
    """
    rval = ""
    sort = kw['s']
    files = projects(os.getenv("GH_ROOT"), sort=sort)
    if kw['PROJECT']:
        files = [_[0] for _ in files if kw['PROJECT'] in _[0]]
    else:
        files = [_[0] for _ in files]

    total = 0
    if kw['count']:
        for path in files:
            tl = get_tasks(path)
            rval += "   {:45s}   {:>5d}\n".format(path, len(tl))
            total += len(tl)
        rval += "   {:45s}   {:>5d}\n".format("Total", total)
    else:
        for path in files:
            rval += show_tasks(path)
    return rval


# -----------------------------------------------------------------------------
@dispatch.on('version')
def gh_version_d(**kw):                                      # pragma: no cover
    """
    Report the current version
    """
    if kw['d']:
        pdb.set_trace()
    print(gh_version_t())


# -----------------------------------------------------------------------------
def gh_version_t():
    """
    Retrieve and return the string for gh version
    """
    return "gh {}".format(version._v)


# -----------------------------------------------------------------------------
def get_tasks(path):
    """
    Get a list of the tasks in dodo file *path*
    """
    task = ""
    task_l = []
    throw_away = True
    dofile = dodo_filename(path)
    if dofile is None:
        return []
    with open(dofile) as rbl:
        for line in rbl:
            pfl = []
            if research(r"^\s[-.>^+<x]\s", line, pfl):
                pfx = pfl[0]
                if pfx in [" - ", " . ", " > ", " ^ "]:
                    task_l.append(task)
                    throw_away = False
                    task = line
                elif pfx in [" + ", " < ", " x "]:
                    throw_away = True
            elif not is_throw_away(line) and not throw_away:
                task += line
        task_l.append(task)

    task_l = [_ for _ in task_l if _]
    return task_l


# -----------------------------------------------------------------------------
def research(needle, haystack, result):
    """
    Look for rgx *needle* in str *haystack*. Put any match in result. If a
    match was found, return True, else return False. Note that result must be a
    list.
    """
    found = re.findall(needle, haystack)
    if found:
        result.append(found[0])
        return True
    else:
        result.clear()
        return False


# -----------------------------------------------------------------------------
def show_tasks(path):
    """
    Show the tasks in dodo file *path*
    """
    rval = ""
    task_l = get_tasks(path)
    if task_l:
        rval += "----------- {} ------------\n".format(path)
        for task in task_l:
            rval += task + "\n"
    return rval


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
    rval = any([line.startswith("--------"),
                line.strip() == "",
                line.startswith("#"),
                re.search(r"^ *-+\s+DONE", line),
                re.search(r"^-\s+=+\s+DONE", line),
                re.search(r"^=+\s+DONE", line),
                ])
    return rval


# -----------------------------------------------------------------------------
def omit_list():
    """
    Return a list of projects to omit from the lists
    """
    rval = ["tbarron.github.io", "_site", "evernote_helpers"]
    return rval


# -----------------------------------------------------------------------------
def projects(root, sort=None):
    """
    Return a list of tuples representing project directories. The first element
    of each tuple is the path of the directory. The second element is a string
    that is either empty (if a DODO file exists) or '(no DODO)' (if no DODO
    file is present).

    To represent a project, the directory must contain a marker file named
    '.project'.
    """
    plist = []
    dolist = []
    omits = ['venv',
             '__pycache__',
             'test',
             'attic',
             'egg-info',
             '.git',
             '.cache',
             ]
    for (path, dirs, files) in os.walk(root, followlinks=True):
        rmables = [d for d in dirs if any(o in d for o in omits)]
        [dirs.remove(item) for item in rmables]
        if '.project' in files:
            plist.append(path)
            if any('DODO' in _ for _ in files):
                dolist.append(path)

    if sort == 'alpha':
        plist = alpha_sort(plist)
    elif sort == 'old':
        plist = old_sort(plist)
    elif sort == 'new':
        plist = new_sort(plist)
    else:
        plist = plist

    rval = []
    for path in plist:
        if path in dolist:
            rval.append((path, ''))
        else:
            rval.append((path, '(no DODO)'))

    return rval


# -----------------------------------------------------------------------------
def alpha_sort(projs):
    """
    Sort project paths alphabetically
    """
    return sorted(projs)


# -----------------------------------------------------------------------------
def old_sort(projs):
    """
    Sort project paths from oldest to newest by mtime of DODO file. Projects
    with no DODO file are considered oldest.
    """
    pdict = {}
    for prj in projs:
        dofile = dodo_filename(prj)
        if dofile:
            pdict[prj] = osp.getmtime(dofile)
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
if __name__ == "__main__":
    dispatch(__doc__)                                        # pragma: no cover
