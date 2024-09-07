from fastapi.testclient import TestClient
from unittest.mock import patch
from src.app import app

client = TestClient(app)

mock_data = {
    "businesses": [
        {
            "id": 1,
            "name": "Tech Store",
            "address": "123 Tech Street",
            "employees": [],
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


@patch("src.routes.business.read_data", return_value=mock_data)
def test_list_businesses(mock_read_data):
    response = client.get("/businesses/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Tech Store"


@patch("src.routes.business.read_data", return_value=mock_data)
@patch("src.routes.business.write_data")
def test_create_business(mock_write_data, mock_read_data):
    new_business = {
        "id": 3,
        "name": "Coffee Shop",
        "address": "789 Coffee Ave",
        "employees": [],
        "products": [],
    }

    response = client.post("/businesses/", json=new_business)
    assert response.status_code == 200
    assert response.json()["name"] == "Coffee Shop"

    mock_write_data.assert_called_once()
    updated_data = mock_read_data.return_value
    updated_data["businesses"].append(new_business)
    mock_write_data.assert_called_with(updated_data)


@patch("src.routes.business.read_data", return_value=mock_data)
def test_get_business(mock_read_data):
    response = client.get("/businesses/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Tech Store"


@patch("src.routes.business.read_data", return_value=mock_data)
def test_get_non_existent_business(mock_read_data):
    response = client.get("/businesses/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Business not found"}


@patch("src.routes.business.read_data", return_value=mock_data)
@patch("src.routes.business.write_data")
def test_update_business(mock_write_data, mock_read_data):
    updated_business = {
        "id": 1,
        "name": "Updated Tech Store",
        "address": "123 Updated Tech Street",
        "employees": [],
        "products": [],
    }

    response = client.put("/businesses/1", json=updated_business)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Tech Store"

    mock_write_data.assert_called_once()
    updated_data = mock_read_data.return_value
    updated_data["businesses"][0].update(updated_business)
    mock_write_data.assert_called_with(updated_data)


@patch("src.routes.business.read_data", return_value=mock_data)
@patch("src.routes.business.write_data")
def test_delete_business(mock_write_data, mock_read_data):
    response = client.delete("/businesses/1")
    assert response.status_code == 200
    assert response.json() == {"msg": "Business deleted"}

    mock_write_data.assert_called_once()
    updated_data = mock_read_data.return_value
    updated_data["businesses"] = [b for b in updated_data["businesses"] if b["id"] != 1]
    mock_write_data.assert_called_with(updated_data)


@patch("src.routes.business.read_data", return_value=mock_data)
def test_delete_non_existent_business(mock_read_data):
    response = client.delete("/businesses/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Business not found"}
