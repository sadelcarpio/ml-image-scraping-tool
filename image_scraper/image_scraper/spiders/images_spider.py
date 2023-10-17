import time

import scrapy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from ..items import ImageItem


class GoogleImagesSpider(scrapy.Spider):
    name = "google_images_spider"
    # large images published on the last 24 hrs
    start_urls = [
        "https://www.google.com/search?q=cats+images&tbm=isch&tbs=qdr:d%2Cisz:l",
    ]
    base_path = '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div'

    def parse(self, response, **kwargs):
        # Extract the image URLs from the Google Images page.
        # Scrape the image data.
        driver: WebDriver = response.meta['driver']
        time.sleep(3)
        initial_load = len(response.xpath('//*[@id="islrg"]/div[1]/div/a[1]/div[1]/img').getall())
        additional_scrolls = 3
        for i in range(1, initial_load + additional_scrolls + 1):  # more scrolls than this throw unrelated images
            try:
                thumbnail_img = driver.find_element(By.XPATH, f'//*[@id="islrg"]/div[1]/div[{i}]/a[1]/div[1]/img')
                driver.execute_script('arguments[0].click()', thumbnail_img)
            except NoSuchElementException:
                loaded_in_scroll = len(
                    driver.find_elements(By.XPATH, f'//*[@id="islrg"]/div[1]/div[{i}]/div/a[1]/div[1]/img'))
                if not loaded_in_scroll:
                    break
                for j in range(1, loaded_in_scroll + 1):
                    thumbnail_img = driver.find_element(By.XPATH,
                                                        f'//*[@id="islrg"]/div[1]/div[{i}]/div[{j}]/a[1]/div[1]/img')
                    driver.execute_script('arguments[0].click()', thumbnail_img)
                    # TODO: Add logic to guarantee clicked image is on full size and not loading
                    time.sleep(3)  # waits for image to be HD
                    img_element = driver.find_element(By.XPATH,
                                                      f'{self.base_path}//a/img[1]')
                    # img_element = WebDriverWait(driver, 10).until(
                    #     expected_conditions.element_to_be_clickable((By.XPATH, f'{self.base_path}//a/img[1]')))
                    img_src = img_element.get_attribute('src')
                    if not img_src.startswith('data:image'):
                        yield ImageItem(image_urls=[img_src])
                    driver.find_element(By.XPATH, f'{self.base_path}//div[1]/div/div[2]/div[3]/button').click()
            else:
                time.sleep(3)
                img_element = driver.find_element(By.XPATH,
                                                  f'{self.base_path}//a/img[1]')
                # img_element = WebDriverWait(driver, 10).until(
                #     expected_conditions.element_to_be_clickable((By.XPATH, f'{self.base_path}//a/img[1]')))
                img_src = img_element.get_attribute('src')
                if not img_src.startswith('data:image'):
                    yield ImageItem(image_urls=[img_src])
                driver.find_element(By.XPATH, f'{self.base_path}//div[1]/div/div[2]/div[3]/button').click()
            finally:
                if i >= initial_load:
                    driver.execute_script("window.scrollBy(0, 1000);")
                    time.sleep(10)
