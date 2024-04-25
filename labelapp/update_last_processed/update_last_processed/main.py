from datetime import datetime

import fastapi
from fastapi import Depends
from pydantic import BaseModel
from sqlmodel import Session, SQLModel, Field, select

from update_last_processed.db import get_session

app = fastapi.FastAPI()


class DateString(BaseModel):
    date_str: str


class ProjectModel(SQLModel, table=True):
    __tablename__ = "projects"
    id: int | None = Field(default=None, primary_key=True, index=True)
    name: str
    last_processed: datetime = Field(default_factory=lambda: datetime.utcfromtimestamp(0))


@app.patch("/{project_name}", status_code=204)
def update_project_last_processed(project_name: str, timestamp: DateString, session: Session = Depends(get_session)):
    project = session.exec(select(ProjectModel).where(ProjectModel.name == project_name)).one()
    project.last_processed = datetime.strptime(timestamp.date_str, "%Y-%m-%dT%H:%M:%S.%f")
    session.add(project)
    session.commit()
