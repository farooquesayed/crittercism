import random
import unittest
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import nose.plugins.attrib

from src import clogger
from src import config
from src import baseTest
from src.constants import BrowserConstants
from src.page_helpers import team
from src.page_helpers import utils
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
        #self.logout()
        pass

    def sign_up_new_account(self, accnt):
        """
            creates new account, returns nothing. Brings driver to dashboard for new account
        """
        account_types = generate_account_types()
        self.logout()
        #self.browser.implicitly_wait(3)
        self.browser.get(self.config.common.url + "/signup?plan=" + account_types[accnt])
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
        page_url = self.config.common.url + "/developers/register-application"
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
    def logout(self):
        self.browser.get(self.config.common.url + "/developers/logout")

    def get_back_to_dashboard(self):
        """
            Get back to the enterprise account

        """
        self.logout()
        self.browser.implicitly_wait(1)
        utils.login(self.browser)

    def upload_file(self, app_ids):
        #upload!
        self.find_element_and_click(value='//a[@class="e-appWrappingStart"]')
        self.browser.implicitly_wait(3)
        self.get_web_element(value='//input[@type="file"]').send_keys(os.getcwd() + "/bin/Cactus.ipa")
        self.get_web_element(value='//input[@type="file"]').submit()

        self.find_element_and_click(value='//div[@class="chosen-container chosen-container-single e-sdkSelect e-step2-attr chosen-container-single-nosearch"]')
        self.find_element_and_click(value='//*[contains(text(), "(latest)"]')
        self.find_element_and_click(value='//input[@value="Start Upload!"]')

        patience= 10 #time to wait in seconds
        try:
            element = WebDriverWait(self, patience).until(EC.presence_of_element_located((By.ID, "success")))
        except:
            self.fail("upload timed out")
            pass
        finally:
            pass

    ###TESTS###
    @nose.plugins.attrib.attr(genre="wrapping")
    def test_1_ent_new_ios(self):
        """
            1)log into enterprise account, generate a new iOS application, load wrapping page, wrap an app
        """
        #self.get_back_to_dashboard()
        print os.getcwd()
        app_name = self.create_new_app(0)

        app_ids = team.get_id_from_app_name(self.browser, app_name)
        self.browser.get(self.config.common.url + "/developers/wrapping/" + app_ids[0])
        self.browser.implicitly_wait(2)
        self.assertEqual(self.browser.current_url, "https://app-staging.crittercism.com/developers/wrapping/" + app_ids[0],
                         "Expected wrapping page, and instead got %s" % self.browser.current_url)
        #self.upload_file(app_ids) #under construction
        team.delete_app_given_ids(browser=self.browser, app_ids=app_ids)

    @nose.plugins.attrib.attr(genre="wrapping")
    def test_2_ent_new_android(self):
        """
            2)log into enterprise account, generate a new Android application, load wrapping page
        """
        self.browser.get(self.config.common.url + "/developers/")
        app_name = self.create_new_app(1)

        app_ids = team.get_id_from_app_name(self.browser, app_name)
        self.browser.get(self.config.common.url + "/developers/wrapping/" + app_ids[0])
        self.browser.implicitly_wait(2)
        self.assertNotEqual(self.browser.current_url, "https://app-staging.crittercism.com/developers/wrapping/" + app_ids[0],
                         "Loaded wrapping page for a non- iOS application")
        team.delete_app_given_ids(browser=self.browser, app_ids=app_ids)



    ################TRIAL LEVEL#####################
    @nose.plugins.attrib.attr(genre="wrapping")
    def test_3_create_trial_new_ios(self):
        """
            3)create trial account, generate a new iOS application, load wrapping page
        """

        self.logout()

        self.sign_up_new_account(0)
        app_name = self.create_new_app(0)

        app_ids = team.get_id_from_app_name(self.browser, app_name)
        self.browser.get(self.config.common.url + "/developers/wrapping/" + app_ids[0])
        self.browser.implicitly_wait(2)
        self.assertEqual(self.browser.current_url,self.config.common.url + "/developers/wrapping/" + app_ids[0],
                         "should have received wrapping page for trial account")
        team.delete_app_given_ids(browser=self.browser, app_ids=app_ids)

    @nose.plugins.attrib.attr(genre="wrapping")
    def test_4_create_trial_new_android(self):
        """
            4)create trial account, generate a new Android application, load wrapping page
        """

        self.logout()

        self.sign_up_new_account(0)
        app_name = self.create_new_app(1)

        app_ids = team.get_id_from_app_name(self.browser, app_name)
        self.browser.get(self.config.common.url + "/developers/wrapping/" + app_ids[0])
        self.browser.implicitly_wait(2)
        self.assertNotEqual(self.browser.current_url, "https://app-staging.crittercism.com/developers/wrapping/" + app_ids[0],
                         "Loaded wrapping page for a non- iOS application")
        team.delete_app_given_ids(browser=self.browser, app_ids=app_ids)

    ######BASIC LEVEL######
    @nose.plugins.attrib.attr(genre="wrapping")
    def test_5_basic_new_ios(self):
        """
            5)log into basic account, generate a new iOS application, load wrapping page
        """

        self.logout()
        utils.login(self.browser, username="tkerbosch+integration@crittercism.com", password="crittercism")
        app_name = self.create_new_app(0)

        app_ids = team.get_id_from_app_name(self.browser, app_name)
        self.browser.get(self.config.common.url + "/developers/wrapping/" + app_ids[0])
        self.browser.implicitly_wait(2)
        self.assertNotEqual(self.browser.current_url, "https://app-staging.crittercism.com/developers/wrapping/" + app_ids[0],
                         "Loaded wrapping page for a basic user")
        team.delete_app_given_ids(browser=self.browser, app_ids=app_ids)

    @nose.plugins.attrib.attr(genre="wrapping")
    def test_6_basic_new_android(self):
        """
            6)log into basic account, generate a new android application, load wrapping page
        """

        self.logout()
        utils.login(self.browser, username="tkerbosch+integration@crittercism.com", password="crittercism")
        app_name = self.create_new_app(1)

        app_ids = team.get_id_from_app_name(self.browser, app_name)
        self.browser.get(self.config.common.url + "/developers/wrapping/" + app_ids[0])
        self.browser.implicitly_wait(2)
        self.assertNotEqual(self.browser.current_url, "https://app-staging.crittercism.com/developers/wrapping/" + app_ids[0],
                         "Loaded wrapping page for a non-iOS application with a basic user")
        team.delete_app_given_ids(browser=self.browser, app_ids=app_ids)

    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):

        super(WrappingTestSuite, cls).tearDownClass()

        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)