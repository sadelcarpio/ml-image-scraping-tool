from sqlmodel import SQLModel
from sqlmodel import Session

from app import Settings
from app.crud import CRUDUser, CRUDProject
from app.db.engine import get_engine
from app.models.extras import LabelModel
from app.models.projects import ProjectModel
from app.models.urls import UrlModel
from app.models.users import UserModel
from app.schemas.projects import ProjectCreateWithUsers
from app.schemas.users import UserCreate


def init_db():
    engine = get_engine(settings=Settings())
    SQLModel.metadata.create_all(engine)
    # Just for testing CRUD operations
    with Session(engine) as session:
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
        projects_crud.create_with_users(obj_in=ProjectCreateWithUsers(name="test-project-full",
                                                                      keywords="gatitos+chidos",
                                                                      description="This is a test",
                                                                      task_type="classification",
                                                                      labels=[label1, label2],
                                                                      user_ids=[user_1.id],
                                                                      owner_id=user.id))

        project = projects_crud.get(1)
        urls = [UrlModel(gcs_url=f"https://www.google.com/image_{i}",
                         hashed_url=f"abcdef{i}",
                         user_id=user_1.id,
                         project_id=project.id) for i in range(10)]
        session.add_all(urls)
        session.commit()
