from sqlmodel import Session

from app import Settings
from app.crud import CRUDUser, CRUDProject
from app.db.engine import get_engine
from app.models import SQLModel, UserModel, ProjectModel, LabelModel
from app.schemas.projects import ProjectCreate
from app.schemas.users import UserCreate


def init_db():
    engine = get_engine(settings=Settings())
    SQLModel.metadata.create_all(engine)
    # Just for testing CRUD operations
    user_crud = CRUDUser(UserModel)
    projects_crud = CRUDProject(ProjectModel)
    with Session(engine) as session:
        my_user = user_crud.create(session, obj_in=UserCreate(username="sergio",
                                                              email="sergio@gmail.com",
                                                              is_admin=True,
                                                              password="123456",
                                                              full_name="Sergio"))
        label1 = LabelModel(name="cat")
        label2 = LabelModel(name="dog")
        projects_crud.create_with_labels(session,
                                         obj_in=ProjectCreate(name="test",
                                                              keywords="test,test2",
                                                              description="This is a test",
                                                              owner_id=my_user.id),
                                         labels=[label1, label2])
