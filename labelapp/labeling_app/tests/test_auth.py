import unittest
import uuid
from unittest.mock import MagicMock

from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlmodel import Session

from app import create_app
from app.api.deps import get_db
from app.core.config import get_settings, Settings
from app.crud.crud_project import CRUDProject, get_projects_crud
from app.crud.crud_user import CRUDUser, get_users_crud
from app.models.users import UserModel
from app.security.auth import authenticate_user, get_current_user
from app.security.passwords import get_password_hash


class TestAuth(unittest.TestCase):
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
                                      hashed_password=get_password_hash("test-password"),
                                      email="test@test.com",
                                      id=uuid.uuid4())
        self.mock_projects_crud = MagicMock(autospec=CRUDProject)
        self.mock_users_crud = MagicMock(autospec=CRUDUser)

        def get_settings_override():
            return self.mock_settings

        def get_db_override():
            return self.mock_db

        def get_projects_crud_override():
            return self.mock_projects_crud

        def get_users_crud_override():
            return self.mock_users_crud

        app = create_app(settings=self.mock_settings)
        app.dependency_overrides[get_settings] = get_settings_override
        app.dependency_overrides[get_db] = get_db_override
        app.dependency_overrides[get_projects_crud] = get_projects_crud_override
        app.dependency_overrides[get_users_crud] = get_users_crud_override
        self.mock_users_crud.get_by_username.return_value = self.current_user
        self.test_client = TestClient(app)

    def test_authenticate_user(self):
        for passwd in ["password", "test-password", "my-pass", "contraseña"]:
            user = authenticate_user(self.mock_users_crud, "test-user", passwd)
            if passwd == "test-password":
                self.assertNotEqual(False, user)
                self.assertEqual(self.current_user, user)
            else:
                self.assertEqual(False, user)

    def test_token_endpoint(self):
        response = self.test_client.post(f"{self.mock_settings.API_V1_STR}/token",
                                         data={"username": "test-user", "password": "test-password"})
        response_dict = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9', response_dict["access_token"].split('.')[0])
        self.assertEqual('bearer', response_dict["token_type"])

    def test_token_user_not_found(self):
        self.mock_users_crud.get_by_username.return_value = None
        response = self.test_client.post(f"{self.mock_settings.API_V1_STR}/token",
                                         data={"username": "test-user", "password": "test-password"})
        self.assertEqual(401, response.status_code)
        self.assertEqual("Incorrect username or password", response.json()["detail"])

    def test_get_current_user(self):
        response = self.test_client.post(f"{self.mock_settings.API_V1_STR}/token",
                                         data={"username": "test-user", "password": "test-password"})
        token = response.json()["access_token"]
        security_scopes = MagicMock()
        # Not admin
        security_scopes.scopes = []
        security_scopes.scope_str = ""
        user = get_current_user(security_scopes, token, self.mock_users_crud)
        self.assertEqual(user, self.current_user)
        self.mock_users_crud.get_by_username.assert_called_with("test-user")

    def test_get_current_user_credentials_exception(self):
        response = self.test_client.post(f"{self.mock_settings.API_V1_STR}/token",
                                         data={"username": "test-user", "password": "test-password"})
        token = response.json()["access_token"]
        security_scopes = MagicMock()
        security_scopes.scopes = []
        security_scopes.scope_str = ""
        # For some reason the user gets deleted or it is not found on the db
        self.mock_users_crud.get_by_username.return_value = None
        with self.assertRaises(HTTPException) as e:
            user = get_current_user(security_scopes, token, self.mock_users_crud)
        self.assertEqual("Could not validate credentials", e.exception.detail)
        self.assertEqual(401, e.exception.status_code)
        self.mock_users_crud.get_by_username.assert_called_with("test-user")

    def test_get_current_user_unauthorized(self):
        response = self.test_client.post(f"{self.mock_settings.API_V1_STR}/token",
                                         data={"username": "test-user", "password": "test-password"})
        token = response.json()["access_token"]
        security_scopes = MagicMock()
        # Admin scope
        security_scopes.scopes = ["admin"]
        security_scopes.scope_str = "admin"
        with self.assertRaises(HTTPException) as e:
            user = get_current_user(security_scopes, token, self.mock_users_crud)
        self.assertEqual(401, e.exception.status_code)
        self.assertEqual("Not enough permissions", e.exception.detail)
        self.mock_users_crud.get_by_username.assert_called_with("test-user")

    def test_get_current_user_admin_scope(self):
        self.current_user.is_admin = True
        response = self.test_client.post(f"{self.mock_settings.API_V1_STR}/token",
                                         data={"username": "test-user", "password": "test-password"})
        token = response.json()["access_token"]
        security_scopes = MagicMock()
        # Admin scope
        security_scopes.scopes = ["admin"]
        security_scopes.scope_str = "admin"
        user = get_current_user(security_scopes, token, self.mock_users_crud)
        self.assertEqual(user, self.current_user)
        self.mock_users_crud.get_by_username.assert_called_with("test-user")
