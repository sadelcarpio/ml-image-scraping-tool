from sqlmodel import Session, select

from dag_info.models import ProjectModel, UserModel


def fetch_project_information(session: Session):
    projects = list(session.exec(select(ProjectModel)))
    user_emails = [session.exec(select(UserModel.email).where(UserModel.id == project.owner_id)).first()
                   for project in projects]
    return [{"project": project.name,
             "keywords": project.keywords,
             "notify": user_email} for project, user_email in zip(projects, user_emails)]
