from pydantic import BaseModel


class Employee(BaseModel):
    """Class representing an employee"""

    id: int
    name: str
    role: str

    def isIdValid(self):
        return type(self.id) == int

    def isManager(self):
        return self.role == "Manager"
