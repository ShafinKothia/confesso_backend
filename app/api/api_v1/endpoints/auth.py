from jose import JWTError, jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm.session import Session
from ....crud.rep_user import rep_user
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Any, Union
from ....schemas.token import TokenData
from app.core import security
from app.core.config import settings
import json



class AuthHandler():
    ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60 * 365
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def  create_access_token(self, data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta

        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        print(datetime.utcnow())
        print(expire)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=security.ALGORITHM)
        return encoded_jwt


    def authenticate_user(self, db : Session, username: str, password: str):
        user = rep_user.get_user_by_username(db=db, username=username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    

 

    

    