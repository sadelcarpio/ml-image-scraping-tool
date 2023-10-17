import time

import scrapy
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from ..items import ImageItem


class GoogleImagesSpider(scrapy.Spider):
    name = "google_images_spider"
    start_urls = [
        "https://www.google.com/search?q=real+cats+images&tbm=isch&tbs=qdr:d%2Cisz:l",
    ]
    base_path = '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div'

    def parse(self, response, **kwargs):
        # Extract the image URLs from the Google Images page.
        # Scrape the image data.
        driver: WebDriver = response.meta['driver']
        images_per_load = len(response.xpath('//*[@id="islrg"]/div[1]/div/a[1]/div[1]/img').getall())
        for i in range(1, images_per_load + 1):
            driver.find_element(By.XPATH, f'//*[@id="islrg"]/div[1]/div[{i}]/a[1]/div[1]/img').click()
            # Could work but need to validate if image loaded completely (not pixelated)
            # img_element = WebDriverWait(driver, 10).until(
            #  expected_conditions.presence_of_element_located((By.XPATH, f'{self.base_path}/div[3]/div[1]/a/img[1]'))
            # )
            time.sleep(3)
            img_element = driver.find_element(By.XPATH, f'{self.base_path}/div[3]/div[1]/a/img[1]')
            img_src = img_element.get_attribute('src')
            if not img_src.startswith('data:image'):
                yield ImageItem(image_urls=[img_src])

        # TODO: Logic for handling infinite scrolling on results
        # next_page = response.xpath("//tbody/td/a/@href").get() or response.xpath(
        #     "//tbody/tr/td/a/span[text()='>']/parent::a/@href").get()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)
