import time
from selenium import webdriver
import os

CHROMEDRIVER_PATH = os.path.dirname(os.path.realpath(__file__)) + '/chromedrivers/'

class Reserver:
    def __init__(self, version):
        self.driver = webdriver.Chrome(CHROMEDRIVER_PATH + f"/chromedriver{version}.exe")

    def open(self, url):
        self.driver.get(url)

    def close(self):
        self.driver.quit()

r = Reserver(89)
r.open('https://google.com')
time.sleep(3)
r.open('https://youtube.com')
