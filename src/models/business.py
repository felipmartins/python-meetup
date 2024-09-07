from pydantic import BaseModel
from typing import List
from src.models.employee import Employee
from src.models.product import Product


class Business(BaseModel):
    id: int
    name: str
    address: str
    employees: List[Employee] = []
    products: List[Product] = []
