from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, Security
from fastapi.security import SecurityScopes, OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from starlette import status

from app.crud.crud_user import CRUDUserDep
from app.models.users import UserModel
from app.schemas.token import TokenData
from app.security.passwords import verify_password

SECRET_KEY = "546fc0304773380edc8f1171636ceaf47f9660ad54f26d7a3c935daf645ee5a3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def authenticate_user(users_crud: CRUDUserDep, username: str, password: str):
    user = users_crud.get_by_username(username)
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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token",
                                     scopes={"admin": "Admin functionalities"})
TokenDep = Annotated[TokenData, Depends(oauth2_scheme)]


async def get_current_user(security_scopes: SecurityScopes, token: TokenDep, users_crud: CRUDUserDep):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = users_crud.get_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


CurrentUser = Annotated[UserModel, Depends(get_current_user)]
CurrentAdminUser = Annotated[UserModel, Security(get_current_user, scopes=["admin"])]
