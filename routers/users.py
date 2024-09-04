from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_password_hash
from app.models import User

router = APIRouter()

@router.post("/users/", response_model=dict)
def create_user(username: str, password: str, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(password)
    new_user = User(username=username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"username": new_user.username, "id": new_user.id}
