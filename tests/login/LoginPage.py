import time

from nose.plugins.attrib import attr
from selenium.webdriver.firefox import webdriver

from src import baseTest

__author__ = 'farooque'

#import unittest
#from selenium import webdriver

class LoginPage(baseTest.SeleniumTestCase):

    def setUp(self):
#        self.selenium = webdriver.Firefox()
#        self.addCleanup(self.selenium.quit)
#        self.getLoginPage()
        pass

    def getLoginPage(self):
        self.selenium.get('https://app.crittercism.com/developers/login')
        self.assertIn("Crittercism - Login", self.selenium.title)

    def gotoGoogleSignin(self):
        self.getLoginPage()
        inputElement = self.selenium.find_element_by_id("google-openid-2")
        inputElement.click()
        self.assertIn('Sign in - Google Accounts', self.selenium.title)

    def gotoCrittercismLoginPage(self):
        self.getLoginPage()
        pass

    def loginToGoogleByPasswordOnly(self):
        password = self.selenium.find_element_by_id("Passwd")
        #password.send_keys("critpass123")
        password.send_keys("saranzara143")
        self.selenium.find_element_by_id("signIn").click()
        #webElement = self.selenium.find_element_by_xpath("/html/body/div[4]/div/div/div/h2")
        #self.assertIn("It looks like this is your first time here!", webElement.text)

    def signinFromGoogleAccountIfAlreadytLoggedIn(self):
        pass

    def signinFromGoogleAccountByUserNameAndPassword(self):
        email = self.selenium.find_element_by_id("Email")
        #email.send_keys("nsolaiappan@login.com")
        email.send_keys("farooque.sayed")
        self.loginToGoogleByPasswordOnly()

    def signinFromGoogleAccountByPassword(self):
        self.loginToGoogleByPasswordOnly()
        pass

    def signInFromGoogle(self):
        self.gotoGoogleSignin()
        if self.selenium.find_element_by_id("Email") :
            self.signinFromGoogleAccountByUserNameAndPassword()
        elif self.selenium.find_element_by_id("Passwd") :
            self.signinFromGoogleAccountByPassword()
        else:
            self.signinFromGoogleAccountIfAlreadytLoggedIn()
            pass

    def loginFromCrittercism(self):
        self.getLoginPage()
        emailTxtBox = self.selenium.find_element_by_id("email")
        emailTxtBox.send_keys("nsolaiappan@login.com")
        passwd = self.selenium.find_element_by_id("password")
        passwd.send_keys("CritPass123")

        self.selenium.find_element_by_id("commit").click()


    def isLoginSucceed(self):
        self.selenium.get("https://app.login.com/developers")
        #self.selenium.support.ui.WebDriverWait()

        registerNewAppButton = self.selenium.find_elements_by_xpath("//*[@class='button btn-blue']")

        if registerNewAppButton is None:
             return False

        return True


    def testGoogleSignIn(self):
        self.signInFromGoogle()
        self.assertEquals(self.isLoginSucceed(), True, "Login Failed")

    def testGoogleSignInByUsernameAndPassword(self):
        self.gotoGoogleSignin()
        self.assertEquals(self.isLoginSucceed(), True, "Login Failed")

        # Setup the browser to do this


    @attr(genre="tests")
    def testFAQ(self):
        self.signInFromGoogle()
        self.selenium.find_element_by_link_text("Billing FAQ").click()

    def testCheckTableContentChangeSettings(self):
        self.signInFromGoogle()
        self.selenium.get("https://app.login.com/developers/register_application")
        time.sleep(3)
        table = self.selenium.find_element_by_xpath('//*[contains(text(),"Change Settings")]/..')
        count = table.find_elements_by_xpath ("./*[@class='disabled']")
        self.assertEquals(count.__len__(),2,"Expecting Disabled found Enabled")

    def testCheckTableContentCrashData(self):
        self.signInFromGoogle()
        self.selenium.get("https://app.login.com/developers/register_application")
        time.sleep(3)
        table = self.selenium.find_element_by_xpath('//*[contains(text(),"View Crash Data")]/..')
        count = table.find_elements_by_xpath ("./*[@class='disabled']")
        self.assertEquals(count.__len__(),2,"Expecting Disabled found Enabled")

    def testmethod(self):
        pass

    def testSigninFromCrittercismAccount(self):
        self.loginFromCrittercism()

        self.assertEquals(self.isLoginSucceed(), True, "Login Failed")
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
