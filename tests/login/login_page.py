import time

import unittest2 as unittest
import nose.plugins.attrib
from selenium.webdriver.common.by import By

from src import baseTest
from src import clogger
from src import config
from src.page_helpers import utils


logger = clogger.setup_custom_logger(__name__)

__author__ = 'farooque'


page_url = config.CliConfig().common.url + "/developers/logout"

class LoginPageSuite(baseTest.SeleniumTestCase):
    #TODO: Move this to Utils or BaseClass and combine into one function from team.py
    def wait_for_password_reset_email(self):

        counter = 0
        utils.login_to_yahoo(browser=self.browser)
        while counter < 10 :
            if self.browser.find_elements_by_xpath('//*[contains(text(),"Reset Your Password")]').__len__():
                self.browser.find_element_by_xpath('//*[contains(text(),"Reset Your Password")]').click()
                time.sleep(5)
                self.assertFalse(self.find_element_and_click(by=By.XPATH, value='//a[contains(text(),"Memory Blip")]'),
                                 " Broken link at " + self.browser.current_url)

                logger.debug("Closing the browser containing yahoo email")
                #self.browser.close()
                return True
            logger.debug("Email  not arrived. will try again after 10 seconds. So far %d seconds spent" % (counter * 10))
            time.sleep(5)  # Sleeping for email to arrive
            counter += 1
            self.browser.refresh()
            time.sleep(5)  # Sleeping for email to arrive
            if counter % 2 == 1:
                #Now check in spam folder
                self.find_element_and_click(by=By.ID, value="spam-label")
                time.sleep(3)  # To Open the email
                self.browser.find_element(by=By.XPATH, value="//*[@class='focusable neoFocusable enabled']").click()
                time.sleep(3)  # TO Select the email
                #Make it not a Spam becuase links are disabled in spam folder
                self.find_element_and_click(by=By.ID, value="btn-not-spam")
            else:
                #Now check in inbox again
                self.find_element_and_click(by=By.XPATH, value="//*[@class='inbox-label icon-text']")

            logger.debug("Sleeping for 3 seconds for page to load")
            time.sleep(3)

        return False


    def validate_password_was_reset(self):
        for handle in self.browser.window_handles:
            self.browser.switch_to_window(handle)
            if "Crittercism " in self.browser.title :
                break # Got the window we are looking for

        self.browser.find_element_by_id("pass").send_keys(self.config.login.test_user_password)
        self.browser.find_element_by_id("pass2").send_keys(self.config.login.test_user_password)
        self.assertFalse(self.find_element_and_submit(by=By.ID, value="commit"),
                         " Broken link at " + self.browser.current_url)

        with self.multiple_assertions():
            self.assertIn("developers/", self.browser.current_url, " Didn't login automatically after password change")
            self.assertTrue(self.browser.find_elements_by_xpath("//*[contains(text(),'Register a New App')]").__len__(),
                            "Didn't get redirected to New app register page")

    @classmethod
    def setUpClass(cls):
        super(LoginPageSuite, cls).setUpClass()
        utils.delete_all_yahoo_email(browser=cls.browser)

    def setUp(self):
        self.browser.get(page_url)
        pass

    def get_login_page(self):
        self.browser.get(self.config.common.url)
        #time.sleep(2)
        self.browser.get(page_url)
        #self.assertIn("Crittercism - Login", self.browser.title)

    def goto_google_signin(self):
        """
        """
        # self.browser.get(page_url)
        # self.get_login_page()
        self.browser.find_element_by_id("google-openid-2").click()
        #self.assertIn('Sign in - Google Accounts', self.browser.title)

    def goto_crittercism_login_page(self):
        """
        """
        self.get_login_page()
        pass

    def login_to_google_by_password_only(self):
        """


        """
        password = self.browser.find_element_by_id("Passwd")
        password.send_keys(self.config.login.password)
        self.browser.find_element_by_id("signIn").click()

    def signin_from_google_account_if_already_logged_in(self):
        """


        """
        pass

    def signin_from_google_account_by_username_and_password(self):
        """


        """
        #self.goto_google_signin()
        email = self.browser.find_element_by_id("Email")
        email.send_keys(self.config.login.username)
        self.login_to_google_by_password_only()

    def signin_from_google_account_by_password(self):
        self.login_to_google_by_password_only()

    def signIn_from_google(self):

        self.browser.find_element_by_id("google-openid-2").click()
        if self.browser.find_element_by_id("Email"):
            self.signin_from_google_account_by_username_and_password()
        elif self.browser.find_element_by_id("Passwd"):
            self.signin_from_google_account_by_password()
        else:
            self.signin_from_google_account_if_already_logged_in()

    def login_from_crittercism(self):
        self.get_login_page()
        self.browser.find_element_by_id("email").clear()
        self.browser.find_element_by_id("email").send_keys(self.config.login.username)
        self.browser.find_element_by_id("password").send_keys(self.config.login.password)

        self.browser.find_element_by_id("commit").click()
        time.sleep(5)

    def is_login_succeed(self):

        registerNewAppButton = self.browser.find_elements_by_xpath("//*[@class='button btn-blue']")

        if registerNewAppButton.__len__():
            return True

        return False

    @nose.plugins.attrib. attr(genre="login", smoke=True)
    def test_crittercism_sign_in(self):
        __name__ + """[Test] Login using Crittercism info """

        self.login_from_crittercism()
        self.assertEquals(self.is_login_succeed(), True, "Login Failed -- New App Button Not found")
        pass

    @nose.plugins.attrib. attr(genre="login")
    def test_google_sign_in(self):
        __name__ + """[Test] Login using google credential """

        self.signIn_from_google()
        self.assertEquals(self.is_login_succeed(), True, "Login Failed")

    @nose.plugins.attrib. attr(genre="login")
    def test_login_forgot_password(self):
        __name__ + """ [Test] Forgot Password  """

        forgot_password_link = self.config.common.url + "/developers/forgot-password"
        self.browser.get(forgot_password_link)
        self.browser.find_element_by_id("email").send_keys(self.config.login.test_user_engg)
        #self.browser.find_element_by_id("commit").submit()
        self.assertFalse(self.find_element_and_submit(by=By.ID, value="commit"),
                         " Broken link at " + self.browser.current_url)

        self.assertIn("reset-password", self.browser.current_url, "It was not redirected to reset-password link")
        self.assertEqual(self.browser.find_elements_by_xpath("//*[contains(text(),'Reset Your Password')]").__len__(),1,
                         "Didn't get the text saying password reset was successful")

        #Login to yahoo portal
        self.assertEqual(self.wait_for_password_reset_email(), True, "Email not received waited until 10 mins")
        self.validate_password_was_reset()

    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        super(LoginPageSuite, cls).tearDownClass()
        logger.info("Finished executing SampleTestSuite")
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
