import logging
import time
from datetime import datetime

import scrapy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from ..items import ImageItem

logger = logging.getLogger(__name__)


class GoogleImagesSpider(scrapy.Spider):
    name = "google_images_spider"
    # large images published on the last 24 hrs
    domain = "https://www.google.com/search?q="
    search_params = "&tbm=isch&tbs=qdr:d%2Cisz:l"
    base_path = '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div'

    def __init__(self, scraping_project, start_urls: str = "cats+images", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = None
        self.job_timestamp = datetime.now().strftime('%d-%m-%Y')
        self.scraping_project = scraping_project
        start_urls = start_urls.split(",")
        self.start_urls = [self.domain + start_url + self.search_params for start_url in start_urls]
        logger.info(f"Scraping the following URLs: {self.start_urls}")

    def parse(self, response, **kwargs):
        # Extract the image URLs from the Google Images page.
        # Scrape the image data.
        self.driver: WebDriver = response.meta['driver']
        time.sleep(5)
        initial_load = len(response.xpath('//*[@id="rso"]/div/div/div[1]/div/div/div/div[2]/h3/a/div/div/div/g-img/img').getall())
        additional_scrolls = 5
        for i in range(1, initial_load + additional_scrolls + 1):  # more scrolls than this throw unrelated images
            try:
                thumbnail_img = self.driver.find_element(By.XPATH, f'//*[@id="rso"]/div/div/div[1]/div/div/div[{i}]/div[2]/h3/a/div/div/div/g-img/img')
                self.driver.execute_script('arguments[0].click()', thumbnail_img)
            # TODO: encontrar el xpath actualizado para el nuevo scroll
            except NoSuchElementException:
                loaded_in_scroll = len(
                    self.driver.find_elements(By.XPATH, f'//*[@id="islrg"]/div[1]/div[{i}]/div/a[1]/div[1]/img'))
                if not loaded_in_scroll:
                    break
                for j in range(1, loaded_in_scroll + 1):
                    thumbnail_img = self.driver.find_element(By.XPATH,
                                                             f'//*[@id="islrg"]/div[1]/div[{i}]/div[{j}]/a[1]/div[1]/img')
                    self.driver.execute_script('arguments[0].click()', thumbnail_img)
                    yield from self.scrape_image_url()
            else:
                yield from self.scrape_image_url()
            finally:
                if i >= initial_load:
                    self.driver.execute_script("window.scrollBy(0, 1000);")
                    time.sleep(10)

    def scrape_image_url(self):
        time.sleep(5)  # waits for image to be HD
        img_element = self.driver.find_element(By.XPATH,
                                               f'{self.base_path}//a/img[1]')
        img_src = img_element.get_attribute('src')
        if not img_src.startswith('data:image'):
            yield ImageItem(image_urls=[img_src])
        self.driver.find_element(By.XPATH, f'{self.base_path}//div[1]/div/div[2]/div[2]/button').click()
