#!/usr/bin/env bash
set -u
mkdir -p reports
python -m pytest -v --junitxml=reports/junit.xml
pytest_status=$?
python reporting/summarize_junit.py reports/junit.xml
summary_status=$?
if [ "$pytest_status" -ne 0 ]; then
  exit "$pytest_status"
fi
exit "$summary_status"
