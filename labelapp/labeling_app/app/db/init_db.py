from sqlmodel import Session

from app.models import SQLModel, UserModel, ProjectModel, UserProjectModel, UrlModel
from app.db.engine import engine


def init_db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        first_user = UserModel(username="sadelcarpio", full_name="Sergio DC",
                               email="sdelcarpioa@uni.pe")
        session.add(first_user)
        session.commit()
        session.refresh(first_user)
        first_project = ProjectModel(name="test-project", keywords="test,testing,fastapi",
                                     description="Jajaja", owner_id=first_user.id)
        session.add(first_project)
        session.commit()
        session.refresh(first_project)
        user_assignment = UserProjectModel(user_id=first_user.id, project_id=first_project.id)
        session.add(user_assignment)
        session.commit()
        session.refresh(user_assignment)
        url = UrlModel(gcs_url="https://storage.googleapis.com/my_img.jpg",
                       hashed_url="abcdefg",
                       labeled=False,
                       user_id=first_user.id,
                       project_id=first_project.id)
        session.add(url)
        session.commit()
        session.refresh(url)
