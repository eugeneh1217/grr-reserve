import time
import os

from selenium import webdriver

CHROMEDRIVER_PATH = os.path.dirname(os.path.realpath(__file__)) + '/chromedrivers/'
GRR_RESERVE_BASE = 'https://grandriverrocks.com/waterloo/reservations/'
SECTIONS = {
    'front': 'zone1wat/',
    'back': 'zone2wat/',
    'train': 'zone3wat/'
}

CALENDAR_ID = 'start_date_calendar'
FORM_ID = 'theform'

ZONE_PAGE_IDS = {
    'calendar': 'start_date_calendar',
    'form': 'theform',
    'event_table': 'offering-page-select-events-table'
}

ZONE_PAGE_PATHS = {
    'participants_increment': f"//form[@id='{ZONE_PAGE_IDS['form']}']/"
    "div[6]/div[1]/fieldset[1]/table[1]/tbody[1]/tr[1]/td[1]/a[2]",
    'calendar_table': f"//div[@id='{ZONE_PAGE_IDS['calendar']}']/div[1]/table[1]/tbody[1]"
}

LOAD_PAUSE = 2

class Reserver:
    def __init__(self, version):
        self.driver = webdriver.Chrome(CHROMEDRIVER_PATH + f"/chromedriver{version}.exe")

    def open(self, url):
        self.driver.get(url)

    def close(self):
        self.driver.quit()

    def get_element(self, xpath=None, element_id=None):
        if xpath:
            return self.driver.find_element_by_xpath(xpath)
        if element_id:
            return self.driver.find_element_by_id(element_id)
        return None

    def increment_participants(self):
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))
        time.sleep(LOAD_PAUSE)
        form = self.get_element(xpath=ZONE_PAGE_PATHS['participants_increment'])
        form.click()
        self.driver.switch_to.default_content()
    
    def select_day(self, day):
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))
        time.sleep(LOAD_PAUSE)
        calendar = self.get_element(xpath=ZONE_PAGE_PATHS['calendar_table'])
        try:
            for table_row in calendar.find_elements_by_tag_name('tr'):
                for table_data in table_row.find_elements_by_tag_name('td'):
                    try:
                        if int(table_data.text) == day:
                            table_data.find_element_by_tag_name('a').click()
                    except ValueError:
                        continue
        except:
            pass
        self.driver.switch_to.default_content()
        time.sleep(LOAD_PAUSE)

    def select_event(self, start_time):
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))
        try:
            event_table = self.get_element(element_id=ZONE_PAGE_IDS['event_table']).find_element_by_xpath('tbody[1]')
            print(len(event_table))
            for table_row in event_table.find_elements_by_tag_name('tr'):
                print(table_row.text + 'new row')
                if start_time in table_row.text and 'spaces' in table_row.text:
                    print(f"clicked {table_row.find_element_by_xpath('td[4]/a[1]').get_attribute('class')}")
                    table_row.find_element_by_xpath('td[4]/a[1]').click()
                else:
                    print(table_row.text)
        except:
            pass
        self.driver.switch_to.default_content()
        time.sleep(LOAD_PAUSE)

    def sign_in(self, username, password):


    def select_slot(self, section, day):
        self.increment_participants()
        self.select_day(day)
        self.select_event('10 AM')

    def book(self, section, day):
        self.open(GRR_RESERVE_BASE + SECTIONS[section])
        self.select_slot(section, day)
        time.sleep(5)

r = Reserver(89)
r.book('front', 19)
# time.sleep(60)
r.close()
