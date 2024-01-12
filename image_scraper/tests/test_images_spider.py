import unittest
from unittest.mock import patch

from image_scraper.spiders.images_spider import GoogleImagesSpider


# patching time.sleep in class scope may bring unexpected behavior while debugging
@patch('time.sleep')
class GoogleImagesSpiderTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spider = GoogleImagesSpider(scraping_project='test-project')

    def test_scrape_image_url(self, mock_time):
        self.assertTrue(hasattr(self.spider, 'job_timestamp'))
        self.assertTrue(hasattr(self.spider, 'scraping_project'))
        with patch.object(self.spider, 'driver'):
            result = list(self.spider.scrape_image_url())
            expected_calls = [('xpath', f'{self.spider.base_path}//a/img[1]'),
                              ('xpath', f'{self.spider.base_path}//div[1]/div/div[2]/div[2]/button')]
            actual_calls = [call_obj.args for call_obj in self.spider.driver.find_element.call_args_list]
            self.assertEqual(expected_calls, actual_calls)

    @patch('scrapy.http.HtmlResponse')
    def test_parse(self, mock_response, mock_time):
        with patch.object(self.spider, 'driver'), patch.object(self.spider, 'scrape_image_url'):
            result = list(self.spider.parse(mock_response))
            expected_calls = [5, 10, 10, 10, 10, 10]
            actual_calls = [call_obj.args[0] for call_obj in mock_time.call_args_list]
            self.assertEqual(expected_calls, actual_calls)
