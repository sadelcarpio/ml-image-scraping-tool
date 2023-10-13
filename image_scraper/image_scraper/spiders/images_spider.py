import scrapy

from ..items import ImageItem


class GoogleImagesSpider(scrapy.Spider):
    name = "google_images_spider"
    start_urls = [
        "https://www.google.com/search?q=cats+images&tbm=isch",
    ]

    def parse(self, response, **kwargs):
        # Extract the image URLs from the Google Images page.
        # Scrape the image data.
        for image_url in response.css("img::attr(src)").getall():
            if image_url.startswith("https:"):
                yield ImageItem(image_urls=[image_url])

        next_page = response.xpath("//tbody/td/a/@href").get() or response.xpath(
            "//tbody/tr/td/a/span[text()='>']/parent::a/@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
