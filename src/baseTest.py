from datetime import datetime
import os
import re
from string import join
import sys
import threading
import inspect
from random import randrange

import unittest2 as unittest
from yopenstackqe_tests import config
from yopenstackqe_tests.common import multiple_assertions
from yopenstackqe_tests.common.utils import yLogger
from yopenstackqe_tests.services.osNative import novaCommands

from selenium.webdriver.firefox.webdriver import WebDriver
# from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import ui as selenium_ui


logger = yLogger.setup_custom_logger(__name__)


class BaseCliTest(multiple_assertions.TestCaseWithMultipleAssertions):
    def __init__(self, *args, **kwargs):
        super(BaseCliTest, self).__init__(*args, **kwargs)

    def setUp(self):
        logger.debug("BASE:SETUP Override me in the test suite ")

    @classmethod
    def setUpClass(cls):
        cls.config = config.CliConfig()
        logger.debug("SetupCLass for BaseTest")
        # Since the same IP can get assigned to VMs, ensure that entries are
        # not written into ~/.ssh/known_hosts file
        threading.Semaphore().acquire()
        linePresent = False
        fH = None
        try:
            logger.info("Filename: " + str(cls.config.compute.ssh_config_filename))
            with open(cls.config.compute.ssh_config_filename) as fH:
                for line in fH:
                    if re.search('^#', line):
                        continue
                    if 'UserKnownHostsFile=/dev/null' in line:
                        linePresent = True
                        break
                if linePresent is not True:
                    raise IOError("Line not present")
        except IOError:
            if fH is not None:
                fH = open(cls.config.compute.ssh_config_filename, 'a+')
                fH.write('UserKnownHostsFile=/dev/null\n')
        finally:
            if fH is not None:
                fH.close()
        threading.Semaphore().release()
        Initialization()

    def log_assert(self, expected=0, actual=0, message=None):

        if expected == actual:
            logger.info("Pass: " + str(inspect.stack()[1][3]))
        elif message is not None and self.canSkipped(message):
                logger.warn("Skipping test for " + str(message))
        else:
            logger.error("Fail:" + str(inspect.stack()[1][3]) + " : " + str(message))

        assert expected == actual, message
        
    def tearDown(self):
        logger.info(">> BASE:TEARDOWN Override me in the test suite <<")
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
                logger.warn("Skipping test for " + str(failure))
                raise unittest.SkipTest(str(failure))

        return False

class SeleniumTestCase(BaseCliTest):

    @classmethod
    def setUpClass(cls):
        super(SeleniumTestCase, cls).setUpClass()
        os.environ["webdriver.chrome.driver"] = \
            config.BrowserConfig().browser.chromedriver_path

        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(5)

        #======= Bouncer login =========
        cls.selenium.get('https://by.bouncer.login.yahoo.com/')
        cls.selenium.find_element_by_name('id').send_keys(
            config.CliConfig().compute.username)
        cls.selenium.find_element_by_name('pass_word').send_keys(
            config.CliConfig().compute.password)
        cls.selenium.find_element_by_id('sbmt').submit()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTestCase, cls).tearDownClass()

    def setUp(self):
        self.ui = selenium_ui
        super(SeleniumTestCase, self).setUp()

    def tearDown(self):
        if sys.exc_info()[0]:
            filename = os.environ['LOG_DIR'] + '/screenshots/' + \
                       self._testMethodName + \
                       datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%ss')
            self.selenium.get_screenshot_as_file(filename)
            logger.error("Screenshot on failure saved: %s", filename)


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
        self.cleanUpAllExistingVMs()
        self.loadKnownFailures()
        if config.CliConfig().compute.minimum_image_list is not None:
            self.loadDefaultImage()

    @classmethod
    def cleanUpAllExistingVMs(cls):
        if os.environ['TEST_TYPE'] == "aria":
            novaCommands.NovaDeleteAllVMs(config.CliConfig().identity.aria_vm_name)
        else:
            novaCommands.NovaDeleteAllVMs()

    @classmethod
    def loadKnownFailures(cls):
        """Load data from known_failure File"""
        fH = None
        try:
            logger.info("Loading Known Failures from : " + str(config.CliConfig().common.known_failure_filename))
            if os.path.isfile(config.CliConfig().common.known_failure_filename):
                with open(config.CliConfig().common.known_failure_filename) as fH:
                    for line in fH:
                        if re.search('^#', line):
                            continue
                        config.CliConfig().knownFailureList.append(line)
                        logger.debug(line)
        finally:
            if fH is not None:
                fH.close()

    @classmethod
    def loadDefaultImage(cls):
        """Load a random image name when image ref is not defined"""
        if config.CliConfig().compute.image_ref is not None:
            logger.debug("Using the image defined in image_ref config " + config.CliConfig().compute.image_ref)
            config.CliConfig().defaultImage = config.CliConfig().compute.image_ref
            return

        logger.debug("Loading the default image from config file defined under minimum-image-list")

        minimum_image_list = config.CliConfig().compute.minimum_image_list.split(",")
        # Because we need to populate 2 images for all the tests

        # Handle the case when it has one 1 image in the list
        if minimum_image_list.__len__() == 1:
            config.CliConfig().defaultImage = minimum_image_list[0]
            logger.debug("Default Image is name = " + config.CliConfig().defaultImage)
            return

        index = randrange(0, minimum_image_list.__len__() - 1)
        config.CliConfig().defaultImage = minimum_image_list[index].strip()
        logger.debug("Default Image is name = " + config.CliConfig().defaultImage)

        if index == 0:
            config.CliConfig().defaultImageAlt = minimum_image_list[index + 1].strip()
        else:
            config.CliConfig().defaultImageAlt = minimum_image_list[index - 1].strip()

        logger.debug("Alternate Image is name = " + config.CliConfig().defaultImageAlt)