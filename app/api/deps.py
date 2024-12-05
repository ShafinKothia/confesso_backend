import uuid
from websockets import Data
from app.core.config import Settings
from datetime import datetime, timedelta
from typing import Union, Generator
from app.schemas import UserMe
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.core import security
from app.db.session import SessionLocal
from app.crud.rep_user import rep_user
from sqlalchemy.orm import Session
from app import crud, models, schemas



reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/users/token"
)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()



async def get_current_user(db: Session = Depends(get_db) , token: str = Depends(reusable_oauth2)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},

    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        person_id = payload.get("sub")
        username = rep_user.get_user_by_id(db=db,id=person_id).username
        if username is None:
            raise credentials_exception
        print(username)
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Session Expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = crud.rep_user.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserMe = Depends(get_current_user)):
    return current_user



