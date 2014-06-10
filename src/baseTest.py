from datetime import datetime
import inspect
import os
import re
import random

from requests.exceptions import InvalidSchema, MissingSchema, ConnectionError
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui as selenium_ui
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import src.constants as constants
from src import multiple_assertions
from src import clogger
from src import config
from src.page_helpers import utils


logger = clogger.setup_custom_logger(__name__)


class BaseCliTest(multiple_assertions.TestCaseWithMultipleAssertions):
    def __init__(self, *args, **kwargs):
        super(BaseCliTest, self).__init__(*args, **kwargs)

    def setUp(self):
        logger.debug("BASE:SETUP Override me in the tests suite ")

    @classmethod
    def setUpClass(cls):
        cls.config = config.CliConfig()
        logger.debug("SetupCLass for BaseTest")
        Initialization()

    def get_test_method_name(self):
        """
        Return the test method name from the caller stack
        :rtype : method Name to return from caller stack
        """
        for element in inspect.stack():
            if element[3].find('test_') == 0:
                return str(element[3])

        return "test_method_name_not_found"


    def tearDown(self):
        logger.info(">> BASE:TEARDOWN Override me in the tests suite <<")
        pass

    @classmethod
    def tearDownClass(cls):
        logger.info("BASE:tearDownClass:Called once for each class instance. Can be overridden")
        pass


class SeleniumTestCase(BaseCliTest):
    @classmethod
    def setUpClass(cls):
        super(SeleniumTestCase, cls).setUpClass()

        hub_url = config.CliConfig().common.selenium_hub_url or "http://localhost:" + os.environ.get("PORT") + "/wd/hub"

        if os.environ.get("BROWSER", "firefox") == "firefox":
            cls.browser = webdriver.Remote(hub_url, DesiredCapabilities.FIREFOX)
        elif os.environ.get("BROWSER", "firefox") == "chrome":
            cls.browser = webdriver.Remote(hub_url, DesiredCapabilities.CHROME)
        elif os.environ.get("BROWSER", "firefox") == "safari":
            cls.browser = webdriver.Remote(hub_url, DesiredCapabilities.SAFARI)

        cls.browser.implicitly_wait(5)

    def is_url_broken(self, link=""):
        """
            Checks if the URL supplied or current page is broken mean oops page or not

            :Args:
             - link = Optional Value: if not passed then current page is used to test

            :Usage:
                utils.is_url_broken(self.browser)
        """
        try:
            # Navigate to the link if it is not there already
            if link != self.browser.current_url and link != "":
                self.browser.get(link)
            #Needs to login instead any of the link redirect us to login page
            if "login" in self.browser.current_url and self.browser.find_elements_by_id('email').__len__() > 0:
                utils.login(browser=self.browser)

            element = self.browser.find_elements_by_xpath(
                '//*[contains(text(),"Well, this is embarrassing - you found a broken link.")]').__len__()
            return element
        except (InvalidSchema, MissingSchema, ConnectionError):
            logger.error("Hit an exception while traversing the URL")
            return True

    def capture_screenshot(self):
        """
            Common routine to capture the screen shot and save it in log/screenshots folder
            file_name can either be testname or element name depending upon the caller
            In both cases the filename will be appended by timestamp to make it unique

            :Args:
             :Usage:
              - self.capture_screenshot()
        """
        filename = os.environ.get('LOG_DIR', '../../logs') + "/screenshots/" + \
                   self.get_test_method_name() + \
                   datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%ss') + ".png"
        self.browser.save_screenshot(filename)
        logger.error("Screen shot on failure saved: %s with URL %s" % (filename, self.browser.current_url))


    def get_web_element(self, by=By.XPATH, value=None):
        """
            Locate an element on page by its attribute.
            If element is found return that element else raise an assertion exception

            :Args:
             - by = Optional Value: value to search the element by
             - value = element string to search for items

            :Usage:
                self.get_web_element(by=By.XPATH, value="//div[contains(@class, 'foo')]")
        """
        #Catching the exception if element is not found
        try:
            return self.browser.find_element(by=by, value=value)
        except NoSuchElementException:
            logger.error("Not able to find the web element by %s having value : %s" % (by, value))
            self.capture_screenshot()
            raise AssertionError(("Not able to find the web element by %s having value : %s" % (by, value)))


    def find_element_and_click(self, by=By.XPATH, value=None):
        """
            Locate an element on page by its attribute.
            If element is found click on it and verify that it does not result in 404 - page not found

            :Args:
             - by = Optional Value: value to search the element by
             - value = element string to search for items

            :Usage:
                self.find_element_and_click(by=By.XPATH, value="//div[contains(@class, 'foo')]")
        """
        #Catching the exception if element is not found
        try:
            self.browser.find_element(by=by, value=value).click()
            return self.is_url_broken()
        except NoSuchElementException:
            logger.error("Not able to find the web element by %s having value : %s" % (by, value))
            self.capture_screenshot()
            raise AssertionError(("Not able to find the web element by %s having value : %s" % (by, value)))


    def find_element_and_submit(self, by=By.XPATH, value=None):
        """
            Locate an element on page by its attribute.
            If element is found submit on it and verify that it does not result in 404 - page not found

            :Args:
             - by = Optional Value: value to search the element by
             - value = element string to search for items

            :Usage:
                self.find_element_and_click(by=By.XPATH, value="//div[contains(@class, 'foo')]")
        """
        #Catching the exception if element is not found
        try:
            self.browser.find_element(by=by, value=value).submit()
            return self.is_url_broken()
        except NoSuchElementException:
            logger.error("Not able to find the web element by %s having value : %s" % (by, value))
            self.capture_screenshot()
            raise AssertionError(("Not able to find the web element by %s having value : %s" % (by, value)))


    def click(self, web_element=None):
        """
            Performs an click action on the element and verify it does not result in 404 - page not found
            :Args:
             - browser = Current instance of browser to use to login
             - web_element = Web Element to be clicked

            :Usage:
                self.click(web_element)
        """
        #Catching the exception if element is not found
        try:
            web_element.click()
            return self.is_url_broken()
        except NoSuchElementException:
            logger.error("Not able to find the web element to click ")
            self.capture_screenshot()
            raise AssertionError(("Not able to find the web element to click"))


    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(SeleniumTestCase, cls).tearDownClass()

    def setUp(self):
        self.ui = selenium_ui
        super(SeleniumTestCase, self).setUp()

    def tearDown(self):
        pass


