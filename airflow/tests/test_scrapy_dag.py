import json
import unittest
from sys import platform
from unittest.mock import patch, MagicMock

import requests
from airflow.models import DagBag

from dags.tasks import check_scraping_status


class TestScrapyDag(unittest.TestCase):

    @unittest.skipUnless(platform != "win32", "Disable only for Windows")
    @patch('requests.get')
    def test_dag_loads_with_no_errors(self, mock_get):
        """Test the dag loads without any import errors"""
        mock_get.return_value.json.return_value = []
        dag_bag = DagBag(include_examples=False)
        dag_bag.process_file('../dags/scrapy_dag.py')
        self.assertEqual(0, len(dag_bag.import_errors))

    @patch('time.sleep', MagicMock())
    @patch('requests.get')
    @patch('logging.getLogger')
    def test_check_status(self, mock_getlogger, mock_get):
        mock_ti = MagicMock()
        mock_ti.xcom_pull.return_value = {"jobid": "1234", "status": "ok"}
        mock_logger = MagicMock()
        mock_getlogger.return_value = mock_logger
        running_response = MagicMock()
        running_response.raise_for_status = MagicMock()
        running_response.json.return_value = {'running': [{'id': '1234'}, {'id': '4321'}], 'finished': [{'id': 'abc'}]}
        finished_response = MagicMock()
        finished_response.raise_for_status = MagicMock()
        finished_response.json.return_value = {'running': [{'id': '4321'}], 'finished': [{'id': '1234'}, {'id': 'abc'}]}
        # Get running status 3 times and finishes with a finished status
        mock_get.side_effect = [running_response, running_response, running_response, finished_response]
        check_scraping_status.function(ti=mock_ti)
        self.assertEqual(4, len(mock_get.call_args_list))
        self.assertEqual(6, len(running_response.json.call_args_list))
        self.assertEqual(2, len(finished_response.json.call_args_list))
        self.assertEqual("Web scraping finished: {'id': '1234'}",
                         mock_logger.info.call_args_list[-1][0][0])

    @patch('requests.get')
    @patch('time.sleep', MagicMock())
    @patch('json.loads', MagicMock())
    def test_check_status_error_handling(self, mock_get):
        mock_ti = MagicMock()
        error_response = MagicMock()
        error_response.raise_for_status.side_effect = requests.exceptions.RequestException
        mock_get.return_value = error_response
        check_scraping_status.function(ti=mock_ti)
        error_response.raise_for_status.assert_called_once()
