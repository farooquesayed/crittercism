import time

import unittest2 as unittest
from nose.plugins.attrib import attr

from src import baseTest


__author__ = 'farooque'

#import unittest
#from selenium import webdriver

class LoginPageSuite(baseTest.SeleniumTestCase):

    def setUp(self):
        page_url = "https://app.crittercism.com/developers/logout"
        self.browser.get(page_url)

    def getLoginPage(self):
        self.browser.get(self.config.login.login_url)
        self.assertIn("Crittercism - Login", self.browser.title)

    def gotoGoogleSignin(self):
        self.getLoginPage()
        self.browser.find_element_by_id("google-openid-2").click()
        self.assertIn('Sign in - Google Accounts', self.browser.title)

    def gotoCrittercismLoginPage(self):
        self.getLoginPage()
        pass

    def loginToGoogleByPasswordOnly(self):
        password = self.browser.find_element_by_id("Passwd")
        password.send_keys(self.config.login.password)
        self.browser.find_element_by_id("signIn").click()

    def signinFromGoogleAccountIfAlreadytLoggedIn(self):
        pass

    def signinFromGoogleAccountByUserNameAndPassword(self):
        self.gotoGoogleSignin()
        email = self.browser.find_element_by_id("Email")
        email.send_keys(self.config.login.username)
        self.loginToGoogleByPasswordOnly()

    def signinFromGoogleAccountByPassword(self):
        self.loginToGoogleByPasswordOnly()
        pass

    def signInFromGoogle(self):
        self.gotoGoogleSignin()
        if self.browser.find_element_by_id("Email") :
            self.signinFromGoogleAccountByUserNameAndPassword()
        elif self.browser.find_element_by_id("Passwd") :
            self.signinFromGoogleAccountByPassword()
        else:
            self.signinFromGoogleAccountIfAlreadytLoggedIn()

    def loginFromCrittercism(self):
        self.getLoginPage()
        self.browser.find_element_by_id("email").send_keys(self.config.login.username)
        self.browser.find_element_by_id("password").send_keys(self.config.login.password)

        self.browser.find_element_by_id("commit").click()
        time.sleep(1)

    def isLoginSucceed(self):
        self.browser.get("https://app.crittercism.com/developers")
        #self.browser.support.ui.WebDriverWait()

        registerNewAppButton = self.browser.find_elements_by_xpath("//*[@class='button btn-blue']")

        if registerNewAppButton.__len__()  :
             return True

        return False

    @attr(genre="login")
    def test_google_sign_in(self):
        self.signInFromGoogle()
        self.assertEquals(self.isLoginSucceed(), True, "Login Failed")

    @attr(genre="login")
    @unittest.skip("Skipping temporarily")
    def test_google_sign_in_by_username_and_password(self):
        #FIXME : Need to either run this test first or spawn a new browser for this test
        self.signInFromGoogle()
        self.assertEquals(self.isLoginSucceed(), True, "Login Failed")

    @attr(genre="login")
    def test_FAQ(self):
        self.loginFromCrittercism()
        self.browser.find_element_by_link_text("Billing FAQ").click()

    @attr(genre="login")
    def test_check_table_content_crash_data(self):
        self.loginFromCrittercism()
        self.browser.get("https://app.crittercism.com/developers/register_application")
        time.sleep(3)
        table = self.browser.find_element_by_xpath('//*[contains(text(),"View Crash Data")]/..')
        count = table.find_elements_by_xpath ("./*[@class='disabled']")
        self.assertEquals(count.__len__(),2,"Expecting Disabled found Enabled")

    @attr(genre="login")
    def test_signin_from_crittercism_account(self):
        self.loginFromCrittercism()
        self.assertEquals(self.isLoginSucceed(), True, "Login Failed -- New App Button Not found")
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
