import time
import unittest2 as unittest
import nose.plugins.attrib

from src import baseTest
from src import clogger

logger = clogger.setup_custom_logger(__name__)

__author__ = 'farooque'

page_url = "https://app.crittercism.com/developers/logout"


class LoginPageSuite(baseTest.SeleniumTestCase):

    def setUp(self):
        """


        """
        self.browser.get(page_url)
        pass

    def get_login_page(self):
        """

        

        :rtype : object
        """
        #self.browser.get(self.config.login.login_url)
        #time.sleep(2)
        self.browser.get(page_url)
        #self.assertIn("Crittercism - Login", self.browser.title)

    def goto_google_signin(self):
        """
        """
        #self.browser.get(page_url)
        self.get_login_page()
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
        self.goto_google_signin()
        email = self.browser.find_element_by_id("Email")
        email.send_keys(self.config.login.username)
        self.login_to_google_by_password_only()

    def signin_from_google_account_by_password(self):
        """


        """
        self.login_to_google_by_password_only()

    def signIn_from_google(self):
        """


        """
        self.goto_google_signin()
        if self.browser.find_element_by_id("Email"):
            self.signin_from_google_account_by_username_and_password()
        elif self.browser.find_element_by_id("Passwd"):
            self.signin_from_google_account_by_password()
        else:
            self.signin_from_google_account_if_already_logged_in()

    def login_from_crittercism(self):
        self.get_login_page()
        self.browser.find_element_by_id("email").send_keys(self.config.login.username)
        self.browser.find_element_by_id("password").send_keys(self.config.login.password)

        self.browser.find_element_by_id("commit").click()
        time.sleep(5)

    def is_login_succeed(self):
        self.browser.get("https://app.crittercism.com/developers")
        #self.browser.support.ui.WebDriverWait()

        registerNewAppButton = self.browser.find_elements_by_xpath("//*[@class='button btn-blue']")

        if registerNewAppButton.__len__():
            return True

        return False

    @nose.plugins.attrib. attr(genre="login")
    def test_google_sign_in(self):
        self.signIn_from_google()
        self.assertEquals(self.is_login_succeed(), True, "Login Failed")


    @nose.plugins.attrib. attr(genre="login", smoke=True)
    def test_crittercism_sign_in(self):
        """



        """
        self.login_from_crittercism()
        self.assertEquals(self.is_login_succeed(), True, "Login Failed -- New App Button Not found")
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
