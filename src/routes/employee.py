from fastapi import APIRouter, HTTPException
from src.models.employee import Employee
from typing import List
from src.utils import read_data, write_data


router = APIRouter(prefix="/businesses")


@router.get("/{id}/employees", response_model=List[Employee])
def list_employees(id: int):
    """List employees for a specific business"""
    data = read_data()
    for business in data["businesses"]:
        if business["id"] == id:
            return business["employees"]
    raise HTTPException(status_code=404, detail="Business not found")


@router.post("/{id}/employees", response_model=Employee)
def add_employee(id: int, employee: Employee):
    """Add a new employee to a business"""
    data = read_data()
    for business in data["businesses"]:
        if business["id"] == id:
            business["employees"].append(employee.model_dump())
            write_data(data)
            return employee
    raise HTTPException(status_code=404, detail="Business not found")


@router.put("/{id}/employees/{employee_id}", response_model=Employee)
def update_employee(id: int, employee_id: int, updated_employee: Employee):
    """Update an employee for a specific business"""
    data = read_data()
    for business in data["businesses"]:
        if business["id"] == id:
            for employee in business["employees"]:
                if employee["id"] == employee_id:
                    employee.update(updated_employee.model_dump())
                    write_data(data)
                    return employee
    raise HTTPException(status_code=404, detail="Employee not found")


@router.delete("/{id}/employees/{employee_id}")
def delete_employee(id: int, employee_id: int):
    """Delete an employee from a business"""
    data = read_data()
    for business in data["businesses"]:
        if business["id"] == id:
            employees = business["employees"]
            for employee in employees:
                if employee["id"] == employee_id:
                    employees.remove(employee)
                    write_data(data)
                    return {"msg": "Employee deleted"}
    raise HTTPException(status_code=404, detail="Employee not found")
