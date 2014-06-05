import unittest
import os
import threading
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys as keys
import nose.plugins.attrib

from src import clogger
from src import baseTest
import src.constants as constants
from src.page_helpers import team
from src.page_helpers import utils


__author__ = 'egeller'

logger = clogger.setup_custom_logger(__name__)

basic_username = "tkerbosch+integration@crittercism.com"
basic_password = "crittercism"


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

    # ###########ENTERPRISE LEVEL#############
    def logout(self):
        self.browser.get(self.config.common.url + "/developers/logout")

    def get_back_to_dashboard(self):
        """
            Get back to the enterprise account

        """
        utils.logout(self)
        self.browser.implicitly_wait(1)
        utils.login(self.browser)

    def handle_dialog(self, element_initiating_dialog, dialog_text_input):
        def _handle_dialog(_element_initiating_dialog):
            _element_initiating_dialog.click()  # thread hangs here until upload dialog closes

        t = threading.Thread(target=_handle_dialog, args=[element_initiating_dialog])
        t.start()
        time.sleep(1)  # poor thread synchronization, but good enough

        upload_dialog = self.browser.switch_to_active_element()
        upload_dialog.send_keys(dialog_text_input)
        upload_dialog.send_keys(keys.ENTER)

    # ####UNDER CONSTRUCTION#####
    def upload_file(self, app_ids):
        patience = 10  #time to wait in seconds
        ipa_path = os.getcwd() + "/bin/Cactus.ipa"

        #upload!
        self.browser.implicitly_wait(2)
        self.find_element_and_click(value='//a[@class="e-appWrappingStart"]')
        self.browser.implicitly_wait(3)
        self.get_web_element(value='//input[@type="file"]').send_keys(ipa_path)  #culprit
        self.browser.implicitly_wait(3)
        self.find_element_and_click(
            value='//div[@class="chosen-container chosen-container-single e-sdkSelect e-step2-attr chosen-container-single-nosearch"]')
        self.find_element_and_click(value='//*[contains(text(), "(latest)"]')
        self.find_element_and_click(value='//input[@value="Start Upload!"]')
        try:
            element = WebDriverWait(self, patience).until(EC.presence_of_element_located((By.ID, "success")))
        except:
            self.fail("upload timed out")
            pass
        finally:
            pass
            #self.get_web_element(value='//input[@type="file"]').submit()

            #The Migraine Method: Using a file dialog instead
            #file_input_element = self.get_web_element(value='//input[@value="Choose File"]')
            #handle_dialog(file_input_element, ipa_path)


    ######END OF CONSTRUCTION######

    ###TESTS###
    @nose.plugins.attrib.attr(genre="wrapping")
    def test_1_ent_new_ios(self):
        """
            1)log into enterprise account, generate a new iOS application, load wrapping page, wrap an app
        """
        #self.get_back_to_dashboard()
        app_name = utils.create_new_app(self, constants.IOS)

        app_ids = team.get_id_from_app_name(self.browser, app_name)
        self.browser.get(self.config.common.url + "/developers/wrapping/" + app_ids[0])
        self.browser.implicitly_wait(2)
        self.assertEqual(self.browser.current_url,
                         "https://app-staging.crittercism.com/developers/wrapping/" + app_ids[0],
                         "Expected wrapping page, and instead got %s" % self.browser.current_url)
        #####UNDER CONSTRUCTION#####
        #self.upload_file(app_ids)
        #####END OF CONSTRUCTION#####
        team.delete_app_given_ids(browser=self.browser, app_ids=app_ids)

    @nose.plugins.attrib.attr(genre="wrapping")
    def test_2_ent_new_android(self):
        """
            2)log into enterprise account, generate a new Android application, load wrapping page
        """
        self.browser.get(self.config.common.url + "/developers/")
        app_name = utils.create_new_app(self, constants.ANDROID)

        app_ids = team.get_id_from_app_name(self.browser, app_name)
        self.browser.get(self.config.common.url + "/developers/wrapping/" + app_ids[0])
        self.browser.implicitly_wait(2)
        self.assertNotEqual(self.browser.current_url,
                            "https://app-staging.crittercism.com/developers/wrapping/" + app_ids[0],
                            "Loaded wrapping page for a non- iOS application")
        team.delete_app_given_ids(browser=self.browser, app_ids=app_ids)


    ################TRIAL LEVEL#####################
    @nose.plugins.attrib.attr(genre="wrapping")
    def test_3_create_trial_new_ios(self):
        """
            3)create trial account, generate a new iOS application, load wrapping page
        """

        utils.logout(self)

        utils.sign_up_new_account(self, constants.ACCOUNT_TYPES.ENTERPRISE)
        app_name = utils.create_new_app(self, constants.IOS)

        app_ids = team.get_id_from_app_name(self.browser, app_name)
        self.browser.get(self.config.common.url + "/developers/wrapping/" + app_ids[0])
        self.browser.implicitly_wait(2)
        self.assertEqual(self.browser.current_url, self.config.common.url + "/developers/wrapping/" + app_ids[0],
                         "should have received wrapping page for trial account")
        team.delete_app_given_ids(browser=self.browser, app_ids=app_ids)

    @nose.plugins.attrib.attr(genre="wrapping")
    def test_4_create_trial_new_android(self):
        """
            4)create trial account, generate a new Android application, load wrapping page
        """

        utils.logout(self)

        utils.sign_up_new_account(self, constants.ACCOUNT_TYPES.ENTERPRISE)
        app_name = utils.create_new_app(self, constants.ANDROID)

        app_ids = team.get_id_from_app_name(self.browser, app_name)
        self.browser.get(self.config.common.url + "/developers/wrapping/" + app_ids[0])
        self.browser.implicitly_wait(2)
        self.assertNotEqual(self.browser.current_url,
                            "https://app-staging.crittercism.com/developers/wrapping/" + app_ids[0],
                            "Loaded wrapping page for a non- iOS application")
        team.delete_app_given_ids(browser=self.browser, app_ids=app_ids)

    ######BASIC LEVEL######
    #TODO: point to basic account info on config files
    @nose.plugins.attrib.attr(genre="wrapping")
    def test_5_basic_new_ios(self):
        """
            5)log into basic account, generate a new iOS application, load wrapping page
        """

        utils.logout(self)
        utils.login(self.browser, username=basic_username, password=basic_password)
        app_name = utils.create_new_app(self, constants.IOS)

        app_ids = team.get_id_from_app_name(self.browser, app_name)
        self.browser.get(self.config.common.url + "/developers/wrapping/" + app_ids[0])
        self.browser.implicitly_wait(2)
        self.assertNotEqual(self.browser.current_url,
                            "https://app-staging.crittercism.com/developers/wrapping/" + app_ids[0],
                            "Loaded wrapping page for a basic user")
        team.delete_app_given_ids(browser=self.browser, app_ids=app_ids)

    @nose.plugins.attrib.attr(genre="wrapping")
    def test_6_basic_new_android(self):
        """
            6)log into basic account, generate a new android application, load wrapping page
        """

        utils.logout(self)
        utils.login(self.browser, username=basic_username, password=basic_password)
        app_name = utils.create_new_app(self, constants.ANDROID)

        app_ids = team.get_id_from_app_name(self.browser, app_name)
        self.browser.get(self.config.common.url + "/developers/wrapping/" + app_ids[0])
        self.browser.implicitly_wait(2)
        self.assertNotEqual(self.browser.current_url,
                            "https://app-staging.crittercism.com/developers/wrapping/" + app_ids[0],
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