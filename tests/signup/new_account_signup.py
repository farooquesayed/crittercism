import unittest
from selenium.webdriver.common.keys import Keys
from src.page_helpers import utils

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


    @attr(genre='signup',smoke=True)
    def test_sign_up_new_account(self):
        self.browser.get(self.config.common.url + "/signup?plan=basic")
        random_email = (self.config.login.test_user_engg).replace('@', str(random.random()) + '@')
        self.browser.find_element_by_id("firstname").send_keys("test_user")
        self.browser.find_element_by_id("lastname").send_keys("crittercism")
        self.browser.find_element_by_id("company").send_keys("crittercism")
        self.browser.find_element_by_id("phone").send_keys("123-456-7890")
        self.browser.find_element_by_id("email").send_keys(random_email)
        self.browser.find_element_by_id("password").send_keys(self.config.login.password)

        self.browser.find_element_by_xpath("//*[contains(@class,'grid_8 push_2')]").click()
        self.assertFalse(utils.is_url_broken(browser=self.browser,link=self.browser.current_url), " Oops page was found at " + self.browser.current_url)
        with self.multiple_assertions():
            self.assertEqual(self.browser.find_element_by_id("register-app").is_displayed(), True, "Sign up Failed - register-app button is not displayed")
            self.assertEqual(self.browser.find_element_by_id("commit").is_displayed(), True, "Sign up Failed - Commit button is not displayed")
            self.assertEqual(self.browser.find_element_by_id("platform-ios").get_attribute("value"), "1", "IOS button is not selected")
            self.assertIn("/developers/register_application",self.browser.current_url, "Register New App is not in address bar")
            self.validate_user_profile(random_email, "Basic")

    @attr(genre='signup')
    def test_sign_up_new_account_professional(self):
        self.browser.get(self.config.common.url + "/signup?plan=pro")
        random_email = (self.config.login.test_user_engg).replace('@', str(random.random()) + '@')
        self.browser.find_element_by_id("firstname").send_keys("test_user")
        self.browser.find_element_by_id("lastname").send_keys("crittercism")
        self.browser.find_element_by_id("company").send_keys("crittercism")
        self.browser.find_element_by_id("phone").send_keys("123-456-7890")
        self.browser.find_element_by_id("email").send_keys(random_email)
        self.browser.find_element_by_id("password").send_keys(self.config.login.password)

        self.browser.find_element_by_xpath("//*[contains(@class,'grid_8 push_2')]").click()
        self.assertFalse(utils.is_url_broken(browser=self.browser,link=self.browser.current_url), " Oops page was found at " + self.browser.current_url)
        with self.multiple_assertions():
            self.assertEqual(self.browser.find_element_by_id("register-app").is_displayed(), True, "Sign up Failed - register-app button is not displayed")
            self.assertEqual(self.browser.find_element_by_id("commit").is_displayed(), True, "Sign up Failed - Commit button is not displayed")
            self.assertEqual(self.browser.find_element_by_id("platform-ios").get_attribute("value"), "1", "IOS button is not selected")
            self.assertIn("/developers/register_application",self.browser.current_url, "Register New App is not in address bar")
            self.validate_user_profile(random_email, "Professional")

    @attr(genre='signup')
    def test_sign_up_new_account_professional_pro(self):
        self.browser.get(self.config.common.url + "/signup?plan=pro_plus")
        random_email = (self.config.login.test_user_engg).replace('@', str(random.random()) + '@')
        self.browser.find_element_by_id("firstname").send_keys("test_user")
        self.browser.find_element_by_id("lastname").send_keys("crittercism")
        self.browser.find_element_by_id("company").send_keys("crittercism")
        self.browser.find_element_by_id("phone").send_keys("123-456-7890")
        self.browser.find_element_by_id("email").send_keys(random_email)
        self.browser.find_element_by_id("password").send_keys(self.config.login.password)

        self.browser.find_element_by_xpath("//*[contains(@class,'grid_8 push_2')]").click()
        self.assertFalse(utils.is_url_broken(browser=self.browser,link=self.browser.current_url), " Oops page was found at " + self.browser.current_url)

        with self.multiple_assertions():
            self.assertEqual(self.browser.find_elements_by_id("register-app").__len__(), 1, "Sign up Failed - register-app button is not displayed")
            self.assertEqual(self.browser.find_elements_by_id("commit").__len__(), 1, "Sign up Failed - Commit button is not displayed")
            self.assertEqual(self.browser.find_element_by_id("platform-ios").get_attribute("value"), "1", "IOS button is not selected")
            self.assertIn("/developers/register_application",self.browser.current_url, "Register New App is not in address bar")
            self.validate_user_profile(random_email, "Professional Pro")

    @attr(genre='signup')
    def test_sign_up_page_with_no_data(self):

        self.browser.find_element_by_xpath("//*[contains(@class,'grid_8 push_2')]").click()
        total_elements = self.browser.find_elements_by_xpath("// *[contains(text(), 'This field is required')]").__len__()
        self.assertEqual(total_elements, 4, "Expecting 4 Alerts but found %d" %(total_elements))

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

    def validate_user_profile(self, email_id=None, account_type=None):
        search_page_url = self.config.common.url +  "/admin/search"
        #email_id = "nsolaiappan+finarcbasicsignup@crittercism.com"
        self.browser.get(search_page_url)
        self.browser.find_element_by_id("search-email").send_keys(email_id + Keys.ENTER)

        email_link = self.browser.find_element_by_xpath("//a[contains(text(),'" + email_id + "')]").get_attribute("href")
        self.browser.get(email_link)

        actual_email = self.browser.find_element_by_xpath("//table//*/*[contains(text(),'nsolaiappan+finarcbasicsignup@crittercism.com')]").text
        self.assertEqual(actual_email, email_id, ("Expecting %s email but found %s instead" % (actual_email, email_id)))

        billed_plan_caption = self.browser.find_element_by_xpath('//*[@id="admin-portal"]/div/table[1]/tbody/tr[13]/td[1]/strong').text
        billed_plan_value = self.browser.find_element_by_xpath('//*[@id="admin-portal"]/div/table[1]/tbody/tr[13]/td[2]').text
        self.assertEqual(account_type, billed_plan_value, ("Expecting Basic but found %s" % billed_plan_value) )

        pay_via_caption = self.browser.find_element_by_xpath('//*[@id="admin-portal"]/div/table[1]/tbody/tr[16]/td[1]/strong').text
        pay_via_value = self.browser.find_element_by_xpath('//*[@id="admin-portal"]/div/table[1]/tbody/tr[16]/td[2]').text
        self.assertEqual("Credit Card", pay_via_value, ("Expecting Credit Card but found %s" % pay_via_value) )

if __name__ == '__main__':
    unittest.main(verbosity=2)
