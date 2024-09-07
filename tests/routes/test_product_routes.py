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
            "products": [
                {"id": 1, 
                 "name": "Laptop", 
                 "price": 999.99, 
                 "is_available": True},
                {"id": 2, 
                 "name": "Smartphone", 
                 "price": 499.99, 
                 "is_available": False},
            ],
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


@patch("src.routes.product.read_data", return_value=mock_data)
def test_list_products(mock_read_data):
    response = client.get("/businesses/1/products")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Laptop"


@patch("src.routes.product.read_data", return_value=mock_data)
@patch("src.routes.product.write_data")
def test_add_product(mock_write_data, mock_read_data):
    new_product = {"id": 3,
                   "name": "Tablet", 
                   "price": 299.99, 
                   "is_available": True}

    response = client.post("/businesses/1/products", json=new_product)
    assert response.status_code == 200
    assert response.json()["name"] == "Tablet"

    mock_write_data.assert_called_once()
    updated_data = mock_read_data.return_value
    updated_data["businesses"][0]["products"].append(new_product)
    mock_write_data.assert_called_with(updated_data)


@patch("src.routes.product.read_data", return_value=mock_data)
@patch("src.routes.product.write_data")
def test_update_product(mock_write_data, mock_read_data):
    updated_product = {"id": 1, 
                       "name": "Updated Laptop", 
                       "price": 1099.99, 
                       "is_available": True,
                       }

    response = client.put("/businesses/1/products/1", json=updated_product)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Laptop"

    mock_write_data.assert_called_once()
    updated_data = mock_read_data.return_value
    updated_data["businesses"][0]["products"][0].update(updated_product)
    mock_write_data.assert_called_with(updated_data)


@patch("src.routes.product.read_data", return_value=mock_data)
@patch("src.routes.product.write_data")
def test_delete_product(mock_write_data, mock_read_data):
    response = client.delete("/businesses/1/products/1")
    assert response.status_code == 200
    assert response.json() == {"msg": "Product deleted"}

    mock_write_data.assert_called_once()
    updated_data = mock_read_data.return_value
    updated_data["businesses"][0]["products"] = [
        p for p in updated_data["businesses"][0]["products"] if p["id"] != 1
    ]
    mock_write_data.assert_called_with(updated_data)


@patch("src.routes.product.read_data", return_value=mock_data)
def test_list_products_for_non_existent_business(mock_read_data):
    response = client.get("/businesses/999/products")
    assert response.status_code == 404
    assert response.json() == {"detail": "Business not found"}


@patch("src.routes.product.read_data", return_value=mock_data)
def test_delete_non_existent_product(mock_read_data):
    response = client.delete("/businesses/1/products/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}
