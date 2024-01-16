import fastapi
from fastapi import Depends
from sqlmodel import Session

from dag_info.actions import fetch_project_information
from dag_info.db import get_session
from dag_info.schemas import DagInfo

app = fastapi.FastAPI()


@app.get("/", status_code=200, response_model=list[DagInfo])
def get_dag_info(session: Session = Depends(get_session)):
    return fetch_project_information(session)
