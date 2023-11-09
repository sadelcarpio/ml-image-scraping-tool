import os
import unittest
from unittest.mock import MagicMock, patch, call

from image_scraper.kafka.producer import KafkaProducer
from image_scraper.pipelines import URLImagesPipeline


class TestURLImagesPipeline(unittest.TestCase):

    @patch('image_scraper.pipelines.KafkaProducer')
    @patch.dict(os.environ, {'KAFKA_LISTENER': 'localhost:9092'})
    def setUp(self, mock_producer):
        mock_settings = MagicMock()
        self.pipeline = URLImagesPipeline('my-gcs-bucket', settings=mock_settings)

    @patch('image_scraper.pipelines.KafkaProducer')
    @patch('image_scraper.pipelines.logger')
    @patch('builtins.super')
    @patch.dict(os.environ, {'KAFKA_LISTENER': 'localhost:9092'})
    def test_from_settings(self, mock_super, mock_logger, mock_producer):
        mock_settings = MagicMock()
        mock_super().from_settings.return_value = MagicMock(spec=URLImagesPipeline)
        pipeline_from_settings = URLImagesPipeline.from_settings(mock_settings)
        mock_super().from_settings.assert_called_with(mock_settings)
        mock_logger.debug.assert_has_calls([call('Setting up Kafka Producer ...'), call('Kafka Producer set up.')])
        mock_producer.assert_called_with(bootstrap_servers='localhost:9092', client_id='scrapyd')
        self.assertIsInstance(pipeline_from_settings, URLImagesPipeline)

    @patch('scrapy.Request')
    def test_get_media_requests(self, mock_requests):
        mock_item = {'image_urls': ['http://example.com/image1.jpg', 'http://example.com']}
        mock_info = MagicMock()
        result = list(self.pipeline.get_media_requests(mock_item, mock_info))
        mock_requests.assert_has_calls([call('http://example.com/image1.jpg', meta={'dont_proxy': True}),
                                        call('http://example.com', meta={'dont_proxy': True})])
        self.assertEqual(len(mock_requests.call_args_list), 2)
