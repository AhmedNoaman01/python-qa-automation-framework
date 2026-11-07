# Python REST API Test Automation Framework

A learning portfolio project demonstrating a small, reusable API test automation setup using Python, pytest, Requests, FastAPI, Git, and Ubuntu/Linux. The included Products & Orders API is a local demo system under test; it is not a Siemens product and does not represent Calibre, EDA, or semiconductor manufacturing experience.

## What is included

- Local demo REST API for products and orders (`src/demo_api`).
- Reusable Requests-based API client (`clients/api_client.py`).
- pytest fixtures that start and stop the demo API (`tests/conftest.py`).
- Positive, negative, and boundary API tests.
- JUnit XML output and a small Python summary report.
- Bash runner and GitHub Actions workflow.
- Test plan and test-case inventory in `docs/`.

## Requirements

- Python 3.10+
- Git
- Ubuntu/Linux, macOS, or Windows with a Bash-compatible shell (Ubuntu is recommended for this learning track).

## Setup on Ubuntu

```bash
git clone <your-repository-url>
cd python-qa-automation
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the test suite

```bash
chmod +x run_tests.sh
./run_tests.sh
```

The runner starts the local API for the test session, executes pytest, writes `reports/junit.xml`, and creates `reports/summary.md` and `reports/summary.json`. The API process is stopped when pytest finishes.

You can also run pytest directly:

```bash
PYTHONPATH=src python -m pytest -v --junitxml=reports/junit.xml
python reporting/summarize_junit.py reports/junit.xml
```

## Project structure

```text
python-qa-automation/
  src/demo_api/       # FastAPI demo application
  clients/            # reusable Requests API client
  tests/              # pytest suites and fixtures
  reporting/          # JUnit XML summary utility
  docs/               # test plan and test cases
  reports/            # generated reports
  .github/workflows/  # GitHub Actions CI workflow
  requirements.txt
  pytest.ini
  run_tests.sh
```

## Learning tasks for the owner

1. Run the tests and explain the purpose of each test.
2. Add a test for a product name longer than the allowed maximum.
3. Add a test for updating a product with a blank name.
4. Improve one assertion or error message.
5. Commit your changes with clear Git messages and push them to your repository.
6. Review the JUnit XML and summary report; verify the counts match the pytest output.

## Limitations

- The demo API uses in-memory storage and resets when the process restarts.
- This is a compact learning project, not a production framework.
- Tests cover the included demo API contract only.
- No AI agent, Jira integration, browser automation, Calibre, EDA, or actual semiconductor process testing is implemented.

## CV wording (only after you run, understand, and modify the project)

> Built a Python/pytest API automation framework covering [actual test count] scenarios across positive, negative, and boundary conditions; used reusable Requests helpers and pytest fixtures, and generated JUnit XML test reports.

Replace the bracketed count with the actual number reported by your test run.
