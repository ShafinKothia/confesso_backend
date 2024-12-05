from datetime import datetime, timedelta
import random
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm.session import Session
from passlib.context import CryptContext
from pydantic import BaseModel
from email_validator import validate_email, EmailNotValidError, EmailSyntaxError, EmailUndeliverableError
from .auth import AuthHandler
from app.schemas.sch_user import UserCreate, UserMe
from app.schemas.token import TokenData, Token
from app.api import deps
from app.core import security
from app.crud import rep_user
from fastapi.responses import HTMLResponse
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig, MessageType
import json
from app.core.config import settings



router = APIRouter()

auth_handler = AuthHandler()

# to get a string like this run:
# openssl rand -hex 32



@router.post("/token", response_model=Token)
async def login_for_access_token(db_conn: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_handler.authenticate_user(db_conn, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
  
    access_token_expires = timedelta(minutes=auth_handler.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_handler.create_access_token(
        data={"sub": user.id, }, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post('/register')
async def register(  auth_details: UserCreate, db_conn: Session = Depends(deps.get_db)):
    users = rep_user.get_users(db=db_conn)
    errors = {}

    for x in users:
        if x.username == auth_details.username:
            errors["username"] = {"status": False, "error_input": "username", "message": f"Username already registered"}


    for key in auth_details.__dict__.keys():
        print(key)

        # print(getattr(auth_details, key))
        if not getattr(auth_details, key):
            errors[key] = {"status": False, "error_input": key, "message": f"Please enter your {str(key)}"}

    if auth_details.password != auth_details.confirm_password:
        errors["confirm_password"] =  {"status": False, "error_input": "confirm_password", "message": "The password and the re-entered password do not match"}
    
    if errors != {}:
        return {"status": False,"error": "Field Error", "component_errors" : errors}
    else:
        hashed_password = auth_handler.get_password_hash(auth_details.password)

        response_data = rep_user.create_user(db=db_conn, create_data=auth_details, hashed_password=hashed_password)
        new_user = rep_user.get_user_by_id(db=db_conn, id=response_data.id)

        return {"status": True,"error": None, "user": new_user}
    

@router.get("/users/me/", response_model=UserMe)
async def read_users_me(current_user: UserMe = Depends(deps.get_current_active_user)):
    return current_user
