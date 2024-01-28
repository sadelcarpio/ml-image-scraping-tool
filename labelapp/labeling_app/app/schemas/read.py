import uuid

from app.models import LabelModel
from app.schemas.projects import ProjectBase


class ProjectRead(ProjectBase):
    owner_id: uuid.UUID
    labels: list[LabelModel] = []
