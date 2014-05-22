import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.data_driven_test_wrapper import data_driven_test, data, ddt_list
from src.page_helpers import utils

__author__ = 'farooque'
import random

from nose.plugins.attrib import attr

from src import clogger
from src import baseTest


logger = clogger.setup_custom_logger(__name__)


def generate_list_of_accounts():
    account_types = []
    account_types.append("basic")
    account_types.append("pro")
    account_types.append("ent")
    account_types.append("pro_plus")
    return account_types


@data_driven_test
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


    @attr(genre="signup1")
    @data(generate_list_of_accounts())
    @ddt_list
    def test_sign_up_new_account(self,value):
        __name__ + """[Test] Sign up using different type of accounts """

        self.browser.get(self.config.common.url + "/signup?plan=" + value)
        random_email = (self.config.login.test_user_engg).replace('@', str(random.random()) + '@')
        self.browser.find_element_by_id("firstname").send_keys("test_user_" + value)
        self.browser.find_element_by_id("lastname").send_keys("crittercism")
        self.browser.find_element_by_id("company").send_keys("crittercism")
        self.browser.find_element_by_id("phone").send_keys("123-456-7890")
        self.browser.find_element_by_id("email").send_keys(random_email)
        self.browser.find_element_by_id("password").send_keys(self.config.login.password)

        #self.browser.find_element_by_xpath("//*[contains(@class,'grid_8 push_2')]").click()
        #self.assertFalse(utils.is_url_broken(browser=self.browser,link=self.browser.current_url), " Oops page was found at " + self.browser.current_url)
        self.assertFalse(utils.find_element_and_submit(self.browser, By.XPATH, "//*[contains(@class,'grid_8 push_2')]"),
                                 " Broken link at " + self.browser.current_url)
        with self.multiple_assertions():
            self.assertEqual(self.browser.find_element_by_id("register-app").is_displayed(), True, "Sign up Failed - register-app button is not displayed")
            self.assertEqual(self.browser.find_element_by_id("commit").is_displayed(), True, "Sign up Failed - Commit button is not displayed")
            self.assertEqual(self.browser.find_element_by_id("platform-ios").get_attribute("value"), "1", "IOS button is not selected")
            self.assertIn("/developers/register_application",self.browser.current_url, "Register New App is not in address bar")
            self.validate_user_profile(random_email, value)

    @attr(genre='signup',smoke=True)
    def test_sign_up_new_account_basic(self):
        __name__ + """[Test] Sign up using different type of accounts """

        self.browser.get(self.config.common.url + "/signup?plan=basic")
        random_email = (self.config.login.test_user_engg).replace('@', str(random.random()) + '@')
        self.browser.find_element_by_id("firstname").send_keys("test_user_basic")
        self.browser.find_element_by_id("lastname").send_keys("crittercism")
        self.browser.find_element_by_id("company").send_keys("crittercism")
        self.browser.find_element_by_id("phone").send_keys("123-456-7890")
        self.browser.find_element_by_id("email").send_keys(random_email)
        self.browser.find_element_by_id("password").send_keys(self.config.login.password)

        #self.browser.find_element_by_xpath("//*[contains(@class,'grid_8 push_2')]").click()
        utils.find_element_and_click(browser=self.browser, by=By.XPATH, value="//*[contains(@class,'grid_8 push_2')]")

        #self.assertFalse(utils.is_url_broken(browser=self.browser,link=self.browser.current_url), " Oops page was found at " + self.browser.current_url)
        with self.multiple_assertions():
            self.assertEqual(self.browser.find_element_by_id("register-app").is_displayed(), True, "Sign up Failed - register-app button is not displayed")
            self.assertEqual(self.browser.find_element_by_id("commit").is_displayed(), True, "Sign up Failed - Commit button is not displayed")
            self.assertEqual(self.browser.find_element_by_id("platform-ios").get_attribute("value"), "1", "IOS button is not selected")
            self.assertIn("/developers/register_application",self.browser.current_url, "Register New App is not in address bar")
            self.validate_user_profile(random_email, "Basic")

    @attr(genre='signup')
    def test_sign_up_page_with_no_data(self):
        __name__ + """[Test] Sign up with no data """

        self.browser.find_element_by_xpath("//*[contains(@class,'grid_8 push_2')]").click()
        total_elements = self.browser.find_elements_by_xpath("// *[contains(text(), 'This field is required')]").__len__()
        self.assertEqual(total_elements, 4, "Expecting 4 Alerts but found %d" %(total_elements))

    @attr(genre='signup')
    def test_sign_up_page_with_only_first_name(self):
        __name__ + """[Test] Sign up using only first name """

        self.browser.find_element_by_id("firstname").send_keys("test_user")
        self.browser.find_element_by_xpath("//*[contains(@class,'grid_8 push_2')]").click()
        total_elements = self.browser.find_elements_by_xpath("//*[contains(text(), 'This field is required')]").__len__()
        self.assertEqual(total_elements, 3, "Expecting 3 Alerts but found %d" % (total_elements))


    @attr(genre='signup')
    def test_sign_up_page_with_only_first_name_last_name(self):
        __name__ + """[Test] Sign up using only first and last time """

        self.browser.find_element_by_id("firstname").send_keys("test_user")
        self.browser.find_element_by_id("lastname").send_keys("crittercism")
        self.browser.find_element_by_xpath("//*[contains(@class,'grid_8 push_2')]").click()
        total_elements = self.browser.find_elements_by_xpath("//*[contains(text(), 'This field is required')]").__len__()
        self.assertEqual(total_elements, 2, "Expecting 2 Alerts but found %d" % (total_elements))


    @attr(genre='signup')
    def test_sign_up_page_with_only_first_name_last_name_email(self):
        __name__ + """[Test] Sign up using only first, last and email  """

        self.browser.find_element_by_id("firstname").send_keys("test_user")
        self.browser.find_element_by_id("lastname").send_keys("crittercism")
        self.browser.find_element_by_id("email").send_keys(self.config.login.test_user_engg)
        self.browser.find_element_by_xpath("//*[contains(@class,'grid_8 push_2')]").click()
        total_elements = self.browser.find_elements_by_xpath("//*[contains(text(), 'This field is required')]").__len__()
        self.assertEqual(total_elements, 1, "Expecting 1 Alerts but found %d" % (total_elements))


    @attr(genre='signup')
    def test_sign_up_new_account_existing_email_address(self):
        __name__ + """[Test] Sign up using existing email address """

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
        # Logout as any user because this needs to login as a admin user
        self.browser.get(self.config.common.url + "/developers/logout")
        utils.login(browser=self.browser)

        search_page_url = self.config.common.url +  "/admin/search"
        #email_id = "nsolaiappan+finarcbasicsignup@crittercism.com"
        self.browser.get(search_page_url)
        self.browser.find_element_by_id("search-email").send_keys(email_id + Keys.ENTER)

        email_link = self.browser.find_element_by_xpath("//a[contains(text(),'" + email_id + "')]").get_attribute("href")
        self.browser.get(email_link)

        actual_email = self.browser.find_element_by_xpath("//table//*/*[contains(text(),'" + email_id + "')]").text
        self.assertEqual(actual_email, email_id, ("Expecting %s email but found %s instead" % (actual_email, email_id)))

        """
        Need to go with Resolved Plan
        billed_plan_caption = self.browser.find_element_by_xpath('//*[@id="admin-portal"]/div/table[1]/tbody/tr[13]/td[1]/strong').text
        billed_plan_value = self.browser.find_element_by_xpath('//*[@id="admin-portal"]/div/table[1]/tbody/tr[13]/td[2]').text
        self.assertEqual(account_type, billed_plan_value, ("Expecting Basic but found %s" % billed_plan_value) )
        """
        pay_via_caption = self.browser.find_element_by_xpath('//*[@id="admin-portal"]/div/table[1]/tbody/tr[16]/td[1]/strong').text
        pay_via_value = self.browser.find_element_by_xpath('//*[@id="admin-portal"]/div/table[1]/tbody/tr[16]/td[2]').text
        self.assertEqual("Credit Card", pay_via_value, ("Expecting Credit Card but found %s" % pay_via_value) )

if __name__ == '__main__':
    unittest.main(verbosity=2)
