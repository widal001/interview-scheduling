# Interview Scheduling Script

An algorithm for assigning and scheduling interviews based on mutual interest and availability

## Table of Contents

- [About this Project](#overview)
  - [Workflow](#workflow)
  - [Reference Documents](#reference-documents)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## About this Project

The goal of this project is to simplify the following steps of a placement process in which a fixed pool of candidates are applying for a fixed pool of roles:

1. Matching candidates and hiring managers for initial interviews based on mutual interest
1. Scheduling the assigned interviews based on mutual availability
1. Finalizing matches between candidates and roles based on an updated set of preferences submitted after the interviews

The resulting tools and scripts work best for placement processes in which candidates possess a similar set of skills and interests, and the roles comprise a similar set of functions and responsibilities, for example fellowship or internship programs.

### Made With

- [pandas](https://pandas.pydata.org/docs/user_guide/index.html)
- [networkx](https://networkx.org/)

### Reference Documents

## Getting Started

### Prerequisites

- Python version 3.6 to 3.8

In order to check which version of python you have installed, run the following command in your command line (for Mac/Linux)

> **NOTE:** in all of the code blocks below, lines preceded with `$` indicate commands you should enter in your command line (excluding the `$` itself), while lines preceded with `>` indicate the expected output from the previous command.

```
$ python --version
> Python 3.7.7
```

If you don't have Python version 3.6 or later installed on your computer, consider using [pyenv](https://github.com/pyenv/pyenv) to install and manage multiple versions of Python concurrently.

### Installation

1. Fork the repo -- for more information about forking, reference [this guide](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/working-with-forks)
1. Clone your forked repo on your local machine`git clone https://github.com/YOUR_USERNAME/interview-scheduling.git`
1. Create a new virtual environment in your project directory `python -m venv env`
1. Activate your virtual environment `source env/bin/activate`
1. Install necessary python packages`pip install -r requirements.txt`
1. Install pre-commit to enable pre-commit hooks (This step ensures that your code is formatted according the Black standard and is compliant with PEP8.)
   ```
   $ pre-commit install
   > pre-commit installed at .git/hooks/pre-commit
   ```
1. Run the tests and make sure everything passes
   ```
   $ pytest
   > =============== XX passed in XXs ===============
   ```

## Usage

Additional details on usage are in progress.

## Contributing

Additional details on contributing are in progress
