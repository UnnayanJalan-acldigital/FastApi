from fastapi import FastAPI, HTTPException

app = FastAPI()


employees = [
    {"id": 1, "name": "Unnayan", "position": "Intern"},
    {"id": 2, "name": "Pankaj", "position": "Project Manager"},
]

def find_employee(employee_id: int):
    return next((emp for emp in employees if emp["id"] == employee_id), None)

@app.get("/employees")
def get_employees():
    return {"employees": employees}

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    employee=find_employee(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee Not Found")
    return employee

@app.post("/employees")
def create_employee(employee: dict):
    new_id = max(emp["id"] for emp in employees) +1 if employees else 1
    employee["id"] = new_id
    employees.append(employee)
    return employee

@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, update_id:dict):
    employee=find_employee(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee Not Found")
    employee.update(update_id)
    employee["id"]=employee_id
    return employee

