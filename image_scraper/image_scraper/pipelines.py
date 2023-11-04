import hashlib

import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes

from kafka.producer import KafkaProducer


class URLImagesPipeline(ImagesPipeline):

    gcs_url_prefix = 'https://storage.googleapis.com'
    producer: KafkaProducer = None

    @classmethod
    def from_settings(cls, settings):
        obj_from_settings = super().from_settings(settings)
        obj_from_settings.producer = KafkaProducer(bootstrap_servers='localhost:9092', client_id='scrapyd')
        return obj_from_settings

    def get_media_requests(self, item, info):
        for image_url in item["image_urls"]:  # handles field from Item
            yield scrapy.Request(image_url, meta={'dont_proxy': True})

    def item_completed(self, results, item, info):
        image_paths = [x["path"] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        adapter = ItemAdapter(item)
        self.producer.produce_urls(topic='google-images', filenames=image_paths, prefix=self.gcs_url_prefix)
        adapter["images"] = image_paths
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f"{image_guid}.jpg"
