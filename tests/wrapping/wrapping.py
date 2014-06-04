import random
import unittest

from selenium.webdriver.common.by import By

import nose.plugins.attrib

from src import clogger
from src import config
from src import baseTest
from src.constants import BrowserConstants
from src.page_helpers import team

__author__ = 'egeller'

logger = clogger.setup_custom_logger(__name__)

def generate_list_of_crash_types():
    """



    :rtype : object
    :return:
    """
    crash_types = []
    crash_types.append("all")
    crash_types.append("resolved")
    crash_types.append("known")
    crash_types.append("unresolved")
    return crash_types

def generate_account_types():
    account_types = []
    account_types.append("basic")
    account_types.append("pro")
    account_types.append("ent")
    account_types.append("pro_plus")
    return account_types

def generate_platform_types():
    platform_types= []
    platform_types.append("IOS")
    return platform_types

class WrappingTestSuite(baseTest.CrittercismTestCase):

    @classmethod
    def setUpClass(cls):
        """


        """
        super(WrappingTestSuite, cls).setUpClass()


    def setUp(self):
        """
        Setup for the testcase


        """
        pass

    def sign_up_new_account(self, accnt):
        account_types = generate_account_types()
        self.browser.get(config.CliConfig().common.url + "/developers/logout")
        self.browser.implicitly_wait(3)
        self.browser.get(config.CliConfig().common.url + "/signup?plan=" + account_types[accnt])
        random_email = (self.config.login.test_user_engg).replace('@', str(random.random()) + '@')
        self.browser.find_element_by_id("firstname").send_keys("test_user_" + account_types[accnt])
        self.browser.find_element_by_id("lastname").send_keys("crittercism")
        self.browser.find_element_by_id("company").send_keys("crittercism")
        self.browser.find_element_by_id("phone").send_keys("123-456-7890")
        self.browser.find_element_by_id("email").send_keys(random_email)
        self.browser.find_element_by_id("password").send_keys(self.config.login.password)
        self.find_element_and_submit(by=By.XPATH, value="//*[contains(@class,'grid_8 push_2')]")

    def create_new_app(self, platform):
        # platform:
        #  0 = "IOS-", IOS
        #  1 = "ANDRD-", Android
        #  2 = "HTML-", HTML5
        #  3 = "WIN-", Windows 8
        page_url = config.CliConfig().common.url + "/developers/register-application"
        self.browser.get(page_url)


        if platform == 0:
            p_str = "IOS-"
        elif platform == 1:
            p_str = "ANDRD-"
            self.find_element_and_click(value='//label[@for="platform-android"]')
            self.find_element_and_click(value='//label[@for="platform-android"]')
        elif platform == 2:
            p_str = "HTML-"
            self.find_element_and_click(value='//label[@for="platform-html5"]')
        elif platform == 3:
            self.find_element_and_click(value='//label[@for="platform-wp"]')
        else:
            p_str = "IOS-"

        app_name = p_str + str(random.random())
        self.browser.find_element_by_id("app-name").send_keys(app_name)
        self.assertFalse(self.find_element_and_submit(by=By.ID, value=BrowserConstants.COMMIT),
                         " Broken link at " + self.browser.current_url)
        return app_name


    ############ENTERPRISE LEVEL#############
    @nose.plugins.attrib.attr(genre="wrapping")
    def test_ent_new_ios(self):
        """
            1)log into enterprise account, generate a new iOS application, load wrapping page
        """

        app_name = self.create_new_app(0)

        app_ids = team.get_id_from_app_name(self.browser, app_name)
        self.browser.get(self.config.common.url + "/developers/wrapping/" + app_ids[0])
        self.browser.implicitly_wait(2)
        self.assertEqual(self.browser.current_url, "https://app-staging.crittercism.com/developers/wrapping/" + app_ids[0],
                         "Expected wrapping page, and instead got %s" % self.browser.current_url)
        team.delete_app_given_ids(browser=self.browser, app_ids=self.app_ids)

    @nose.plugins.attrib.attr(genre="wrapping")
    def test_ent_new_android(self):
        """
            1)log into enterprise account, generate a new Android application, load wrapping page
        """
        self.browser.get(config.CliConfig().common.url + "/developers/logout")
        app_name = self.create_new_app(1)

        app_ids = team.get_id_from_app_name(self.browser, app_name)
        self.browser.get(self.config.common.url + "/developers/wrapping/" + app_ids[0])
        self.browser.implicitly_wait(2)
        self.assertNotEqual(self.browser.current_url, "https://app-staging.crittercism.com/developers/wrapping/" + app_ids[0],
                         "Loaded wrapping page for a non- iOS application")
        team.delete_app_given_ids(browser=self.browser, app_ids=self.app_ids)

    ################BASIC LEVEL#####################

    #####TRIAL#####

    @nose.plugins.attrib.attr(genre="wrapping")
    def test_create_basic_new_ios(self):
        """
            1)create basic account, generate a new iOS application, load wrapping page
        """
        self.browser.get(config.CliConfig().common.url + "/developers/logout")

        self.sign_up_new_account(2)
        app_name = self.create_new_app(0)

        app_ids = team.get_id_from_app_name(self.browser, app_name)
        self.browser.get(self.config.common.url + "/developers/wrapping/" + app_ids[0])
        self.browser.implicitly_wait(2)
        self.assertEqual(self.browser.current_url, "https://app-staging.crittercism.com/developers/wrapping/" + app_ids[0],
                         "Expected wrapping page, and instead got %s" % self.browser.current_url)
        team.delete_app_given_ids(browser=self.browser, app_ids=self.app_ids)

    @nose.plugins.attrib.attr(genre="wrapping")
    def test_ent_new_android(self):
        """
            1)log into enterprise account, generate a new Android application, load wrapping page
        """
        self.browser.get(config.CliConfig().common.url + "/developers/logout")

        self.sign_up_new_account(2)
        app_name = self.create_new_app(1)

        app_ids = team.get_id_from_app_name(self.browser, app_name)
        self.browser.get(self.config.common.url + "/developers/wrapping/" + app_ids[0])
        self.browser.implicitly_wait(2)
        self.assertNotEqual(self.browser.current_url, "https://app-staging.crittercism.com/developers/wrapping/" + app_ids[0],
                         "Loaded wrapping page for a non- iOS application")
        team.delete_app_given_ids(browser=self.browser, app_ids=self.app_ids)

    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):

        super(WrappingTestSuite, cls).tearDownClass()

        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)