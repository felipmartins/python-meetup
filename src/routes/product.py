from fastapi import APIRouter, HTTPException
from src.models.product import Product
from typing import List
from src.utils import read_data, write_data

router = APIRouter(prefix="/businesses")


@router.get("/{id}/products", response_model=List[Product])
def list_products(id: int):
    data = read_data()
    for business in data["businesses"]:
        if business["id"] == id:
            return business["products"]
    raise HTTPException(status_code=404, detail="Business not found")


@router.post("/{id}/products", response_model=Product)
def add_product(id: int, product: Product):
    data = read_data()
    for business in data["businesses"]:
        if business["id"] == id:
            business["products"].append(product.model_dump())
            write_data(data)
            return product
    raise HTTPException(status_code=404, detail="Business not found")


@router.put("/{id}/products/{product_id}", response_model=Product)
def update_product(id: int, product_id: int, updated_product: Product):
    data = read_data()
    for business in data["businesses"]:
        if business["id"] == id:
            for product in business["products"]:
                if product["id"] == product_id:
                    product.update(updated_product.model_dump())
                    write_data(data)
                    return product
    raise HTTPException(status_code=404, detail="Product not found")


@router.delete("/{id}/products/{product_id}")
def delete_product(id: int, product_id: int):
    data = read_data()
    for business in data["businesses"]:
        if business["id"] == id:
            products = business["products"]
            for product in products:
                if product["id"] == product_id:
                    products.remove(product)
                    write_data(data)
                    return {"msg": "Product deleted"}
    raise HTTPException(status_code=404, detail="Product not found")
