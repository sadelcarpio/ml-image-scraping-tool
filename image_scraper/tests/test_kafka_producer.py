import os
import unittest
from datetime import datetime
from unittest.mock import patch, call

from image_scraper.kafka.producer import KafkaProducer


class TestKafkaProducer(unittest.TestCase):

    @patch.dict(os.environ, {"CATS_BUCKET_NAME": "test-kafka", "PROJECT_ID": "test-id"})
    @patch("datetime.datetime")
    def setUp(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 12, 4)
        self.producer = KafkaProducer(bootstrap_servers="localhost:9092", client_id='my-kafka-client')

    @patch("builtins.super")  # may behave strange when debugging
    def test_produce_urls(self, mock_super):
        filenames = ['a', 'b', 'c']
        self.producer.produce_urls('test-topic', filenames, 'gs:')
        self.assertEqual(mock_super.call_count, len(filenames))
        mock_super().produce.assert_has_calls(
            [call(topic='test-topic', value=b'gs:/test-kafka/04-12-2023/a'),
             call(topic='test-topic', value=b'gs:/test-kafka/04-12-2023/b'),
             call(topic='test-topic', value=b'gs:/test-kafka/04-12-2023/c')]
        )
