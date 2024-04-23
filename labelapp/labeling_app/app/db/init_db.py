from sqlalchemy import exc
from sqlmodel import SQLModel
from sqlmodel import Session

from app import Settings
from app.crud import CRUDUser, CRUDProject
from app.db.engine import get_engine
from app.models.extras import LabelModel
from app.models.projects import ProjectModel
from app.models.urls import UrlModel
from app.models.users import UserModel
from app.schemas.extras import TaskType
from app.schemas.projects import ProjectCreateWithUsers
from app.schemas.users import UserCreate


def init_db():
    engine = get_engine(settings=Settings())
    SQLModel.metadata.create_all(engine)
    # Just for testing CRUD operations
    with Session(engine) as session:
        try:
            users_crud = CRUDUser(UserModel, session)
            projects_crud = CRUDProject(ProjectModel, session)
            my_user = users_crud.create_with_pwd_hashing(obj_in=UserCreate(username="sergio",
                                                                           email="sergio@gmail.com",
                                                                           is_admin=True,
                                                                           password="sacarracatelas",
                                                                           full_name="Sergio"))
            user_1 = users_crud.create_with_pwd_hashing(obj_in=UserCreate(username="sadel",
                                                                          email="sadel@gmail.com",
                                                                          is_admin=False,
                                                                          password="sacarracatelas",
                                                                          full_name="Sergio"))
            user_2 = users_crud.create_with_pwd_hashing(obj_in=UserCreate(username="sadel2",
                                                                          email="sadel2@gmail.com",
                                                                          is_admin=False,
                                                                          password="sacarracatelas",
                                                                          full_name="Sergio"))
            user = users_crud.get(my_user.id)
            user_1 = users_crud.get(user_1.id)
            label1 = LabelModel(name="cat")
            label2 = LabelModel(name="dog")
            label3 = LabelModel(name="a")
            label4 = LabelModel(name="b")
            projects_crud.create_with_users(obj_in=ProjectCreateWithUsers(name="test-project-full",
                                                                          keywords="gatitos+chidos",
                                                                          description="This is a test",
                                                                          task_type=TaskType.sparse,
                                                                          labels=[label1, label2],
                                                                          user_ids=[user_1.id]),
                                            owner_id=user.id)
            projects_crud.create_with_users(obj_in=ProjectCreateWithUsers(name="Airlplane-Properties-Prediction",
                                                                          keywords="airplanes",
                                                                          description="This is a test",
                                                                          task_type=TaskType.sparse,
                                                                          labels=[label3, label4],
                                                                          user_ids=[user_1.id, user_2.id]),
                                            owner_id=user.id)
            project_1 = projects_crud.get(1)
            project_2 = projects_crud.get(2)
            urls_project_1 = [UrlModel(gcs_url=f"https://www.google.com/image_{i}_project_1",
                                       hashed_url=f"abcdefp1{i}",
                                       user_id=user_1.id,
                                       project_id=project_1.id) for i in range(10)]
            session.add_all(urls_project_1)
            session.commit()
            urls_project_2 = [UrlModel(gcs_url=f"https://www.google.com/image_{i}_project_2",
                                       hashed_url=f"abcdefp2{i}",
                                       user_id=user_1.id,
                                       project_id=project_2.id) for i in range(10)]
            session.add_all(urls_project_2)
            session.commit()
        except exc.IntegrityError:
            pass
