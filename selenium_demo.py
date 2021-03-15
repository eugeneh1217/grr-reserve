import time
from selenium import webdriver
import os

CHROMEDRIVER_PATH = os.path.dirname(os.path.realpath(__file__)) + '/chromedrivers/chromedriver89.exe'

driver = webdriver.Chrome(CHROMEDRIVER_PATH)
driver.get('https://www.google.com/')
time.sleep(5)
search_box = driver.find_element_by_name('q')
search_box.send_keys('Chrome Driver')
search_box.submit()
time.sleep(5)
driver.quit()