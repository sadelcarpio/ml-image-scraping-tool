from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import SessionDep
from app.schemas.token import Token
from app.security import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter(tags=["Authentication"])


@router.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: SessionDep) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": ["admin"] if user.is_admin else []}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
