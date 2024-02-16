import json
import unittest
import uuid
from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from sqlmodel import Session

from app import create_app
from app.api.deps import get_db
from app.security import get_current_user
from app.core.config import Settings, get_settings
from app.crud import CRUDUser
from app.crud.crud_project import get_projects_crud, CRUDProject
from app.crud.crud_user import get_users_crud
from app.models.projects import ProjectModel
from app.models.users import UserModel
from app.schemas.projects import ProjectRead


class TestProjectEndpoints(unittest.TestCase):

    def setUp(self):
        self.mock_settings = MagicMock(autospec=Settings)
        self.mock_settings.configure_mock(API_V1_STR="/api/v1",
                                          INSTANCE_NAME="localhost:5432",
                                          DB_USER="test",
                                          DB_PASSWORD="test",
                                          DB_NAME="test")

        self.mock_db = MagicMock(autospec=Session)
        self.current_user = UserModel(username="test-user",
                                      full_name="Test User",
                                      email="test@test.com",
                                      id=uuid.uuid4())
        self.mock_projects_crud = MagicMock(autospec=CRUDProject)
        self.mock_users_crud = MagicMock(autospec=CRUDUser)

        def get_settings_override():
            return self.mock_settings

        def get_db_override():
            return self.mock_db

        def get_user_override():
            return self.current_user

        def get_projects_crud_override():
            return self.mock_projects_crud

        def get_users_crud_override():
            return self.mock_users_crud

        app = create_app(settings=self.mock_settings)
        app.dependency_overrides[get_settings] = get_settings_override
        app.dependency_overrides[get_db] = get_db_override
        app.dependency_overrides[get_current_user] = get_user_override
        app.dependency_overrides[get_projects_crud] = get_projects_crud_override
        app.dependency_overrides[get_users_crud] = get_users_crud_override
        self.test_client = TestClient(app)

    def test_get_project(self):
        project_model = ProjectModel(name="test-proj",
                                     keywords="key1,key2",
                                     description="Test get endpoint.",
                                     task_type="classification",
                                     owner_id=self.current_user.id)
        self.mock_projects_crud.get.return_value = project_model
        response = self.test_client.get(f"{self.mock_settings.API_V1_STR}/projects/1")
        project_read = ProjectRead.model_validate(project_model)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(), json.loads(project_read.model_dump_json()))

    def test_get_project_no_id(self):
        self.mock_projects_crud.get.return_value = None
        response = self.test_client.get(f"{self.mock_settings.API_V1_STR}/projects/1")
        self.assertEqual(404, response.status_code)
        self.assertEqual("No such project with id: 1", response.json()["detail"])

    def test_add_user_wrong_method(self):
        project_model = ProjectModel(name="test-proj",
                                     keywords="key1,key2",
                                     description="Test get endpoint.",
                                     task_type="classification",
                                     owner_id=self.current_user.id)
        self.mock_projects_crud.get.return_value = project_model
        response = self.test_client.get(f"{self.mock_settings.API_V1_STR}/projects/1/{str(self.current_user.id)}")
        self.assertEqual(405, response.status_code)
        self.assertEqual("Method Not Allowed", response.json()["detail"])

    def test_add_user_no_body(self):
        project_model = ProjectModel(name="test-proj",
                                     keywords="key1,key2",
                                     description="Test get endpoint.",
                                     task_type="classification",
                                     owner_id=self.current_user.id)
        self.mock_projects_crud.get.return_value = project_model
        self.mock_users_crud.get.return_value = self.current_user
        response = self.test_client.put(f"{self.mock_settings.API_V1_STR}/projects/1/{str(self.current_user.id)}")
        self.assertEqual(204, response.status_code)
        self.assertEqual(b'', response.content)

    def test_add_user_no_id(self):
        self.mock_users_crud.get.return_value = None
        response = self.test_client.put(f"{self.mock_settings.API_V1_STR}/projects/1/{str(self.current_user.id)}")
        self.assertEqual(404, response.status_code)
        self.assertEqual(f"No user found with id: {str(self.current_user.id)}", response.json()["detail"])
