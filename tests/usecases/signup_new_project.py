import random
from nose.plugins.attrib import attr
from selenium.webdriver.common.by import By
from src import clogger
from src import config
from src import baseTest
from src.constants import BrowserConstants
from src.page_helpers import utils
from src.page_helpers import team

__author__ = 'fsayed'

logger = clogger.setup_custom_logger(__name__)

page_url = config.CliConfig().common.url + "/developers/register-application"

class CustomerUseCasesSignUp(baseTest.SeleniumTestCase):

    @classmethod
    def setUpClass(cls):
        super(CustomerUseCasesSignUp, cls).setUpClass()


    def setUp(self):
        self.browser.get(page_url)

    @attr(genre='usecases')
    def test_new_account_signup_create_project_with_default_parameter(self):
        __name__ + "[Test] Signup for new basic account and create a new project"

        self.browser.get(self.config.common.url + "/signup?plan=basic")
        random_email = (self.config.login.test_user_engg).replace('@', str(random.random()) + '@')
        self.browser.find_element_by_id("firstname").send_keys("test_user_basic")
        self.browser.find_element_by_id("lastname").send_keys("crittercism")
        self.browser.find_element_by_id("company").send_keys("crittercism")
        self.browser.find_element_by_id("phone").send_keys("123-456-7890")
        self.browser.find_element_by_id("email").send_keys(random_email)
        self.browser.find_element_by_id("password").send_keys(self.config.login.password)
        # Hit the button to signup the user
        utils.find_element_and_click(browser=self.browser, by=By.XPATH, value="//*[contains(@class,'grid_8 push_2')]")
        # Start to create a new project
        app_name = "IOS-" + str(random.random())
        self.browser.find_element_by_id("app-name").send_keys(app_name)
        self.assertFalse(utils.find_element_and_submit(self.browser, By.ID, BrowserConstants.COMMIT),
                                 " Broken link at " + self.browser.current_url)
        web_element = utils.get_web_element(browser=self.browser,by=By.XPATH,
                                            value='//*[@id="app-table"]/tbody/*/td[2]/a[contains(text(),"' + app_name + '")]')

        self.assertEquals(web_element.text, app_name, "App creation failed")
        #Delete the test project created
        app_ids = team.get_id_from_app_name(browser=self.browser, app_name=app_name)
        team.delete_app_given_ids(browser=self.browser, app_ids=app_ids)

    def tearDown(self):
       pass


    @classmethod
    def tearDownClass(cls):
        super(CustomerUseCasesSignUp, cls).tearDownClass()
        logger.info("Finished executing SampleTestSuite")
        pass

