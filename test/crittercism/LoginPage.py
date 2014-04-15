from nose.plugins.attrib import attr
import time

__author__ = 'farooque'

import unittest
from selenium import webdriver

class LoginPage(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.addCleanup(self.browser.quit)
        self.getLoginPage()

    def getLoginPage(self):
        self.browser.get('https://app.crittercism.com/developers/login')
        self.assertIn("Crittercism - Login", self.browser.title)

    def gotoGoogleSignin(self):
        self.getLoginPage()
        inputElement = self.browser.find_element_by_id("google-openid-2")
        inputElement.click()
        self.assertIn('Sign in - Google Accounts', self.browser.title)

    def gotoCrittercismLoginPage(self):
        self.getLoginPage()
        pass

    def loginToGoogleByPasswordOnly(self):
        password = self.browser.find_element_by_id("Passwd")
        password.send_keys("saranzara143")
        self.browser.find_element_by_id("signIn").click()
        #webElement = self.browser.find_element_by_xpath("/html/body/div[4]/div/div/div/h2")
        #self.assertIn("It looks like this is your first time here!", webElement.text)

    def signinFromGoogleAccountIfAlreadytLoggedIn(self):
        pass

    def signinFromGoogleAccountByUserNameAndPassword(self):
        email = self.browser.find_element_by_id("Email")
        email.send_keys("farooque.sayed@gmail.com")
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
            pass

    def testGoogleSignIn(self):
        self.signInFromGoogle()

    def testGoogleSignInByUsernameAndPassword(self):
        self.gotoGoogleSignin()

        # Setup the browser to do this


    @attr(genre="test")
    def testFAQ(self):
        self.signInFromGoogle()
        self.browser.find_element_by_link_text("Billing FAQ").click()

    def testCheckTableContentChangeSettings(self):
        self.signInFromGoogle()
        self.browser.get("https://app.crittercism.com/developers/register_application")
        time.sleep(3)
        table = self.browser.find_element_by_xpath('//*[contains(text(),"Change Settings")]/..')
        count = table.find_elements_by_xpath ("./*[@class='disabled']")
        self.assertEquals(count.__len__(),2,"Expecting Disabled found Enabled")

    def testCheckTableContentCrashData(self):
        self.signInFromGoogle()
        self.browser.get("https://app.crittercism.com/developers/register_application")
        time.sleep(3)
        table = self.browser.find_element_by_xpath('//*[contains(text(),"View Crash Data")]/..')
        count = table.find_elements_by_xpath ("./*[@class='disabled']")
        self.assertEquals(count.__len__(),2,"Expecting Disabled found Enabled")

    def testmethod(self):
        pass

    def testSigninFromCrittercismAccount(self):
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
