FROM mlist-scrapy-base:latest

RUN grep -v "scrapyd" requirements.txt | xargs pip install

ENTRYPOINT scrapy crawl google_images_spider