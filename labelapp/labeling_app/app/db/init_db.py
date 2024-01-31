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
    users_crud = CRUDUser(UserModel)
    projects_crud = CRUDProject(ProjectModel)
    with Session(engine) as session:
        my_user = users_crud.create(session, obj_in=UserCreate(username="sergio",
                                                               email="sergio@gmail.com",
                                                               is_admin=True,
                                                               password="123456",
                                                               full_name="Sergio"))
        user = users_crud.get(session, my_user.id)
        label1 = LabelModel(name="cat")
        label2 = LabelModel(name="dog")
        projects_crud.create_with_users(session, obj_in=ProjectCreateWithUsers(name="test",
                                                                               keywords="test,test2",
                                                                               description="This is a test",
                                                                               task_type="classification",
                                                                               labels=[label1, label2],
                                                                               user_ids=[user.id],
                                                                               owner_id=user.id))

        project = projects_crud.get(session, 1)
        urls = [UrlModel(gcs_url=f"https://www.google.com/image_{i}",
                         hashed_url=f"abcdef{i}",
                         user_id=my_user.id,
                         project_id=project.id) for i in range(10)]
        session.add_all(urls)
        session.commit()
