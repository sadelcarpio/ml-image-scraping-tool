from sqlmodel import Session

from app.models import SQLModel, UserModel, ProjectModel, UserProjectModel, UrlModel
from app.db.engine import engine


def init_db():
    SQLModel.metadata.create_all(engine)
    # Just for testing
    with Session(engine) as session:
        first_user = UserModel(username="sadelcarpio", full_name="Sergio DC",
                               email="sdelcarpio")
        session.add(first_user)
        session.commit()
        session.refresh(first_user)
        first_project = ProjectModel(name="test-project", keywords="test,testing,fastapi",
                                     description="Jajaja", owner_id=first_user.id)
        second_project = ProjectModel(name="test-project-2", keywords="test,testing,fastapi",
                                      description="XDDD", owner_id=first_user.id)
        session.add(first_project)
        session.add(second_project)
        session.commit()
        session.refresh(first_project)
        session.refresh(second_project)
        user_assignment1 = UserProjectModel(user_id=first_user.id, project_id=first_project.id)
        user_assignment2 = UserProjectModel(user_id=first_user.id, project_id=second_project.id)
        session.add(user_assignment1)
        session.add(user_assignment2)
        session.commit()
        session.refresh(user_assignment1)
        session.refresh(user_assignment2)
        urls_project_1 = [UrlModel(gcs_url=f"https://storage.googleapis.com/project_1_img_{i}.jpg",
                                   hashed_url=f"abcdefgh{i}",
                                   user_id=first_user.id,
                                   project_id=first_project.id) for i in range(3)]
        urls_project_2 = [UrlModel(gcs_url=f"https://storage.googleapis.com/project_2_img_{i}.jpg",
                                   hashed_url=f"abcdefg{i}",
                                   user_id=first_user.id,
                                   project_id=second_project.id) for i in range(3)]
        session.add_all(urls_project_1)
        session.add_all(urls_project_2)
        session.commit()
