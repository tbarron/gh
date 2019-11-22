## 1.0.1 ... 2019-11-22 14:49:28

 * When displaying tasks, separate them with a blank line
 * Match and display all four active task markers (-, ., >, ^)
 * Add project marker for those with no DODO file
 * Add test for deployability
 * Complete test coverage

## 1.0.0 ... 2019-11-22 09:41:50

 * Project inception
 * Start working toward 100% test coverage of payload code
 * Facilitate testing by separating user control aspects from easily
   testable aspects
 * Add ability to count projects and tasks
 * Add ability to sort projects in various ways
 * Add test for code quality
 * Add tests: code quality (flake8), gh_tasks, gh_projects, show_tasks,
   is_throw_away, projects (alpha sort), omit_list, dodo_filename (dodo
   file exists and doesn't), alpha sort, new sort, old sort, no sort,
   version.
 * Created git controlled files: .gitignore, CHANGELOG.md, README.md,
   requirements.txt, setup.py, gh/{__main__,version}.py, tests
 * Create non-git controlled files: DODO, pytest.ini, venv.3.8

