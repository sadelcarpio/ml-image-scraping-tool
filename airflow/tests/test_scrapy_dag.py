import unittest
from unittest.mock import patch, MagicMock

import requests
from airflow.models import DagBag
from dags.utils.scrapyd_request import check_status


class TestScrapyDag(unittest.TestCase):

    @unittest.skip  # temporarily disable this test since it does not work on Windows
    def test_dag_loads_with_no_errors(self):
        """Test the dag loads without any import errors"""
        dag_bag = DagBag(include_examples=False)
        dag_bag.process_file('../dags/scrapy_dag.py')
        self.assertEqual(0, len(dag_bag.import_errors))

    @patch('time.sleep', MagicMock())
    @patch('requests.get')
    def test_check_status(self, mock_get):
        running_response = MagicMock()
        running_response.raise_for_status = MagicMock()
        running_response.json.return_value = {'running': [{'id': '1234'}], 'finished': []}
        finished_response = MagicMock()
        finished_response.raise_for_status = MagicMock()
        finished_response.json.return_value = {'running': [], 'finished': [{'id': '1234'}]}
        # Get running status 3 times and finishes with a finished status
        mock_get.side_effect = [running_response, running_response, running_response, finished_response]
        check_status()
        self.assertEqual(4, len(mock_get.call_args_list))
        self.assertEqual(6, len(running_response.json.call_args_list))
        self.assertEqual(2, len(finished_response.json.call_args_list))

    @patch('requests.get')
    @patch('time.sleep', MagicMock())
    def test_check_status_error_handling(self, mock_get):
        error_response = MagicMock()
        error_response.raise_for_status.side_effect = requests.exceptions.RequestException
        mock_get.return_value = error_response
        check_status()
        error_response.raise_for_status.assert_called_once()
