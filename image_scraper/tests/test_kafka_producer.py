import os
import unittest
from unittest.mock import patch, call, MagicMock

import confluent_kafka

from image_scraper.events.publish import KafkaProducer


class TestKafkaProducer(unittest.TestCase):

    @patch.dict(os.environ, {"IMAGES_BUCKET_NAME": "test-kafka", "PROJECT_ID": "test-id"})
    def setUp(self):
        self.producer = KafkaProducer(bootstrap_servers="localhost:9092", client_id='my-kafka-client')
        self.producer.client = MagicMock()
        self.mock_client = self.producer.client

    def test_send_urls(self):
        filenames = ['a', 'b', 'c']
        self.producer.send_urls('test-topic', filenames, 'test-project', 'gs:')
        self.assertEqual(len(filenames), self.mock_client.produce.call_count)
        self.mock_client.produce.assert_has_calls(
            [call(topic='test-topic', value=b'{"url": "gs:/test-kafka/a", "project": "test-project"}'),
             call(topic='test-topic', value=b'{"url": "gs:/test-kafka/b", "project": "test-project"}'),
             call(topic='test-topic', value=b'{"url": "gs:/test-kafka/c", "project": "test-project"}')]
        )
