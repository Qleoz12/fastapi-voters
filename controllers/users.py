import logging
from fastapi import HTTPException  # Correct import
from sqlite3 import IntegrityError
from typing import List

from fastapi import APIRouter
from fastapi import FastAPI, Depends, Body

from auth.authentications import get_current_user, get_password_hash
from auth.authorizations import authorize
from models.db import get_db
from models.models import User, UserRole
from models.shcemas import UserSchema, UserSchemaStandart
from sqlalchemy.orm import Session

usersApp = APIRouter(prefix="/users",
                   tags=["users"])

logger = logging.getLogger(__name__)

@usersApp.post('/')
@authorize(role=[UserRole.ADMIN,UserRole.LEAD])
def add(user: UserSchema, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    if existing_user:
       return {"message": "already created", "user": existing_user}
    try:
        UsrORM=User(**user.dict())
        UsrORM.password=get_password_hash(user.password)
        db.add(UsrORM)
        db.commit()
        db.refresh(UsrORM)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error occurred while adding the voter")

    UsrORM.password=""
    return {"message": "added successfully", "user": UsrORM}


@usersApp.get('/', response_model=List[UserSchemaStandart])
@authorize(role=[UserRole.ADMIN])
def get(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        users = db.query(User).all()
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching states.")
    
    return users