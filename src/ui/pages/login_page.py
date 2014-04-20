from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from src import config
from src.wait_utils import Waiter


class LoginPage(object):
    page_url = config.BrowserConfig().browser.horizon_url + '/auth/login/'
    username_input_id = "id_username"
    region_select_id = "id_region"
    sign_in_css = ".modal-footer button"
    username_css = "#user_info span"
    username_after_login_css = "#user_info>span"

    def __init__(self, driver):
        self.driver = driver
        self.waiter = Waiter(driver)

    def get(self):
        self.driver.get(self.page_url)

    def login(self, region=None):
        if not (self.driver.current_url == self.page_url):
            self.get()

        if region:
            select = Select(
                self.driver.find_element_by_id(self.region_select_id))
            select.select_by_visible_text(region)

        self.driver.find_element_by_css_selector(self.sign_in_css).click()

        self.waiter.wait_until_exist_by_css(self.username_css)

    def get_username_after_login(self):
        return self.driver.find_element_by_css_selector(
            self.username_after_login_css).text
