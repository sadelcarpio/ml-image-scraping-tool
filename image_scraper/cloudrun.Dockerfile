FROM mlist-scrapy-base:latest

RUN pip uninstall -y scrapyd scrapyd-client

ENTRYPOINT scrapy crawl google_images_spider