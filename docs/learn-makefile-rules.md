# Learn `Makefile` rules

This project leverages [GNU Make](https://www.gnu.org/software/make/manual/make.html) to simplify the major project lifecycle tasks (e.g. build, unit testing, deploy, etc). The project's `Makefile` has the following important rules:

| Command            | Description                                                   |
| ------------------ | ------------------------------------------------------------- |
| `make [default]`   | Run the `lint`, `unittest`, and `dist` rules                  |
| `make init`        | Initializes the Python virtual env                            |
| `make deplock`     | Lock dependencies with `poetry.lock` file                     |
| `make lint`        | Run linting tasks (e.g. pylint, flake8, etc.)                 |
| `make unittest`    | Run the project unit tests                                    |
| `make dist`        | Create the project distribution & binaries                    |
| `make inttest`     | Run tests that invoke the app locally                         |
| `make deploy`      | Deploy the application to AWS                                 |
| `make e2etest`     | Run tests that invoke the app on AWS                          |
| `make mostlyclean` | Removes generated project files (except virtual env)          |
| `make clean`       | Removes all generated files                                   |
| `make destroy`     | Deletes CloudFormation Stack for the application              |
| `make .gitignore`  | Make the `.gitignore` file using gitignore.io file generation |
