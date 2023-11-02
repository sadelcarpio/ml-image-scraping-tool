import unittest
from unittest.mock import patch, MagicMock, call

from scrapy.http import HtmlResponse

from image_scraper.middlewares import SeleniumMiddleware


class SeleniumMiddlewareTest(unittest.TestCase):
    @patch('selenium.webdriver.Chrome')
    def setUp(self, mock_webdriver):
        mock_driver = MagicMock()
        mock_webdriver.return_value = mock_driver
        self.middleware = SeleniumMiddleware()
        self.assertEqual(self.middleware.driver, mock_driver)

    @patch('image_scraper.middlewares.webdriver.ChromeOptions')
    @patch('selenium.webdriver.Chrome')
    def test_middleware_init(self, mock_chrome, mock_chrome_options):
        mock_options = MagicMock()
        mock_chrome_options.return_value = mock_options
        middleware = SeleniumMiddleware()
        expected_calls = ['--no-sandbox', '--window-size=1920,1080',
                          '--headless', '--disable-gpu', '--disable-dev-shm-usage']
        actual_calls = [call_obj.args[0] for call_obj in mock_options.add_argument.call_args_list]
        self.assertEqual(expected_calls, actual_calls)

    @patch('image_scraper.middlewares.HtmlResponse')
    def test_process_request(self, mock_response):
        mock_request = MagicMock(url='https://example.com')
        mock_spider = MagicMock()
        valid_response = HtmlResponse(
            url='https://example.com',
            body=b"<html>Hello World</html>"
        )
        mock_response.return_value = valid_response
        processed_response = self.middleware.process_request(mock_request, mock_spider)
        self.middleware.driver.get.assert_called_with(mock_request.url)
        assert isinstance(processed_response, HtmlResponse)

    @patch('scrapy.Request')
    def test_process_request_dont_proxy(self, mock_request):
        mock_spider = MagicMock()
        mock_request.meta = {'dont_proxy': True}
        processed_response = self.middleware.process_request(mock_request, mock_spider)
        assert processed_response is None

    @patch.object(SeleniumMiddleware, '__init__', lambda x: None)
    @patch('image_scraper.middlewares.signals')
    def test_from_crawler(self, mock_signals):
        mock_crawler = MagicMock()
        middleware = SeleniumMiddleware.from_crawler(mock_crawler)
        assert isinstance(middleware, SeleniumMiddleware)
        assert mock_crawler.signals.connect.call_args == call(
            middleware.spider_closed, mock_signals.spider_closed
        )

    def test_spider_closed(self):
        self.middleware.spider_closed()
        assert self.middleware.driver.close().called_once()
