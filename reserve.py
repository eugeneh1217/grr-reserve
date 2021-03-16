import time
from selenium import webdriver
import os

CHROMEDRIVER_PATH = os.path.dirname(os.path.realpath(__file__)) + '/chromedrivers/'
GRR_RESERVE_BASE = 'https://grandriverrocks.com/waterloo/reservations/'
SECTIONS = {
    'front': 'zone1wat/',
    'back': 'zone2wat/',
    'train': 'zone3wat/'
}

ZONE_PAGE_IDS = {
    'calendar': 'start_date_calendar',
    'form': 'theform'
}

ZONE_PAGE_PATHS = {
    'participants_increment': f"//form[@id=\"{ZONE_PAGE_IDS['form']}\"]/div[6]/fieldset[2]/table[1]/tbody/tr[1]/td/a[2]",
    'calendar_table': f"//div[@id='{ZONE_PAGE_IDS['calendar']}]'/div[1]/table[1]"
}

CALENDAR_ID = 'start_date_calendar'
FORM_ID = 'theform'


class Reserver:
    def __init__(self, version):
        self.driver = webdriver.Chrome(CHROMEDRIVER_PATH + f"/chromedriver{version}.exe")

    def open(self, url):
        self.driver.get(url)

    def close(self):
        self.driver.quit()

    def increment_participants(self):
        r.switch_to_iframe_by_index(0)
        time.sleep(2)
        form = r.get_element(xpath="//form[@id='theform']/div[6]/div[1]/fieldset[1]/table[1]/tbody[1]/tr[1]/td[1]/a[2]")
        form.click()

    def book(self, section):
        self.open(GRR_RESERVE_BASE + SECTIONS[section])
        self.increment_participants()
        # time.sleep(2)

    def get_element(self, xpath=None, element_id=None):
        if xpath:
            return self.driver.find_element_by_xpath(xpath)
        if element_id:
            return self.driver.find_element_by_id(element_id)

r = Reserver(89)
r.book('front')
r.close()
