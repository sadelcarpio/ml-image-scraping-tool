from typing import Annotated

from fastapi import HTTPException, Depends
from fastapi.security import SecurityScopes
from jose import jwt, JWTError
from pydantic import ValidationError
from starlette import status

from app.db import SessionDep
from app.models import UserModel
from app.schemas import TokenData
from app.security import TokenDep, SECRET_KEY, ALGORITHM, get_user


async def get_current_user(security_scopes: SecurityScopes, token: TokenDep, session: SessionDep):
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
    user = get_user(session, token_data.username)
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
