import unittest
from unittest.mock import patch, MagicMock

from image_scraper.middlewares import SeleniumMiddleware
from image_scraper.spiders.images_spider import GoogleImagesSpider


class GoogleImagesSpiderTest(unittest.TestCase):
    @patch('selenium.webdriver.Chrome')
    def setUp(self, mock_webdriver):
        mock_driver = MagicMock()
        mock_webdriver.return_value = mock_driver
        self.middleware = SeleniumMiddleware()
        self.assertEqual(self.middleware.driver, mock_driver)
        self.spider = GoogleImagesSpider()
