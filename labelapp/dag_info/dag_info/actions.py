from sqlmodel import Session, select

from dag_info.models import ProjectModel, UserModel


def fetch_project_information(session: Session):
    project_info = session.exec(select(ProjectModel.name, ProjectModel.last_processed,
                                       ProjectModel.keywords, UserModel.email).join(UserModel))
    return [{"project": project[0],
             "last_processed": project[1].strftime("%Y-%m-%d %H:%M:%S.%f"),
             "keywords": project[2],
             "notify": project[3]} for project in project_info]
