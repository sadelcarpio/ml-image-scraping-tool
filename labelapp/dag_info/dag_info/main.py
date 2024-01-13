import fastapi
from sqlmodel import Session, select

from dag_info.db import engine
from dag_info.models import ProjectModel, UserModel
from dag_info.schemas import DagInfo

app = fastapi.FastAPI()


@app.get("/", status_code=200)
def get_dag_info() -> list[DagInfo]:
    with Session(engine) as session:
        projects = list(session.exec(select(ProjectModel)))
        user_emails = [session.exec(select(UserModel.email).where(UserModel.id == project.owner_id)).first()
                       for project in projects]
        return [DagInfo(project=project.name,
                        keywords=project.keywords,
                        notify=user_email) for project, user_email in zip(projects, user_emails)]
