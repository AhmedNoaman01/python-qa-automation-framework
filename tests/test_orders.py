def test_create_order_returns_total_and_reduces_stock(api_client, make_product):
    product = make_product(price=7.5, stock=5)
    response = api_client.post("/api/orders", json={"product_id": product["id"], "quantity": 2})
    assert response.status_code == 201
    body = response.json()
    assert body["product_id"] == product["id"]
    assert body["quantity"] == 2
    assert body["unit_price"] == 7.5
    assert body["total"] == 15.0
    updated_product = api_client.get(f"/api/products/{product['id']}").json()
    assert updated_product["stock"] == 3


def test_create_order_rejects_unknown_product(api_client):
    response = api_client.post("/api/orders", json={"product_id": "missing-product", "quantity": 1})
    assert response.status_code == 404


def test_create_order_rejects_zero_quantity(api_client, make_product):
    product = make_product()
    response = api_client.post("/api/orders", json={"product_id": product["id"], "quantity": 0})
    assert response.status_code == 422


def test_create_order_rejects_negative_quantity(api_client, make_product):
    product = make_product()
    response = api_client.post("/api/orders", json={"product_id": product["id"], "quantity": -1})
    assert response.status_code == 422


def test_create_order_rejects_insufficient_stock(api_client, make_product):
    product = make_product(stock=1)
    response = api_client.post("/api/orders", json={"product_id": product["id"], "quantity": 2})
    assert response.status_code == 409
    assert response.json()["detail"] == "Insufficient stock"


def test_create_order_rejects_missing_product_id(api_client):
    response = api_client.post("/api/orders", json={"quantity": 1})
    assert response.status_code == 422
