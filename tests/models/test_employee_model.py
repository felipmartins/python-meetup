import pytest
from pydantic import ValidationError
from src.models.employee import Employee


def test_create_employee_with_valid_data():
    employee = Employee(id=1, name="John Doe", role="Manager")
    assert employee.id == 1
    assert employee.name == "John Doe"
    assert employee.role == "Manager"


def test_create_employee_with_invalid_id():
    with pytest.raises(ValidationError):
        Employee(id="abc", name="John Doe", role="Manager")


def test_create_employee_with_missing_name():
    with pytest.raises(ValidationError):
        Employee(id=1, role="Manager")


def test_create_employee_with_missing_role():
    with pytest.raises(ValidationError):
        Employee(id=1, name="John Doe")


def test_create_employee_with_invalid_role_type():
    with pytest.raises(ValidationError):
        Employee(id=1, name="John Doe", role=123)


def test_create_employee_with_all_fields():
    employee = Employee(id=1, name="Jane Doe", role="Developer")
    assert employee.id == 1
    assert employee.name == "Jane Doe"
    assert employee.role == "Developer"
