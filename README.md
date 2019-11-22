# gh - project management for my github repositories

  * This repo contains code that helps me manage my github repos.

  * I don't plan to put this on travis since I don't expect anyone else would
    be interested in it.

  * Functions available:

      * gh projects [-d] [-s SORT] [--count]

         * List or count projects in $GH_ROOT. SORT can be 'alpha', 'new',
           or 'old'. If -s is not present, the list of projects is not
           sorted. If -d is present, we fire up the debugger.

      * gh tasks [-d] [-s SORT] [--count] [PROJECT]

         * List or count tasks. If PROJECT is present, only tasks for that
           project are counted/listed. SORT is the same as for the projects
           function. What gets sorted is the projects, not tasks within a
           project. If -d is present, we fire up the debugger.

      * gh version [-d]

         * Report the current version of gh.
