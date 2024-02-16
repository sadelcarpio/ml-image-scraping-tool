from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm

from app.db import SessionDep
from app.deps import CurrentUser, get_current_user
from app.models import UserModel
from app.schemas import Token, UserRead, UserCreate
from app.security import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, pwd_context

app = FastAPI()


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
        data={"sub": user.username, "scopes": ["admin"] if user.is_admin else []}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me", status_code=status.HTTP_200_OK, response_model=UserRead)
async def read_users_me(current_user: CurrentUser):
    return current_user


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserRead)
def create_user(user: UserCreate, session: SessionDep):
    user_dict = {key: value for key, value in user if key != "password"}
    hashed_password = pwd_context.hash(user.password)
    db_user = UserModel(**user_dict, hashed_password=hashed_password)
    session.add(db_user)
    session.commit()
    return db_user


@app.get("/users/admin", status_code=status.HTTP_200_OK, response_model=UserRead)
async def get_admin_info(current_user: Annotated[UserModel, Security(get_current_user, scopes=["admin"])]):
    return current_user
