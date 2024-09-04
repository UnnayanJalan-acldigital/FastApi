from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import users, employees, departments, auth
from app.database import engine, Base

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(employees.router)
app.include_router(departments.router)
