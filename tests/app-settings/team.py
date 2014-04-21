from selenium.webdriver.support.select import Select
import time

__author__ = 'farooque'

from src import clogger
from src import baseTest
from src.page_helpers import team

page_url = "https://app.crittercism.com/developers/app-settings/"
#app_name = "TiborTestAPP"
app_name = "zakirtest"

logger = clogger.setup_custom_logger(__name__)

class AddTeamMemberSuite(baseTest.SeleniumTestCase):

    @classmethod
    def setUpClass(self):
        super(AddTeamMemberSuite, self).setUpClass()
        pass

    def setUp(self):
        app_id = team.get_id_from_app_name(browser=self.browser,app_name=app_name)
        logger.debug("Found the ID = %s" % app_id[0])
        self.browser.get(page_url + app_id[0] + "#team-members")


    def test_add_team_member_engg(self):

        app_name = "crittercism.engg"

        self.browser.find_element_by_id("team_email").send_keys(self.config.login.test_user_engg)
        select = Select(self.browser.find_element_by_id("team_role"))
        select.select_by_visible_text("Engineer")
        self.browser.find_element_by_name("add-team-member").click()
        time.sleep (30) # Email to appear on yahoo mail

        #Get to yahoo mail to activate the link

        self.browser.get("https://mail.yahoo.com")
        self.browser.find_element_by_id("username").send_keys(self.config.login.test_user_engg)
        self.browser.find_element_by_id("passwd").send_keys(self.config.login.password)
        self.browser.find_element_by_id(".save").click()
        time.sleep(10) # login to yahoo mail
        self.browser.find_element_by_xpath('//*[contains(text(),"Added as a team member for ' + app_name + '")]').click()
        time.sleep(5) # wait for email to open
        self.browser.find_element_by_xpath('//*[contains(text(),"Click Here to Activate Your Crittercism Account")]').click()
        pass

    def test_add_team_member_admin(self):

        app_name = "crittercism.admin"

        self.browser.find_element_by_id("team_email").send_keys(self.config.login.test_user_engg)
        select = Select(self.browser.find_element_by_id("team_role"))
        select.select_by_visible_text("Admin")
        self.browser.find_element_by_name("add-team-member").click()
        time.sleep (30) # Email to appear on yahoo mail

        #Get to yahoo mail to activate the link

        self.browser.get("https://mail.yahoo.com")
        self.browser.find_element_by_id("username").send_keys(self.config.login.test_user_engg)
        self.browser.find_element_by_id("passwd").send_keys(self.config.login.password)
        self.browser.find_element_by_id(".save").click()
        time.sleep(10) # login to yahoo mail
        self.browser.find_element_by_xpath('//*[contains(text(),"Added as a team member for ' + app_name + '")]').click()
        time.sleep(5) # wait for email to open
        self.browser.find_element_by_xpath('//*[contains(text(),"Click Here to Activate Your Crittercism Account")]').click()
        pass

    def test_add_team_member_manager(self):

        app_name = "crittercism.manager"

        self.browser.find_element_by_id("team_email").send_keys(self.config.login.test_user_engg)
        select = Select(self.browser.find_element_by_id("team_role"))
        select.select_by_visible_text("Manager")
        self.browser.find_element_by_name("add-team-member").click()
        time.sleep (30) # Email to appear on yahoo mail

        #Get to yahoo mail to activate the link

        self.browser.get("https://mail.yahoo.com")
        self.browser.find_element_by_id("username").send_keys(self.config.login.test_user_engg)
        self.browser.find_element_by_id("passwd").send_keys(self.config.login.password)
        self.browser.find_element_by_id(".save").click()
        time.sleep(10) # login to yahoo mail
        self.browser.find_element_by_xpath('//*[contains(text(),"Added as a team member for ' + app_name + '")]').click()
        time.sleep(5) # wait for email to open
        self.browser.find_element_by_xpath('//*[contains(text(),"Click Here to Activate Your Crittercism Account")]').click()
        pass

    @classmethod
    def tearDownClass(self):
        super(AddTeamMemberSuite, self).tearDownClass()
        pass
