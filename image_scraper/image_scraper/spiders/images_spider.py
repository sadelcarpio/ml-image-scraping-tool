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
        "https://www.google.com/search?q=real+cats+images&tbm=isch&tbs=qdr:d%2Cisz:l",
    ]
    base_path = '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div'

    def parse(self, response, **kwargs):
        # Extract the image URLs from the Google Images page.
        # Scrape the image data.
        driver: WebDriver = response.meta['driver']
        time.sleep(3)
        initial_load = len(response.xpath('//*[@id="islrg"]/div[1]/div/a[1]/div[1]/img').getall())
        i = 1
        while True:
            try:
                thumbnail_img = driver.find_element(By.XPATH, f'//*[@id="islrg"]/div[1]/div[{i}]/a[1]/div[1]/img')
                driver.execute_script('arguments[0].click()', thumbnail_img)
            except NoSuchElementException:
                break
            time.sleep(0.1)
            img_element = driver.find_element(By.XPATH, f'{self.base_path}//a/img[1]')
            img_src = img_element.get_attribute('src')
            if not img_src.startswith('data:image'):
                yield ImageItem(image_urls=[img_src])
            driver.find_element(By.XPATH, f'{self.base_path}//div[1]/div/div[2]/div[3]/button').click()
            i += 1
            if i % initial_load == 0:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
        self.parse_scrolled(response, i)

    def parse_scrolled(self, response, i):
        driver = response.meta['driver']
        initial_load = len(response.xpath(f'//*[@id="islrg"]/div[1]/div[{i}]/div/a[1]/div[1]/img').getall())
        j = 1
        while True:
            try:
                driver.find_element(By.XPATH, f'//*[@id="islrg"]/div[1]/div[{i}]/div[{j}]/a[1]/div[1]/img').click()
            except NoSuchElementException:
                self.parse_scrolled(response, i + 1)
            time.sleep(3)
            img_element = driver.find_element(By.XPATH, f'{self.base_path}//a/img[1]')
            img_src = img_element.get_attribute('src')
            if not img_src.startswith('data:image'):
                yield ImageItem(image_urls=[img_src])
            driver.find_element(By.XPATH, f'{self.base_path}//div[1]/div/div[2]/div[3]/button').click()
            if i % (initial_load - 1) == 0:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)

# before scrolling
# //*[@id="islrg"]/div[1]/div[47]/a[1]/div[1]/img
# //*[@id="islrg"]/div[1]/div[48]/a[1]/div[1]/img
# //*[@id="islrg"]/div[1]/div[37]/a[1]/div[1]/img
# //*[@id="islrg"]/div[1]/div[46]/a[1]/div[1]/img
# //*[@id="islrg"]/div[1]/div[49]/a[1]/div[1]/img
# after scrolling (increases an extra div)
# //*[@id="islrg"]/div[1]/div[51]/div[1]/a[1]/div[1]/img
# //*[@id="islrg"]/div[1]/div[51]/div[2]/a[1]/div[1]/img
# //*[@id="islrg"]/div[1]/div[51]/div[3]/a[1]/div[1]/img
# //*[@id="islrg"]/div[1]/div[51]/div[4]/a[1]/div[1]/img
# //*[@id="islrg"]/div[1]/div[51]/div[13]/a[1]/div[1]/img
# //*[@id="islrg"]/div[1]/div[51]/div[24]/a[1]/div[1]/img
# //*[@id="islrg"]/div[1]/div[51]/div[38]/a[1]/div[1]/img
# //*[@id="islrg"]/div[1]/div[51]/div[54]/a[1]/div[1]/img
# //*[@id="islrg"]/div[1]/div[52]/div[3]/a[1]/div[1]/img
# //*[@id="islrg"]/div[1]/div[52]/div[70]/a[1]/div[1]/img
# //*[@id="islrg"]/div[1]/div[53]/div[18]/a[1]/div[1]/img
