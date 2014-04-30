import time
import random

from nose.plugins.attrib import attr
from selenium.webdriver.support.select import Select


__author__ = 'farooque'

from src import clogger
from src import baseTest
from src.page_helpers import team
from src import config

page_url = config.CliConfig().common.url + "/developers/register-application"

#app_name = "TiborTestAPP"
app_name = "IOS-" + str(random.random())

logger = clogger.setup_custom_logger(__name__)

class AddTeamMemberSuite(baseTest.CrittercismTestCase):

    def wait_for_email(self):
        counter = 0
        self.browser.get("https://mail.yahoo.com")
        self.browser.find_element_by_id("username").send_keys(self.config.login.test_user_engg)
        self.browser.find_element_by_id("passwd").send_keys(self.config.login.password)
        self.browser.find_element_by_id(".save").click()

        while counter < 10 :
            if self.browser.find_elements_by_xpath('//*[contains(text(),"Added as a team member for ' + app_name + '")]').__len__():
                self.browser.find_element_by_xpath('//*[contains(text(),"Added as a team member for ' + app_name + '")]').click()
                self.browser.find_element_by_xpath('//a[contains(text(),"Click Here to")]').click()
                return True
            logger.debug("Email  not arrived. will try again after 10 seconds. So far %d seconds spent" % (counter * 10))
            time.sleep(10) # Sleeping for email to arrive
            counter += 1
            self.browser.refresh()

        return False


    @classmethod
    def setUpClass(cls):
        super(AddTeamMemberSuite, cls).setUpClass()
        pass

    def setUp(self):

        self.browser.get(page_url)

        #app_name = "IOS-" + str(random.random())
        self.browser.find_element_by_id("app-name").send_keys(app_name)
        self.browser.find_element_by_id("commit").click()
        web_element = self.browser.find_element_by_xpath(
            '//*[@id="app-table"]/tbody/*/td[2]/a[contains(text(),"' + app_name + '")]')
        self.assertEquals(web_element.text, app_name, "App creation failed")

        app_id = team.get_id_from_app_name(browser=self.browser,app_name=app_name)
        logger.debug("Found the ID = %s" % app_id[0])
        self.browser.get(self.config.common.url + "/developers/app-settings/" + app_id[0] + "#team-members")

        # Remove existing permissions

        for item in self.browser.find_elements_by_xpath("//*[contains(text(),'Remove')]"):
            item.click()

        for item in self.browser.find_elements_by_xpath("//*[contains(text(),'Revoke Invite')]"):
            item.click()


    @attr(genre="invite-member1")
    def test_add_team_member_engg(self):

        #app_name = "crittercism.engg"

        self.browser.find_element_by_id("team_email").send_keys(self.config.login.test_user_engg)
        select = Select(self.browser.find_element_by_id("team_role"))
        select.select_by_visible_text("Engineer")
        self.browser.find_element_by_name("add-team-member").click()

        #Get to yahoo mail to activate the link
        self.wait_for_email()
        self.browser.find_element_by_id('email').send_keys(self.config.login.test_user_engg)
        self.browser.find_element_by_name('password').send_keys(self.config.login.password)
        self.browser.find_element_by_id('commit').submit()

        with self.multiple_assertions():
            self.assertIn ("developers/app-settings/", self.browser.current_url, "Not able to redirect to App-Setting page")
            self.assertEqual(self.browser.find_element_by_name("name").get_attribute("value"), app_name, "Not able to see the correct App name")


    @attr(genre="invite-member2")
    def test_add_team_member_admin(self):

        self.browser.find_element_by_id("team_email").send_keys(self.config.login.test_user_engg)
        select = Select(self.browser.find_element_by_id("team_role"))
        select.select_by_visible_text("Admin")
        self.browser.find_element_by_name("add-team-member").click()

        #Goto to yahoo mail to activate the link
        self.wait_for_email()
        with self.multiple_assertions():
            self.assertIn ("developers/app-settings/", self.browser.current_url, "Not able to redirect to App-Setting page")
            self.assertIn(self.browser.find_element_by_xpath('//*[contains(text(),"You are now added to ' + app_name + '")]').is_displayed(),
                          True,"Not able to see the correct App name")
            self.assertIn(self.browser.find_element_by_xpath('//*[contains(text(),"You have been granted Admin access.")]').is_displayed(),
                          True,"Not able to see the message")



    @attr(genre="invite-member1")
    def test_add_team_member_manager(self):

        app_name = "crittercism.manager"

        self.browser.find_element_by_id("team_email").send_keys(self.config.login.test_user_engg)
        select = Select(self.browser.find_element_by_id("team_role"))
        select.select_by_visible_text("Manager")
        self.browser.find_element_by_name("add-team-member").click()

        #Goto to yahoo mail to activate the link
        self.wait_for_email()
        pass

    @classmethod
    def tearDown(self):

        app_ids = team.get_id_from_app_name(browser=self.browser, app_name=app_name)
        self.assertEquals(True, team.delete_app_given_ids(browser=self.browser, app_ids=app_ids),
                          "Deleting App failed")
        pass

    @classmethod
    def tearDownClass(cls):
        super(AddTeamMemberSuite, cls).tearDownClass()
        pass
