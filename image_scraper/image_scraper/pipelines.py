import hashlib
import logging
import os

import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes

from image_scraper.kafka.producer import KafkaProducer

logger = logging.getLogger(__name__)


class URLImagesPipeline(ImagesPipeline):
    gcs_url_prefix = 'https://storage.googleapis.com'
    producer: KafkaProducer = None
    project_name = None
    spider_timestamp = None

    @classmethod
    def from_settings(cls, settings):
        logger.info("Setting up Kafka Producer ...")
        obj_from_settings = super().from_settings(settings)
        obj_from_settings.producer = KafkaProducer(bootstrap_servers=os.environ['KAFKA_LISTENER'], client_id='scrapyd')
        logger.info("Kafka Producer set up.")
        return obj_from_settings

    def get_media_requests(self, item, info):
        if self.project_name is None:
            self.project_name = info.spider.scraping_project
        if self.spider_timestamp is None:
            self.spider_timestamp = info.spider.job_timestamp
        for image_url in item["image_urls"]:  # handles field from Item
            yield scrapy.Request(image_url, meta={'dont_proxy': True})

    def item_completed(self, results, item, info):
        image_paths = [x["path"] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        adapter = ItemAdapter(item)
        logger.info(f"Sending GCS URL for {image_paths} ...")
        self.producer.produce_urls(topic=os.environ["MSG_TOPIC"],
                                   filenames=image_paths,
                                   scraping_project=self.project_name,
                                   prefix=self.gcs_url_prefix)
        logger.info("GCS URLs sent.")
        adapter["images"] = image_paths
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f"{self.project_name}/{self.spider_timestamp}/{image_guid}.jpg"
