import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item["image_urls"]:  # handles field from Item
            yield scrapy.Request(image_url, meta={'dont_proxy': True})

    def item_completed(self, results, item, info):
        image_paths = [x["path"] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        adapter = ItemAdapter(item)
        adapter["images"] = image_paths
        return item
