# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy import signals

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SeleniumMiddleware:
    def __init__(self):
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')
        self.driver = webdriver.Chrome(options=options)

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
