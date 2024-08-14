from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/employee_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    position = Column(String(50))


Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/employees")
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return {"employees": employees}

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee Not Found")
    return employee

@app.post("/employees")
def create_employee(employee: dict, db: Session = Depends(get_db)):
    new_employee = Employee(name=employee["name"], position=employee["position"])
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, update_data: dict, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee Not Found")
    for key, value in update_data.items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    return employee

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee Not Found")
    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}
