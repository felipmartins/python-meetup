from fastapi import APIRouter, HTTPException
from src.models.business import Business
from typing import List
from src.utils import read_data, write_data

router = APIRouter(prefix="/businesses")


@router.get("/", response_model=List[Business])
def list_businesses():
    data = read_data()
    return data["businesses"]


@router.post("/", response_model=Business)
def create_business(business: Business):
    data = read_data()
    data["businesses"].append(business.model_dump())
    write_data(data)
    return business


@router.get("/{id}", response_model=Business)
def get_business(id: int):
    data = read_data()
    for business in data["businesses"]:
        if business["id"] == id:
            return business
    raise HTTPException(status_code=404, detail="Business not found")


@router.put("/{id}", response_model=Business)
def update_business(id: int, updated_business: Business):
    data = read_data()
    for business in data["businesses"]:
        if business["id"] == id:
            business.update(updated_business.model_dump())
            write_data(data)
            return business
    raise HTTPException(status_code=404, detail="Business not found")


@router.delete("/{id}")
def delete_business(id: int):
    data = read_data()
    businesses = data["businesses"]
    for business in businesses:
        if business["id"] == id:
            businesses.remove(business)
            write_data(data)
            return {"msg": "Business deleted"}
    raise HTTPException(status_code=404, detail="Business not found")
