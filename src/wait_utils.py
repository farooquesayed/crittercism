from selenium.webdriver.support import ui

from src.common_utils import wait_for_event


class Waiter(object):

    def __init__(self, driver, timeout = 30, pool_period = 2):
        self.driver = driver
        self.timeout = timeout
        self.pool_period = pool_period
        self.wait = ui.WebDriverWait(driver, timeout, pool_period)


    def wait_until_exist_by_id(self, id, timeout=None, pool_period=None):
        self.wait_until_exist_by_css('#' + id, timeout, pool_period)

    def wait_until_exist_by_css(self, css, timeout=None, pool_period=None):
        if timeout:
            self.wait._timeout = timeout
        if pool_period:
            self.wait._poll = pool_period

        def element_exists(driver):
            return len(driver.find_elements_by_css_selector(css)) > 0

        self.wait.until(element_exists)

        if timeout:
            self.wait._timeout = self.timeout
        if pool_period:
            self.wait._poll = self.pool_period

    def wait_until_not_exist_by_id(self, id, timeout=None, pool_period=None):
        self.wait_until_not_exist_by_css('#' + id, timeout, pool_period)

    def wait_until_not_exist_by_css(self, css, timeout=None, pool_period=None):
        if timeout:
            self.wait._timeout = timeout
        if pool_period:
            self.wait._poll = pool_period

        def element_exists(driver):
            return len(driver.find_elements_by_css_selector(css)) > 0

        self.wait.until_not(element_exists)

        if timeout:
            self.wait._timeout = self.timeout
        if pool_period:
            self.wait._poll = self.pool_period

    def wait_until_visible_by_id(self, id, timeout=None, pool_period=None):
        self.wait_until_visible_by_css('#' + id, timeout, pool_period)

    def wait_until_visible_by_css(self, css, timeout=None, pool_period=None):
        if timeout:
            self.wait._timeout = timeout
        if pool_period:
            self.wait._poll = pool_period

        def element_visible(driver):
            return driver.find_element_by_css_selector(css).is_displayed()

        self.wait.until(element_visible)

        if timeout:
            self.wait._timeout = self.timeout
        if pool_period:
            self.wait._poll = self.pool_period

    def wait_until_not_visible_by_css(
            self, css, timeout=None, pool_period=None):
        if timeout:
            self.wait._timeout = timeout
        if pool_period:
            self.wait._poll = pool_period

        def element_visible(driver):
            return driver.find_element_by_css_selector(css).is_displayed()

        self.wait.until_not(element_visible)

        if timeout:
            self.wait._timeout = self.timeout
        if pool_period:
            self.wait._poll = self.pool_period

    def wait_until_page_changed(self, current_url):
        wait_for_event(self.timeout, self.pool_period,
                       "Instances page hasn't appeared",
                       lambda : self.driver.current_url != current_url)


