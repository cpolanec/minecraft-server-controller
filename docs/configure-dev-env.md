# Configure development environment

## Prerequisites

The following environment configurations are expected to build, deploy and run this application locally:

| Resource                     | Supported | Expected (but not validated) |
| ---------------------------- | --------- | ---------------------------- |
| Operating System             | macOS     | Windows                      |
| Python                       | 3.8       | n/a                          |
| Python Dependency Management | Poetry    | n/a                          |
| IDE                          | VS Code   | PyCharm                      |

## Other resources

Poetry will take care of the remaining technology dependencies including:

- AWS SAM
- Pylint, pytest
- Other Python dependencies

This project contains the Python [`diagram`](https://diagrams.mingrammer.com) library which creates diagram images from Python code. This module is only required to create new images for the project documentation and is NOT required to run/deploy the application. Please review the [`diagram` installation guide](https://diagrams.mingrammer.com/docs/getting-started/installation) if you want to modify these diagrams.
