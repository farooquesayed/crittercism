import random

from nose.plugins.attrib import attr
from selenium.webdriver.common.by import By

import nose.plugins.attrib

from src import clogger
from src import config
from src import baseTest
from src.constants import BrowserConstants
from src.page_helpers import team

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


account_types = []
account_types.append("basic")
account_types.append("pro")
account_types.append("ent")
account_types.append("pro_plus")

platform_types= []
platform_types.append("IOS")

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
        self.browser.get(self.config.common.url + "/developers/logout")
        self.browser.get(self.config.common.url + "/signup")
        pass

    def sign_up_new_account(self, accnt):
        __name__ + """[Test] Sign up user with all account types """

        self.browser.get(config.CliConfig().common.url + "/developers/logout")
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
        page_url = config.CliConfig().common.url + "/developers/register-application"
        app_name = "IOS-" + str(random.random())
        self.browser.find_element_by_id("app-name").send_keys(app_name)
        self.assertFalse(self.find_element_and_submit(by=By.ID, value=BrowserConstants.COMMIT),
                         " Broken link at " + self.browser.current_url)
        return app_name


    ############ENTERPRISE LEVEL#############
    @nose.plugins.attrib.attr(genre="wrapping")
    def test_ent_new_ios(self):
        """
            1)Create new enterprise account, generate a new iOS application, load wrapping page
        """

        self.sign_up_new_account(2)
        app_name = self.create_new_app("IOS")
        app_id = team.get_id_from_app_name(this.browser, app_name)
        self.browser.get(self.config.common.url + "developers/wrapping/" + app_id)
        self.browser.implicitly_wait(2)
        self.assertEqual(self.browser.current_url, "https://app-staging.crittercism.com/developers/wrapping/" + app_id,
                         "Enterprise users are not directed properly")