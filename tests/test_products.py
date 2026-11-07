import pytest


def test_create_product_returns_created_resource(api_client):
    response = api_client.post("/api/products", json={"name": "Keyboard", "price": 25.5, "stock": 8})
    assert response.status_code == 201
    body = response.json()
    assert body["id"]
    assert body["name"] == "Keyboard"
    assert body["price"] == 25.5
    assert body["stock"] == 8


def test_create_product_trims_surrounding_spaces(api_client):
    response = api_client.post("/api/products", json={"name": "  Mouse  ", "price": 10, "stock": 4})
    assert response.status_code == 201
    assert response.json()["name"] == "Mouse"


@pytest.mark.parametrize("payload", [
    {"price": 10, "stock": 3},
    {"name": "", "price": 10, "stock": 3},
    {"name": "   ", "price": 10, "stock": 3},
])
def test_create_product_rejects_missing_or_blank_name(api_client, payload):
    response = api_client.post("/api/products", json=payload)
    assert response.status_code == 422


@pytest.mark.parametrize("price", [0, -1])
def test_create_product_rejects_non_positive_price(api_client, price):
    response = api_client.post("/api/products", json={"name": "Invalid Price", "price": price, "stock": 2})
    assert response.status_code == 422


def test_create_product_rejects_negative_stock(api_client):
    response = api_client.post("/api/products", json={"name": "Invalid Stock", "price": 5, "stock": -1})
    assert response.status_code == 422


def test_get_product_returns_existing_product(api_client, make_product):
    created = make_product(name="Fetchable Product")
    response = api_client.get(f"/api/products/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_product_returns_404_for_unknown_id(api_client):
    response = api_client.get("/api/products/does-not-exist")
    assert response.status_code == 404


def test_update_product_changes_requested_fields(api_client, make_product):
    created = make_product(name="Before Update", price=20, stock=5)
    response = api_client.put(f"/api/products/{created['id']}", json={"name": "After Update", "price": 22})
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "After Update"
    assert body["price"] == 22
    assert body["stock"] == 5


def test_update_product_rejects_invalid_price(api_client, make_product):
    created = make_product()
    response = api_client.put(f"/api/products/{created['id']}", json={"price": 0})
    assert response.status_code == 422


def test_delete_product_removes_resource(api_client, make_product):
    created = make_product()
    delete_response = api_client.delete(f"/api/products/{created['id']}")
    get_response = api_client.get(f"/api/products/{created['id']}")
    assert delete_response.status_code == 204
    assert get_response.status_code == 404


def test_delete_unknown_product_returns_404(api_client):
    response = api_client.delete("/api/products/unknown-delete-id")
    assert response.status_code == 404
