# Test Plan — Demo Products & Orders API

## Objective
Verify the core behavior, input validation, and error handling of the local Products & Orders REST API using repeatable automated tests. The goal is to demonstrate practical test design and Python automation techniques.

## Scope
- Health endpoint.
- Product creation, retrieval, update, and deletion.
- Order creation and stock validation.
- Required-field, invalid-value, not-found, and insufficient-stock behavior.
- Response status codes and selected response-body fields.

## Out of scope
- Performance/load, security penetration, database persistence, UI/browser testing, payment processing, and integrations with external services.
- Calibre, semiconductor manufacturing, EDA, and IC layout verification.

## Test approach
- Positive testing: valid product and order flows.
- Negative testing: missing/blank fields, invalid values, unknown IDs.
- Boundary testing: zero/negative price, stock, and quantity; maximum name length can be added as an owner exercise.
- State verification: confirm that creating an order reduces product stock by the requested quantity.
- Reproducibility: create test data through API fixtures and run the demo API in a fresh process for each test session.

## Environment
Python 3.10+, FastAPI, Uvicorn, pytest, Requests, local loopback HTTP, Git, and Ubuntu/Linux recommended.

## Entry criteria
Dependencies installed, virtual environment active, and repository available locally.

## Exit criteria
All tests execute; actual pass/fail/error/skip counts are captured in JUnit XML and the Markdown/JSON summaries. Investigate and document any failures; do not hide failures to achieve a green report.
