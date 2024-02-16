from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlmodel import select

from app.db import SessionDep
from app.models import UserModel
from app.schemas import TokenData

SECRET_KEY = "546fc0304773380edc8f1171636ceaf47f9660ad54f26d7a3c935daf645ee5a3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token",
                                     scopes={"me": "Read information about the current user.", "items": "Read items."})


def verify_password(plain_password, hashed_password):
    # return pwd_context.verify(plain_password, hashed_password)
    return plain_password == hashed_password  # For fast testing


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(session: SessionDep, username: str):
    user = session.exec(select(UserModel).where(UserModel.username == username)).first()
    return user


def authenticate_user(session: SessionDep, username: str, password: str):
    user = get_user(session, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


TokenDep = Annotated[TokenData, Depends(oauth2_scheme)]
