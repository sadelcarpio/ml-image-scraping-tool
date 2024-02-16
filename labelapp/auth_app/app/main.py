from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import OAuth2PasswordRequestForm

from app.db import SessionDep
from app.deps import CurrentUser, get_current_user
from app.init_db import init_db
from app.models import UserModel
from app.schemas import Token, UserRead
from app.security import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token

app = FastAPI()
init_db()


@app.post("/token")
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
        data={"sub": user.username, "scopes": form_data.scopes}, expires_delta=access_token_expires  # TODO: change scopes for the actual scopes of the user
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=UserRead)
async def read_users_me(current_user: CurrentUser):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
        current_user: Annotated[UserModel, Security(get_current_user, scopes=["items"])]
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/status/")
async def read_system_status(current_user: CurrentUser):
    return {"status": "ok"}
