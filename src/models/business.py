from pydantic import BaseModel
from typing import List
from src.models.employee import Employee
from src.models.product import Product


class Business(BaseModel):
    """Represents a business"""

    id: int
    name: str
    address: str
    employees: List[Employee] = []
    products: List[Product] = []

    def getAddress(self):
        return self.address == None

    def isNameValid(self):
        return type(self.name) == str
