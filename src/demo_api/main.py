"""Small local REST API used only as a predictable test target."""
from uuid import uuid4
from typing import Optional

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Demo Products and Orders API", version="1.0.0")
products = {}
orders = {}

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("name must not be blank")
        return value

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=80)
    price: Optional[float] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)

    @field_validator("name")
    @classmethod
    def clean_optional_name(cls, value):
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("name must not be blank")
        return value

class OrderCreate(BaseModel):
    product_id: str
    quantity: int = Field(gt=0)

@app.get("/health")
def health():
    return {"status": "ok", "service": "demo-products-orders-api"}

@app.post("/api/products", status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate):
    product_id = str(uuid4())
    record = {"id": product_id, **payload.model_dump()}
    products[product_id] = record
    return record

@app.get("/api/products")
def list_products():
    return {"items": list(products.values()), "count": len(products)}

@app.get("/api/products/{product_id}")
def get_product(product_id: str):
    product = products.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/api/products/{product_id}")
def update_product(product_id: str, payload: ProductUpdate):
    product = products.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="At least one field is required")
    product.update(changes)
    return product

@app.delete("/api/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    del products[product_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/api/orders", status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate):
    product = products.get(payload.product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if product["stock"] < payload.quantity:
        raise HTTPException(status_code=409, detail="Insufficient stock")
    order_id = str(uuid4())
    total = round(product["price"] * payload.quantity, 2)
    order = {
        "id": order_id,
        "product_id": product["id"],
        "quantity": payload.quantity,
        "unit_price": product["price"],
        "total": total,
    }
    product["stock"] -= payload.quantity
    orders[order_id] = order
    return order
