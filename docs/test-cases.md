# Test Case Inventory

| ID | Scenario | Expected result | Type |
|---|---|---|---|
| API-HEALTH-001 | Check health endpoint | 200 and service status is ok | Positive |
| API-PROD-001 | Create product with valid fields | 201 and generated product ID | Positive |
| API-PROD-002 | Create product with surrounding spaces in name | 201 and name is trimmed | Positive |
| API-PROD-003 | Create product without name | 422 validation response | Negative |
| API-PROD-004 | Create product with empty or whitespace name | 422 validation response | Negative |
| API-PROD-005 | Create product with zero or negative price | 422 validation response | Boundary |
| API-PROD-006 | Create product with negative stock | 422 validation response | Boundary |
| API-PROD-007 | Retrieve existing product | 200 and matching ID | Positive |
| API-PROD-008 | Retrieve unknown product | 404 not found | Negative |
| API-PROD-009 | Update product fields | 200 and requested fields changed | Positive |
| API-PROD-010 | Update product with invalid price | 422 validation response | Negative |
| API-PROD-011 | Delete existing product | 204 then subsequent GET returns 404 | Positive |
| API-PROD-012 | Delete unknown product | 404 not found | Negative |
| API-ORDER-001 | Create order within available stock | 201, correct total, stock decreases | Positive |
| API-ORDER-002 | Create order for unknown product | 404 not found | Negative |
| API-ORDER-003 | Create order with zero quantity | 422 validation response | Boundary |
| API-ORDER-004 | Create order with negative quantity | 422 validation response | Boundary |
| API-ORDER-005 | Create order above available stock | 409 conflict | Negative |
| API-ORDER-006 | Create order without product ID | 422 validation response | Negative |

The executed pytest count may include parameterized cases as separate test instances. Use the generated report for the actual count.
