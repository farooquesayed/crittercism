import os
import re
from string import join
import inspect
#from selenium.webdriver.remote import webdriver

from selenium import webdriver

import unittest2 as unittest
from selenium.webdriver.support import ui as selenium_ui

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from src import  multiple_assertions
from src import clogger
from src import config


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

    def log_assert(self, expected=0, actual=0, message=None):

        if expected == actual:
            logger.info("Pass: " + str(inspect.stack()[1][3]))
        elif message is not None and self.canSkipped(message):
                logger.warn("Skipping tests for " + str(message))
        else:
            logger.error("Fail:" + str(inspect.stack()[1][3]) + " : " + str(message))

        assert expected == actual, message

    def tearDown(self):
        logger.info(">> BASE:TEARDOWN Override me in the tests suite <<")
        pass

    @classmethod
    def tearDownClass(cls):
        logger.info("BASE:tearDownClass:Called once for each class instance. \
                      Can be overridden")
        pass

    def canSkipped(self, message):
        for failure in config.CliConfig().knownFailureList:
            msg = failure.split('|')
            logger.debug("Splitting " + str(msg.__len__()) + " " + join(msg))
            if msg[1].strip() in message:
                logger.warn("Skipping tests for " + str(failure))
                raise unittest.SkipTest(str(failure))

        return False

class SeleniumTestCase(BaseCliTest):

    @classmethod
    def setUpClass(cls):
        super(SeleniumTestCase, cls).setUpClass()

        if os.environ.get("BROWSER", "chrome") == "firefox":
            cls.browser = webdriver.Remote(config.CliConfig().common.selenium_hub_url, DesiredCapabilities.FIREFOX)
        elif os.environ.get("BROWSER", "chrome") == "chrome":
            cls.browser = webdriver.Remote(config.CliConfig().common.selenium_hub_url, DesiredCapabilities.CHROME)
        elif os.environ.get("BROWSER", "chrome") == "safari":
            cls.browser = webdriver.Remote(config.CliConfig().common.selenium_hub_url, DesiredCapabilities.SAFARI)

        cls.browser.implicitly_wait(5)

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
        cls.browser.find_element_by_id('email').send_keys(config.CliConfig().login.username)
        cls.browser.find_element_by_name('password').send_keys(config.CliConfig().login.password)
        cls.browser.find_element_by_id('commit').submit()


    @classmethod
    def tearDownClass(cls):
        super(CrittercismTestCase, cls).tearDownClass()

    def setUp(self):
        super(CrittercismTestCase, self).setUp()

    def tearDown(self):
        pass


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

