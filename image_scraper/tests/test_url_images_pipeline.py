import os
import unittest
from unittest.mock import MagicMock, patch, call

import scrapy

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
        self.pipeline = URLImagesPipeline.from_settings(mock_settings)
        mock_super().from_settings.assert_called_with(mock_settings)
        mock_logger.debug.assert_has_calls([call('Setting up Kafka Producer ...'), call('Kafka Producer set up.')])
        mock_producer.assert_called_with(bootstrap_servers='localhost:9092', client_id='scrapyd')
        self.assertIsInstance(self.pipeline, URLImagesPipeline)

    @patch('scrapy.Request')
    def test_get_media_requests(self, mock_requests):
        mock_item = {'image_urls': ['http://example.com/image1.jpg', 'http://example.com']}
        mock_info = MagicMock()
        result = list(self.pipeline.get_media_requests(mock_item, mock_info))
        mock_requests.assert_has_calls([call('http://example.com/image1.jpg', meta={'dont_proxy': True}),
                                        call('http://example.com', meta={'dont_proxy': True})])
        self.assertEqual(2, len(mock_requests.call_args_list))

    @patch('image_scraper.pipelines.logger')
    def test_item_completed(self, mock_logger):
        mock_results = [(True, {'url': 'https://example.com/image1.jpg', 'path': 'abcdefg.jpg', 'checksum': '123456',
                                'status': 'downloaded'})]
        mock_item = {'image_urls': ['https://example.com/image1.jpg']}
        expected_item = {'image_urls': ['https://example.com/image1.jpg'],
                         'images': ['abcdefg.jpg']}
        self.pipeline.producer = MagicMock(spec=KafkaProducer)
        actual_item = self.pipeline.item_completed(results=mock_results, item=mock_item, info=MagicMock())
        mock_logger.debug.assert_has_calls([call("Sending GCS URL for ['abcdefg.jpg'] ..."),
                                            call("GCS URLs sent.")])
        self.pipeline.producer.produce_urls.assert_called_with(topic='google-images',
                                                               filenames=['abcdefg.jpg'],
                                                               prefix='https://storage.googleapis.com')
        self.assertEqual(expected_item, actual_item)

    def test_filepath(self):
        mock_request = MagicMock(spec=scrapy.Request, url='https://example.com/image1.jpg')
        expected_filepath = '15de8280f794673ca19a187bc85cd573cfdcf3ac.jpg'
        actual_filepath = self.pipeline.file_path(mock_request)
        self.assertEqual(expected_filepath, actual_filepath)
