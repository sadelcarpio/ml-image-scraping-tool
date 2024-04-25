import unittest

from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select
from sqlmodel.pool import StaticPool
from starlette.testclient import TestClient

from dag_info.actions import fetch_project_information
from dag_info.main import app
from dag_info.db import get_session
from dag_info.models import UserModel, ProjectModel


def get_session_override():
    engine = create_engine(f"sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        return session


class TestGetDagInfo(unittest.TestCase):
    session = None

    @classmethod
    def setUpClass(cls):
        cls.session = get_session_override()

        def get_mock_session():
            return cls.session

        user1 = UserModel(email="user1@mail.com")
        user2 = UserModel(email="user2@mail.com")
        project1 = ProjectModel(name="test1", keywords="project1", owner_id=user1.id)
        project2 = ProjectModel(name="test2", keywords="project2", owner_id=user2.id)
        project3 = ProjectModel(name="test3", keywords="project3", owner_id=user2.id)
        cls.session.add(user1)
        cls.session.add(user2)
        cls.session.add(project1)
        cls.session.add(project2)
        cls.session.add(project3)
        cls.session.commit()

        app.dependency_overrides[get_session] = get_mock_session
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        app.dependency_overrides.clear()

    def test_fetch_project_information(self):
        results = fetch_project_information(self.session)
        self.assertEqual([
            {"project": "test1", "last_processed": "1970-01-01T00:00:00.000000",
             "keywords": "project1", "notify": "user1@mail.com"},
            {"project": "test2", "last_processed": "1970-01-01T00:00:00.000000",
             "keywords": "project2", "notify": "user2@mail.com"},
            {"project": "test3", "last_processed": "1970-01-01T00:00:00.000000",
             "keywords": "project3", "notify": "user2@mail.com"}], results)

    def test_get_dag_info(self):
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        self.assertEqual([
            {"project": "test1", "last_processed": "1970-01-01T00:00:00.000000",
             "keywords": "project1", "notify": "user1@mail.com"},
            {"project": "test2", "last_processed": "1970-01-01T00:00:00.000000",
             "keywords": "project2", "notify": "user2@mail.com"},
            {"project": "test3", "last_processed": "1970-01-01T00:00:00.000000",
             "keywords": "project3", "notify": "user2@mail.com"}], response.json())

    def test_project_deleted(self):
        project1 = self.session.exec(select(ProjectModel).where(ProjectModel.name == "test1")).one()
        self.session.delete(project1)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(2, len(data))
        self.assertEqual([
            {"project": "test2", "last_processed": "1970-01-01T00:00:00.000000",
             "keywords": "project2", "notify": "user2@mail.com"},
            {"project": "test3", "last_processed": "1970-01-01T00:00:00.000000",
             "keywords": "project3", "notify": "user2@mail.com"}], data)

    def test_update_email(self):
        user2 = self.session.exec(select(UserModel).where(UserModel.email == "user2@mail.com")).one()
        user2.email = "user2@newmail.com"
        self.session.add(user2)
        self.session.commit()
        response = self.client.get("/")
        data = response.json()
        self.assertEqual([
            {"project": "test2", "last_processed": "1970-01-01T00:00:00.000000",
             "keywords": "project2", "notify": "user2@newmail.com"},
            {"project": "test3", "last_processed": "1970-01-01T00:00:00.000000",
             "keywords": "project3", "notify": "user2@newmail.com"}], data)

    def test_user_deleted(self):
        user2 = self.session.exec(select(UserModel).where(UserModel.email == "user2@newmail.com")).one()
        self.session.delete(user2)
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual([], data)
