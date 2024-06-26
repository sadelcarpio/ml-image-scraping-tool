import unittest
import uuid
from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from sqlmodel import Session

from app import create_app
from app.api.deps import get_db
from app.core.config import Settings, get_settings
from app.models.extras import UserProjectModel
from app.models.urls import UrlModel
from app.models.users import UserModel
from app.security.auth import get_current_user


class TestUrlEndpoints(unittest.TestCase):

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
                                      email="test@test.com")

        def get_settings_override():
            return self.mock_settings

        def get_db_override():
            return self.mock_db

        def get_user_override():
            return self.current_user

        app = create_app(settings=self.mock_settings)
        app.dependency_overrides[get_settings] = get_settings_override
        app.dependency_overrides[get_db] = get_db_override
        app.dependency_overrides[get_current_user] = get_user_override
        self.test_client = TestClient(app)

    def test_current_url_no_unlabeled_urls_error(self):
        """Tests 404 response in case of no unlabeled URLs found."""
        self.mock_db.exec.return_value.first.return_value = None
        response = self.test_client.get(f"{self.mock_settings.API_V1_STR}/urls/1/current-url")
        self.assertEqual("Didn't find any unlabeled urls.", response.json()["detail"])
        self.assertEqual(404, response.status_code)

    def test_submit_url_no_current_url(self):
        """Tests that /submit endpoint called before /current-url gives an HTTP Exception."""
        self.mock_db.exec.return_value.all.return_value = ["cat", "dog"]
        self.mock_db.exec.return_value.first.return_value = None
        response = self.test_client.put(f"{self.mock_settings.API_V1_STR}/urls/1/submit-url",
                                        json=["cat"])
        self.assertEqual("Error in selecting URL to submit. Be sure to have called"
                         " /current-url endpoint first", response.json()["detail"])
        self.assertEqual(404, response.status_code)

    def test_current_url_returned(self):
        """Test Url is displayed correctly and updates current_url in user assignment."""
        user_id = uuid.uuid4()
        url_to_return = UrlModel(id=1, gcs_url="https://test.jpg", hashed_url="abcdefg", labeled=False,
                                 user_id=user_id, project_id=1)
        user_assignment = UserProjectModel(user_id=user_id, project_id=1)
        self.mock_db.exec.return_value.first.side_effect = [url_to_return, user_assignment]
        response = self.test_client.get(f"{self.mock_settings.API_V1_STR}/urls/1/current-url")
        self.assertEqual(1, user_assignment.current_url)
        self.mock_db.add.assert_called_once_with(user_assignment)
        self.mock_db.commit.assert_called_once()
        self.assertEqual(200, response.status_code)
        self.assertEqual({"gcs_url": url_to_return.gcs_url,
                          "id": url_to_return.id,
                          "labeled": False,
                          "user_id": str(user_id)}, response.json())
        self.assertEqual(user_assignment.current_url, url_to_return.id)

    def test_submit_url(self):
        """Test submit-url endpoint updates labeled status."""
        url_to_submit = UrlModel(id=1, gcs_url="https://test.jpg", hashed_url="abcdefg", labeled=False,
                                 user_id="uid1", project_id=1)
        self.mock_db.exec.return_value.all.return_value = ["cat", "dog"]
        self.mock_db.exec.return_value.first.side_effect = [url_to_submit, 1, 2]
        response = self.test_client.put(f"{self.mock_settings.API_V1_STR}/urls/1/submit-url",
                                        json=["cat"])
        self.assertEqual(204, response.status_code)
        self.assertEqual(b'', response.content)
        self.assertTrue(url_to_submit.labeled)
        self.assertEqual(2, len(self.mock_db.add.call_args_list))
        self.assertEqual(2, len(self.mock_db.commit.call_args_list))
        self.mock_db.refresh.assert_called_once_with(url_to_submit)

    def test_submit_labels_not_allowed(self):
        """Tests that /submit endpoint with wrong labels raises a 400 error"""
        self.mock_db.exec.return_value.all.return_value = ["cat", "dog"]
        self.mock_db.exec.return_value.first.return_value = None
        response = self.test_client.put(f"{self.mock_settings.API_V1_STR}/urls/1/submit-url",
                                        json=["rex"])
        self.assertEqual("Labels not allowed. Valid labels are ['cat', 'dog']", response.json()["detail"])
        self.assertEqual(400, response.status_code)
