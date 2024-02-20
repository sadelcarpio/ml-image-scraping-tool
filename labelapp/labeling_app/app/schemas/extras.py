from enum import Enum

from sqlmodel import SQLModel


class LabelRead(SQLModel):
    name: str


class TaskType(str, Enum):
    multilabel = "multilabel_classification"
    sparse = "sparse_classification"
    regression = "regression"
    detection = "detection"