class CrittercismTestCase(SeleniumTestCase):
    @classmethod
    def setUpClass(cls):
        super(CrittercismTestCase, cls).setUpClass()
        #======= login to portal =========
        cls.browser.get(config.CliConfig().common.url + "/developers/login")
        cls.browser.find_element_by_id('email').clear()
        cls.browser.find_element_by_id('email').send_keys(config.CliConfig().login.username)
        cls.browser.find_element_by_name('password').send_keys(config.CliConfig().login.password)
        cls.browser.find_element_by_id('commit').submit()

    def setUp(self):
        super(CrittercismTestCase, self).setUp()

    def logout(self):
        self.browser.get(self.config.common.url + "/developers/logout")

    def sign_up_new_account(self, plan_type="basic"):
        self.logout()
        # self.browser.implicitly_wait(3)
        self.browser.get(self.config.common.url + "/signup?plan=" + plan_type)
        random_email = (self.config.login.test_user_engg).replace('@', str(random.random()) + '@')
        self.browser.find_element_by_id("firstname").send_keys("test_user_" + plan_type)
        self.browser.find_element_by_id("lastname").send_keys("crittercism")
        self.browser.find_element_by_id("company").send_keys("crittercism")
        self.browser.find_element_by_id("phone").send_keys("123-456-7890")
        self.browser.find_element_by_id("email").send_keys(random_email)
        self.browser.find_element_by_id("password").send_keys(self.config.login.password)
        self.find_element_and_submit(by=By.XPATH, value="//*[contains(@class,'grid_8 push_2')]")

    def create_new_app(self, platform=None):
        page_url = self.config.common.url + "/developers/register-application"
        self.browser.get(page_url)

        p_str = platform.PREFIX
        self.find_element_and_click(value='//label[@for=' + platform.PLATFORM + ']')
        app_name = p_str + str(random.random())
        self.browser.find_element_by_id("app-name").send_keys(app_name)
        self.assertFalse(self.find_element_and_submit(by=By.ID, value=constants.BrowserConstants.COMMIT),
                         " Broken link at " + self.browser.current_url)
        return app_name

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        super(CrittercismTestCase, cls).tearDownClass()


def Singleton(self):
    """Simple wrapper for classes that should only have a single instance"""
    instances = {}

    def getinstance():
        if self not in instances:
            instances[self] = self()
        return instances[self]

    return getinstance


@Singleton
class Initialization:
    def __init__(self):
        self.cleanUpAllExistingMess()
        self.loadKnownBugs()

    @classmethod
    def cleanUpAllExistingMess(cls):
        pass

    @classmethod
    def loadKnownBugs(cls):
        """Load data from known_failure File"""
        fH = None
        try:
            logger.info("Loading Known Failures from : " + str(config.CliConfig().common.known_bugs_filename))
            if os.path.isfile(config.CliConfig().common.known_bugs_filename):
                with open(config.CliConfig().common.known_bugs_filename) as fH:
                    for line in fH:
                        if re.search('^#', line):
                            continue
                        config.CliConfig().knownFailureList.append(line)
                        logger.debug(line)
        finally:
            if fH is not None:
                fH.close()