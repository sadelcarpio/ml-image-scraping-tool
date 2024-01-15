from unittest import TestCase
from unittest.mock import MagicMock, patch

from dag_info.actions import fetch_project_information
from dag_info.db import get_session
from dag_info.models import UserModel
from fastapi.testclient import TestClient


class TestGetInfo(TestCase):

    @patch('dag_info.actions.select')
    def test_fetch_project_information(self, mock_select):
        mock_session = MagicMock()
        user = UserModel(email='test@test.test')
        project = [("test-project", "super,cool", "test@test.test")]
        user_result_mock = MagicMock()
        mock_session.exec.side_effect = [project]
        user_result_mock.first.return_value = user.email
        results = fetch_project_information(mock_session)
        self.assertEqual(1, len(results))
        self.assertDictEqual({
            "project": "test-project",
            "keywords": "super,cool",
            "notify": "test@test.test"
        }, results[0])
        self.assertEqual(1, len(mock_session.exec.call_args_list))
        self.assertEqual(1, len(mock_select.call_args_list))

    @patch('dag_info.actions.fetch_project_information')
    def test_get_dag_info(self, mock_fetch_project_information):
        mock_session = MagicMock()
        from dag_info.main import app
        app.dependency_overrides[get_session] = lambda: mock_session
        expected_result = [{
            "project": "test-project",
            "keywords": "super,cool",
            "notify": "test@test.test"
        }]
        mock_fetch_project_information.return_value = expected_result
        client = TestClient(app)
        response = client.get("/")
        app.dependency_overrides.clear()
        data = response.json()
        self.assertEqual(expected_result, data)
