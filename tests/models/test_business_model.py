import pytest
from pydantic import ValidationError
from src.models.business import Business
from src.models.employee import Employee
from src.models.product import Product


def test_create_business_with_valid_data():
    employee = Employee(id=1, name="John Doe", role="Manager")
    product = Product(id=101, name="Laptop", price=999.99)

    business = Business(
        id=1,
        name="Tech Store",
        address="123 Tech Street",
        employees=[employee],
        products=[product],
    )

    assert business.id == 1
    assert business.name == "Tech Store"
    assert business.address == "123 Tech Street"
    assert len(business.employees) == 1
    assert business.employees[0].name == "John Doe"
    assert len(business.products) == 1
    assert business.products[0].name == "Laptop"


def test_create_business_with_invalid_id():
    employee = Employee(id=1, name="John Doe", role="Manager")
    product = Product(id=101, name="Laptop", price=999.99)

    with pytest.raises(ValidationError):
        Business(
            id="abc",
            name="Tech Store",
            address="123 Tech Street",
            employees=[employee],
            products=[product],
        )


def test_create_business_with_missing_name():
    employee = Employee(id=1, name="John Doe", role="Manager")
    product = Product(id=101, name="Laptop", price=999.99)

    with pytest.raises(ValidationError):
        Business(
            id=1,
            address="123 Tech Street",
            employees=[employee],
            products=[product],
        )


def test_create_business_with_missing_address():
    employee = Employee(id=1, name="John Doe", role="Manager")
    product = Product(id=101, name="Laptop", price=999.99)

    with pytest.raises(ValidationError):
        Business(
            id=1,
            name="Tech Store",
            employees=[employee],
            products=[product],
        )


def test_create_business_with_empty_employees_and_products():
    business = Business(
        id=2,
        name="Bookstore",
        address="456 Library Lane",
        employees=[],
        products=[],
    )

    assert business.id == 2
    assert business.name == "Bookstore"
    assert business.address == "456 Library Lane"
    assert business.employees == []
    assert business.products == []


def test_create_business_with_missing_fields():
    with pytest.raises(ValidationError):
        Business(
            id=3,
            address="789 Fashion Ave",
            employees=[],
            products=[],
        )


def test_create_business_with_multiple_employees_and_products():
    employee1 = Employee(id=1, name="John Doe", role="Manager")
    employee2 = Employee(id=2, name="Jane Smith", role="Developer")
    product1 = Product(id=101, name="Laptop", price=999.99)
    product2 = Product(id=102, name="Smartphone", price=499.99)

    business = Business(
        id=1,
        name="Tech Store",
        address="123 Tech Street",
        employees=[employee1, employee2],
        products=[product1, product2],
    )

    assert len(business.employees) == 2
    assert business.employees[0].name == "John Doe"
    assert business.employees[1].name == "Jane Smith"
    assert len(business.products) == 2
    assert business.products[0].name == "Laptop"
    assert business.products[1].name == "Smartphone"
