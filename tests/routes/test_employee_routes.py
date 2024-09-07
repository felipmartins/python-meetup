import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.app import app
from src.models.employee import Employee

client = TestClient(app)

mock_data = {
    "businesses": [
        {
            "id": 1,
            "name": "Tech Store",
            "address": "123 Tech Street",
            "employees": [
                {"id": 1, "name": "John Doe", "role": "Manager"},
                {"id": 2, "name": "Jane Doe", "role": "Developer"},
            ],
            "products": [],
        },
        {
            "id": 2,
            "name": "Bookstore",
            "address": "456 Library Lane",
            "employees": [],
            "products": [],
        },
    ]
}


@patch("src.routes.employee.read_data", return_value=mock_data)
def test_list_employees(mock_read_data):
    response = client.get("/businesses/1/employees")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "John Doe"


@patch("src.routes.employee.read_data", return_value=mock_data)
@patch("src.routes.employee.write_data")
def test_add_employee(mock_write_data, mock_read_data):
    new_employee = {"id": 3, "name": "Sarah Connor", "role": "Support"}

    response = client.post("/businesses/1/employees", json=new_employee)
    assert response.status_code == 200
    assert response.json()["name"] == "Sarah Connor"

    mock_write_data.assert_called_once()
    updated_data = mock_read_data.return_value
    updated_data["businesses"][0]["employees"].append(new_employee)
    mock_write_data.assert_called_with(updated_data)


@patch("src.routes.employee.read_data", return_value=mock_data)
@patch("src.routes.employee.write_data")
def test_update_employee(mock_write_data, mock_read_data):
    updated_employee = {"id": 1, "name": "John Doe Updated", "role": "Senior Manager"}

    response = client.put("/businesses/1/employees/1", json=updated_employee)
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe Updated"

    mock_write_data.assert_called_once()
    updated_data = mock_read_data.return_value
    updated_data["businesses"][0]["employees"][0].update(updated_employee)
    mock_write_data.assert_called_with(updated_data)


@patch("src.routes.employee.read_data", return_value=mock_data)
@patch("src.routes.employee.write_data")
def test_delete_employee(mock_write_data, mock_read_data):
    response = client.delete("/businesses/1/employees/1")
    assert response.status_code == 200
    assert response.json() == {"msg": "Employee deleted"}

    mock_write_data.assert_called_once()
    updated_data = mock_read_data.return_value
    updated_data["businesses"][0]["employees"] = [
        e for e in updated_data["businesses"][0]["employees"] if e["id"] != 1
    ]
    mock_write_data.assert_called_with(updated_data)


@patch("src.routes.employee.read_data", return_value=mock_data)
def test_list_employees_for_non_existent_business(mock_read_data):
    response = client.get("/businesses/999/employees")
    assert response.status_code == 404
    assert response.json() == {"detail": "Business not found"}


@patch("src.routes.employee.read_data", return_value=mock_data)
def test_delete_non_existent_employee(mock_read_data):
    response = client.delete("/businesses/1/employees/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}
