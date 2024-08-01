from auth.authentications import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_user
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi import APIRouter
from sqlalchemy.orm import Session
from auth.authorizations import authorize
from models.db import get_db
from models.models import UserRole

securitysApp = APIRouter(prefix="/sec",
                   tags=["sec"])

# Define endpoints for token generation and authentication
@securitysApp.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.name}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@securitysApp.get("/check-all")
@authorize(role=[UserRole.ADMIN,UserRole.LEAD])
async def route1(current_user: dict = Depends(get_current_user)):
    return {"message": "This endpoint is accessible to admin and superadmin only"}


@securitysApp.get("/check-admin")
@authorize(role=[UserRole.ADMIN])
async def route2(current_user: dict = Depends(get_current_user)):
    return {"message": "This endpoint is accessible to admin only"}

@securitysApp.get("/check-leader")
@authorize(role=[UserRole.LEAD])
async def route2(current_user: dict = Depends(get_current_user)):
    return {"message": "This endpoint is accessible to leader only"}