# Scrapy settings for image_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os

BOT_NAME = "image_scraper"

SPIDER_MODULES = ["image_scraper.spiders"]
NEWSPIDER_MODULE = "image_scraper.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Image Pipeline
ITEM_PIPELINES = {"image_scraper.pipelines.URLImagesPipeline": 300}
IMAGES_URLS_FIELD = "image_urls"
IMAGES_RESULT_FIELD = "images"
IMAGES_EXPIRES = 30

# Google cloud storage params
GCS_FOLDER_PATH = f"{os.environ['IMAGES_BUCKET_NAME']}"
IMAGES_STORE = f"gs://{GCS_FOLDER_PATH}/"
GCS_PROJECT_ID = os.environ["PROJECT_ID"]

# Selenium
DOWNLOADER_MIDDLEWARES = {
    'image_scraper.middlewares.SeleniumMiddleware': 300
}

LOG_LEVEL = "INFO"
