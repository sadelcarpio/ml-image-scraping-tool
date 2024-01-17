import unittest
from unittest.mock import patch, MagicMock, call

from url_app.db.db_operations import SQLSession
from url_app.kafka.consumer import KafkaConsumer


class SpecialException(Exception):
    pass


@patch('url_app.kafka.consumer.logger')
@patch.object(KafkaConsumer, 'poll')
@patch.object(KafkaConsumer, 'close')
class TestKafkaConsumer(unittest.TestCase):

    @patch.object(KafkaConsumer, 'subscribe')
    @patch.object(KafkaConsumer, 'poll')
    def setUp(self, mock_poll, mock_subscribe):
        self.sql_session = MagicMock(spec=SQLSession)
        with patch("builtins.super"):  # just to patch the __init__ of Consumer class
            self.kafka_consumer = KafkaConsumer(bootstrap_servers='localhost:9092', group_id='test',
                                                topic='test-google-images', sql_session=self.sql_session)
        self.kafka_consumer.logger = MagicMock()
        mock_subscribe.assert_called_once_with(['test-google-images'])

    @patch('url_app.kafka.consumer.sha256_hash', MagicMock(side_effect=['hash1', 'hash2']))
    def test_kafka_read_urls(self, mock_close, mock_poll, mock_logger):
        msg1 = MagicMock()
        msg1.error.return_value = False
        msg1.value.return_value = b'{"url": "first_url", "project": "test-project-1"}'
        msg2 = MagicMock()
        msg2.error.return_value = False
        msg2.value.return_value = b'{"url": "second_url", "project": "test-project-2"}'
        mock_poll.side_effect = [None, msg1, msg2, SpecialException]
        with self.assertRaises(SpecialException):
            self.kafka_consumer.read_urls()
        mock_logger.info.assert_has_calls([
            call("Waiting ..."),
            call("Consumed event from topic test-google-images: url = first_url, project = test-project-1"),
            call("Consumed event from topic test-google-images: url = second_url, project = test-project-2"),
        ])
        self.sql_session.upload_url.assert_has_calls([
            call(gcs_url='first_url', hashed_url='hash1', project_name='test-project-1',
                 dist_strategy=self.kafka_consumer.strategy),
            call(gcs_url='second_url', hashed_url='hash2', project_name='test-project-2',
                 dist_strategy=self.kafka_consumer.strategy)
        ])
        mock_close.assert_called_once()

    def test_kafka_error_msg(self, mock_close, mock_poll, mock_logger):
        err_msg = MagicMock()
        err_msg.error.return_value = "An error happened"
        mock_poll.side_effect = [err_msg, SpecialException]
        with self.assertRaises(SpecialException):
            self.kafka_consumer.read_urls()
        mock_logger.info.assert_not_called()
        mock_logger.warning.assert_called_with(f"ERROR: {err_msg.error()}")
        mock_close.assert_called_once()
