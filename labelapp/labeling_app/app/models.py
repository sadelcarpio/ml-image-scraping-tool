import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, create_engine
from sqlmodel import SQLModel, Field, Relationship, Session, select


class UrlModel(SQLModel, table=True):
    __tablename__ = "urls"
    id: int | None = Field(default=None, primary_key=True)
    gcs_url: str = Field(unique=True, nullable=False)
    created_at: datetime = Field(index=True, default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        sa_column=Column(DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    )
    labeled: bool
    user_id: uuid.UUID | None = Field(default=None, foreign_key="users.id")
    project_id: int | None = Field(default=None, foreign_key="projects.id")


class UserProjectModel(SQLModel, table=True):
    __tablename__ = "users_projects"
    id: int | None = Field(default=None, primary_key=True)
    user_id: uuid.UUID | None = Field(default_factory=uuid.uuid4, foreign_key="users.id", primary_key=True)
    project_id: int | None = Field(default=None, foreign_key="projects.id", primary_key=True)


class UserModel(SQLModel, table=True):
    __tablename__ = "users"
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str | None = Field(default=None, nullable=False)
    email: str
    created_at: datetime = Field(index=True, default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        sa_column=Column(DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    )
    projects: list["ProjectModel"] = Relationship(back_populates="users", link_model=UserProjectModel)


class ProjectModel(SQLModel, table=True):
    __tablename__ = "projects"
    id: int | None = Field(default=None, primary_key=True, index=True)
    name: str
    keywords: str
    description: str
    created_at: datetime = Field(index=True, default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        sa_column=Column(DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    )
    owner_id: uuid.UUID = Field(default=None, foreign_key="users.id")
    users: list[UserModel] = Relationship(back_populates="projects", link_model=UserProjectModel)


# sqlite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"
# postgres_url = "postgresql+pg8000://db_user:password@localhost:5432/db_name"
# engine = create_engine(postgres_url, echo=True)
#
#
# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)
#
#
# def create_projects():
#     with Session(engine) as session:
#         user1 = UserModel(name="Sergio Del Carpio", email="sdelcarpioa@uni.pe")
#         user2 = UserModel(name="Dora Cerron", email="dcerron.c@uni.pe")
#         session.add(user1)
#         session.add(user2)
#         session.commit()
#         session.refresh(user1)
#         session.refresh(user2)
#         project1 = ProjectModel(name="sergio", keywords="empty", description="Ejemplo xd.",
#                                 owner_id=user1.id)
#         project2 = ProjectModel(name="dora", keywords="empty", description="Ejemplo 2 xd.",
#                                 owner_id=user2.id)
#         project1.users = [user1, user2]
#         project2.users = [user2, user1]
#         session.add(project1)
#         session.add(project2)
#         session.commit()
#
#
# def fetch_urls():
#     with Session(engine) as session:
#         urls = session.exec(select(UrlModel)).all()
#         print(urls)
#
#
# if __name__ == "__main__":
#     create_db_and_tables()
#     fetch_urls()
