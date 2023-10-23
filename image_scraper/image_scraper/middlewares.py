# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy import signals

from scrapy.http import HtmlResponse
from selenium import webdriver


class SeleniumMiddleware:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options)

    def process_request(self, request, spider):
        """It's called after start_requests but before parse method, making it possible to use Selenium
        to request the page with a web driver"""
        if 'dont_proxy' in request.meta:
            return None
        self.driver.get(request.url)
        request.meta['driver'] = self.driver
        body = self.driver.page_source
        return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def spider_closed(self):
        self.driver.close()
