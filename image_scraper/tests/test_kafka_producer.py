import os
import unittest
from datetime import datetime
from unittest.mock import patch, call

from image_scraper.kafka.producer import KafkaProducer


class TestKafkaProducer(unittest.TestCase):

    @patch.dict(os.environ, {"IMAGES_BUCKET_NAME": "test-kafka", "PROJECT_ID": "test-id"})
    def setUp(self):
        self.producer = KafkaProducer(bootstrap_servers="localhost:9092", client_id='my-kafka-client')

    @patch("builtins.super")  # may behave strange when debugging
    def test_produce_urls(self, mock_super):
        filenames = ['a', 'b', 'c']
        self.producer.produce_urls('test-topic', filenames, 'test-project', 'gs:')
        self.assertEqual(len(filenames), mock_super.call_count)
        mock_super().produce.assert_has_calls(
            [call(topic='test-topic', value=b'{"url": "gs:/test-kafka/a", "project": "test-project"}'),
             call(topic='test-topic', value=b'{"url": "gs:/test-kafka/b", "project": "test-project"}'),
             call(topic='test-topic', value=b'{"url": "gs:/test-kafka/c", "project": "test-project"}')]
        )
