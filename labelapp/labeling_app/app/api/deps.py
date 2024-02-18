from typing import Generator, Annotated

from fastapi import Depends, Body, HTTPException
from sqlmodel import Session, select

from app.db.engine import EngineDep
from app.models.extras import LabelModel
from app.models.projects import ProjectModel
from app.schemas.extras import TaskType


def get_db(engine: EngineDep) -> Generator:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


def validate_labels(project_id: int, session: SessionDep, labels: dict = Body(...)):
    task_type = session.exec(select(ProjectModel.task_type).where(ProjectModel.id == project_id)).first()
    allowed_labels = session.exec(select(LabelModel.name).where(LabelModel.project_id == project_id)).all()
    data_type = {TaskType.sparse: int, TaskType.regression: float | int, TaskType.multilabel: int}.get(task_type)
    if not all(isinstance(value, data_type) for value in labels.values()):
        raise HTTPException(status_code=400, detail="Invalid data types for labels.")
    if set(allowed_labels) != set(labels.keys()):
        raise HTTPException(status_code=400, detail=f"Labels not allowed. Valid labels are {allowed_labels}")
