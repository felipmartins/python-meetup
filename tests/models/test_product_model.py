import pytest
from pydantic import ValidationError
from src.models.product import Product


def test_create_product_with_valid_data():
    product = Product(id=1, name="Laptop", price=999.99, is_available=True)
    assert product.id == 1
    assert product.name == "Laptop"
    assert product.price == 999.99


def test_create_product_with_invalid_id():
    with pytest.raises(ValidationError):
        Product(id="abc", name="Laptop", price=999.99, is_available=True)


def test_create_product_with_missing_name():
    with pytest.raises(ValidationError):
        Product(id=1, price=999.99)


def test_create_product_with_missing_price():
    with pytest.raises(ValidationError):
        Product(id=1, name="Laptop")


def test_create_product_with_invalid_price():
    with pytest.raises(ValidationError):
        Product(id=1, name="Laptop", price="expensive")


def test_create_product_with_zero_price():
    product = Product(id=2, 
                      name="Free Item", 
                      price=0.0, 
                      is_available=True)
    assert product.id == 2
    assert product.name == "Free Item"
    assert product.price == 0.0


def test_create_product_with_negative_price():
    with pytest.raises(ValidationError):
        Product(id=3, 
                name="Negative Price Item", 
                price=-100.0, 
                is_available=True)
