from sqlmodel import Session, select

from dag_info.models import ProjectModel, UserModel


def fetch_project_information(session: Session):
    project_info = session.exec(select(ProjectModel.name, ProjectModel.keywords, UserModel.email).join(UserModel))
    return [{"project": project[0],
             "keywords": project[1],
             "notify": project[2]} for project in project_info]
