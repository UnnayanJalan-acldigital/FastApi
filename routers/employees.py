from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import get_db
from app.models import Employee, Department, User
from app.auth import get_current_active_user

  
router = APIRouter()

# Templates directory
templates = Jinja2Templates(directory="app/templates")

@router.post("/employees")
def create_employee(employee: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    department = db.query(Department).filter(Department.id == employee["department_id"]).first()
    if department is None:
        raise HTTPException(status_code=404, detail="Department Not Found")
    
    new_employee = Employee(
        name=employee["name"],
        position=employee["position"],
        department_id=employee["department_id"]
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@router.get("/employees", response_class=HTMLResponse)
def get_employees(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    employees = db.query(Employee).all()
    return templates.TemplateResponse("index.html", {"request": request, "employees": employees})

@router.get("/employees/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee Not Found")
    return employee

@router.put("/employees/{employee_id}")
def update_employee(employee_id: int, update_data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee Not Found")
    for key, value in update_data.items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    return employee
@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee Not Found")
    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}


