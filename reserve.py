import time
import os
from credentials import accounts

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By

CHROMEDRIVER_PATH = os.path.dirname(os.path.realpath(__file__)) + '/chromedrivers/'
GRR_RESERVE_BASE = 'https://grandriverrocks.com/waterloo/reservations/'
SECTIONS = {
    'front': 'zone1wat/',
    'back': 'zone2wat/',
    'train': 'zone3wat/'
}

CALENDAR_ID = 'start_date_calendar'

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
        except StaleElementReferenceException:
            pass
        self.driver.switch_to.default_content()
        time.sleep(LOAD_PAUSE)

    def select_event(self, start_time):
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))
        try:
            event_table = self.get_element(element_id=ZONE_PAGE_IDS['event_table']).find_element_by_xpath('tbody[1]')
            for table_row in event_table.find_elements_by_tag_name('tr'):
                if start_time in table_row.text and 'space' in table_row.text:
                    table_row.find_element_by_xpath('td[4]/a[1]').click()
                    break
        except StaleElementReferenceException:
            pass
        self.driver.switch_to.default_content()
        time.sleep(LOAD_PAUSE)

    def select_slot(self, section, day, start_time):
        self.select_day(day)
        self.increment_participants()
        self.select_event(start_time)

    def open_login(self):
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))
        self.driver.find_element_by_link_text('Log In or Create Profile').click()
        self.driver.switch_to.default_content()
        time.sleep(LOAD_PAUSE)

    def login(self, email, name, password):
        self.driver.switch_to.frame(self.driver.find_element_by_id('rgp00-embedded-modal-frame'))
        self.driver.find_element_by_name('email').send_keys(email)
        self.driver.find_element_by_name('password').send_keys(password)
        self.driver.find_element_by_link_text('Log In').click()
        time.sleep(LOAD_PAUSE)
        self.driver.find_element_by_link_text('Done').click()
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))
        time.sleep(LOAD_PAUSE)
        self.driver.find_elements_by_link_text(name)[1].click()
        time.sleep(LOAD_PAUSE)
        form = self.driver.find_element_by_id(ZONE_PAGE_IDS['form'])
        form.find_element_by_id('pfirstname-pindex-1-1').click()
        form.find_element_by_id('plastname-pindex-1-1').click()
        self.driver.switch_to.default_content()

    def fill_form(self):
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))
        form = self.driver.find_element_by_id(ZONE_PAGE_IDS['form'])
        select_payment = form.find_element_by_xpath('fieldset[2]/div[2]/select[1]')
        for payment_option in select_payment.find_elements_by_tag_name('option'):
            if 'Membership' in payment_option.text:
                payment_option.click()
        form.find_element_by_xpath('fieldset[3]/div[2]/span[1]/input[1]').click()
        form.find_element_by_xpath('fieldset[4]/div[2]/select[1]/option[2]').click()
        form.find_element_by_xpath('fieldset[5]/div[2]/select[1]/option[2]').click()
        form.find_element_by_xpath('fieldset[6]/div[2]/select[1]/option[2]').click()
        form.find_element_by_partial_link_text('CONTINUE').click()
        self.driver.switch_to.default_content()

    def sign_in(self, email, name, password):
        self.open_login()
        self.login(email, name, password)
        self.fill_form()

    def book(self, section, day, start_time, email):
        try:
            self.open(GRR_RESERVE_BASE + SECTIONS[section])
            self.select_slot(section, day, start_time)
            self.sign_in(email, accounts[email].first_name, accounts[email].password)
            time.sleep(LOAD_PAUSE)
        except NoSuchElementException:
            print("NO SPACES AVAILABLE!")

def main():
    r = Reserver(89)
    r.book('front', 21, '10 AM', 'eugeneh1217@gmail.com')
    r.close()

if __name__ == '__main__':
    main()