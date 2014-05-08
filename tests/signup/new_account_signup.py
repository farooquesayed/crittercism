import unittest

__author__ = 'farooque'
import random

from nose.plugins.attrib import attr

from src import clogger
from src import baseTest


logger = clogger.setup_custom_logger(__name__)


class NewAccountSignUpTestSuite(baseTest.SeleniumTestCase):

    @classmethod
    def setUpClass(cls):
        super(NewAccountSignUpTestSuite, cls).setUpClass()
        pass

    def setUp(self):
        #Can override the base class setUp here

        self.browser.get(self.config.common.url + "/developers/logout")
        self.browser.get(self.config.common.url + "/signup")
        pass


    @attr(genre='signup')
    def test_sign_up_new_account(self):
        random_email = (self.config.login.test_user_engg).replace('@', str(random.random()) + '@')
        self.browser.find_element_by_id("firstname").send_keys("test_user")
        self.browser.find_element_by_id("lastname").send_keys("crittercism")
        self.browser.find_element_by_id("company").send_keys("crittercism")
        self.browser.find_element_by_id("phone").send_keys("123-456-7890")
        self.browser.find_element_by_id("email").send_keys(random_email)
        self.browser.find_element_by_id("password").send_keys(self.config.login.password)

        self.browser.find_element_by_xpath("//*[contains(@class,'grid_8 push_2')]").click()
        with self.multiple_assertions():
            self.assertEqual(self.browser.find_element_by_id("register-app").is_displayed(), True, "Sign up Failed - register-app button is not displayed")
            self.assertEqual(self.browser.find_element_by_id("commit").is_displayed(), True, "Sign up Failed - Commit button is not displayed")
            self.assertEqual(self.browser.find_element_by_id("platform-ios").get_attribute("value"), "1", "IOS button is not selected")
            self.assertIn("/developers/register_application",self.browser.current_url, "Register New App is not in address bar")


    @attr(genre='signup')
    def test_sign_up_page_with_no_data(self):

        self.browser.find_element_by_xpath("//*[contains(@class,'grid_8 push_2')]").click()
        total_elements = self.browser.find_elements_by_xpath("// *[contains(text(), 'This field is required')]").__len__()
        self.assertEqual(total_elements, 4, "Expecting 4 Alerts but found %d" %(total_elements))


    @attr(genre='signup')
    def test_sign_up_page_with_no_data(self):
        self.browser.find_element_by_xpath("//*[contains(@class,'grid_8 push_2')]").click()
        total_elements = self.browser.find_elements_by_xpath("//*[contains(text(), 'This field is required')]").__len__()
        self.assertEqual(total_elements, 4, "Expecting 4 Alerts but found %d" % (total_elements))


    @attr(genre='signup')
    def test_sign_up_page_with_only_first_name(self):
        self.browser.find_element_by_id("firstname").send_keys("test_user")
        self.browser.find_element_by_xpath("//*[contains(@class,'grid_8 push_2')]").click()
        total_elements = self.browser.find_elements_by_xpath("//*[contains(text(), 'This field is required')]").__len__()
        self.assertEqual(total_elements, 3, "Expecting 3 Alerts but found %d" % (total_elements))


    @attr(genre='signup')
    def test_sign_up_page_with_only_first_name_last_name(self):
        self.browser.find_element_by_id("firstname").send_keys("test_user")
        self.browser.find_element_by_id("lastname").send_keys("crittercism")
        self.browser.find_element_by_xpath("//*[contains(@class,'grid_8 push_2')]").click()
        total_elements = self.browser.find_elements_by_xpath("//*[contains(text(), 'This field is required')]").__len__()
        self.assertEqual(total_elements, 2, "Expecting 2 Alerts but found %d" % (total_elements))


    @attr(genre='signup')
    def test_sign_up_page_with_only_first_name_last_name_email(self):
        self.browser.find_element_by_id("firstname").send_keys("test_user")
        self.browser.find_element_by_id("lastname").send_keys("crittercism")
        self.browser.find_element_by_id("email").send_keys(self.config.login.test_user_engg)
        self.browser.find_element_by_xpath("//*[contains(@class,'grid_8 push_2')]").click()
        total_elements = self.browser.find_elements_by_xpath("//*[contains(text(), 'This field is required')]").__len__()
        self.assertEqual(total_elements, 1, "Expecting 1 Alerts but found %d" % (total_elements))


    @attr(genre='signup')
    def test_sign_up_new_account_existing_email_address(self):
        self.browser.find_element_by_id("firstname").send_keys("test_user")
        self.browser.find_element_by_id("lastname").send_keys("crittercism")
        self.browser.find_element_by_id("company").send_keys("crittercism")
        self.browser.find_element_by_id("phone").send_keys("123-456-7890")
        self.browser.find_element_by_id("email").send_keys(self.config.login.test_user_engg)
        self.browser.find_element_by_id("password").send_keys(self.config.login.password)

        self.browser.find_element_by_xpath("//*[contains(@class,'grid_8 push_2')]").click()
        with self.multiple_assertions():
            self.assertIn("/signup", self.browser.current_url, "Accepted duplicate email")

    def tearDown(self):
        #Can override the base class setUp here
        pass


    @classmethod
    def tearDownClass(self):
        super(NewAccountSignUpTestSuite, self).tearDownClass()
        logger.info("Finished executing NewAccountSignUpTestSuite")
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
