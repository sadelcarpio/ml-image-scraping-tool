import unittest


class Spider:
    def crawl(self):
        return "Crawling..."

    def stop(self):
        return "Stopped."


class SpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = Spider()

    def test_crawl(self):
        self.assertEqual(self.spider.crawl(), "Crawling...")

    def test_stop(self):
        self.assertEqual(self.spider.stop(), "Stopped.")
