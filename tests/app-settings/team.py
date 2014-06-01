import time
import random

from selenium.webdriver.common.by import By
import unittest2 as unittest
from nose.plugins.attrib import attr
from selenium.webdriver.support.select import Select

from src.constants import BrowserConstants
from src.data_driven_test_wrapper import ddt_list, data, data_driven_test


__author__ = 'farooque'

from src import clogger
from src import baseTest
from src.page_helpers import team
from src import config
from src.page_helpers import utils
from src import constants

page_url = config.CliConfig().common.url + "/developers/register-application"

#app_name = "TiborTestAPP"
app_name = "IOS-" + str(random.random())

logger = clogger.setup_custom_logger(__name__)

def generate_list_of_members_types():
    member_types = ["Engineer", "Manager", "Admin"]
    #member_types = ["Admin"]
    return member_types


@data_driven_test
class AddTeamMemberSuite(baseTest.CrittercismTestCase):

    def wait_for_email(self):
        counter = 0
        utils.login_to_yahoo(browser=self.browser)

        while counter < 50:
            if self.browser.find_elements_by_xpath('//*[contains(text(),"Added as a team member for ' + app_name + '")]').__len__():
                self.assertFalse(self.find_element_and_click(by=By.XPATH,
                                                             value='//*[contains(text(),"Added as a team member for ' + app_name + '")]'),
                                 " Broken link at " + self.browser.current_url)

                self.assertFalse(
                    self.find_element_and_click(by=By.XPATH, value='//a[contains(text(),"Click Here to")]'),
                    " Broken link at " + self.browser.current_url)
                # Closing the current yahoo mail browser and click is yielding a new browser window
                self.browser.close()
                return True
            logger.debug("Email  not arrived. will try again after 10 seconds. So far %d seconds spent" % (counter * 10))
            time.sleep(5)  # Sleeping for email to arrive
            counter += 1
            self.browser.refresh()
            time.sleep(5)  # Sleeping for email to arrive
            if counter % 2 == 1:
                #Now check in spam folder
                self.find_element_and_click(by=By.ID, value="spam-label")
                time.sleep(3)  # To Open the email
                self.browser.find_element(by=By.XPATH, value="//*[@class='focusable neoFocusable enabled']").click()
                time.sleep(3)  # TO Select the email
                #Make it not a Spam becuase links are disabled in spam folder
                self.find_element_and_click(by=By.ID, value="btn-not-spam")
            else:
                #Now check in inbox again
                self.find_element_and_click(by=By.XPATH, value="//*[@class='inbox-label icon-text']")

            logger.debug("Sleeping for 3 seconds for page to load")
            time.sleep(3)

        return False

    def validate_team_member_got_subscribed(self,role=None):

        for handle in self.browser.window_handles:
            self.browser.switch_to_window(handle)
            if constants.CRITTERCISM in self.browser.title:
                break # Got the window we are looking for

        self.assertFalse(utils.is_url_broken(browser=self.browser), " Broken link at " + self.browser.current_url)

        with self.multiple_assertions():
            self.assertIn ("developers/app_settings/", self.browser.current_url, ("Not able to redirect to App-Setting page for role = %s" % role))
            self.assertEqual(self.browser.find_element_by_name("name").get_attribute("value"), app_name, ("Not able to see the correct App name for role = %s" % role))

    @classmethod
    def setUpClass(cls):
        super(AddTeamMemberSuite, cls).setUpClass()
        utils.delete_all_yahoo_email(browser=cls.browser)
        pass

    def setUp(self):

        self.browser.get(page_url)

        self.browser.find_element_by_id("app-name").send_keys(app_name)
        self.assertFalse(self.find_element_and_click(by=By.ID, value='commit'), ("Broken link at %s" %
                                                                                 self.browser.current_url))

        web_element = self.browser.find_element_by_xpath(
            '//*[@id="app-table"]/tbody/*/td[2]/a[contains(text(),"' + app_name + '")]')
        self.assertEquals(web_element.text, app_name, "App creation failed")

        app_id = team.get_id_from_app_name(browser=self.browser,app_name=app_name)
        logger.debug("Found the ID = %s" % app_id[0])
        self.browser.get(self.config.common.url + "/developers/app_settings/" + app_id[0] + "#team-members")

        # Remove existing permissions
        for item in self.browser.find_elements_by_xpath("//*[contains(text(),'Remove')]"):
            self.assertFalse(self.click(web_element=item), "Broken link at " + self.browser.current_url)

        for item in self.browser.find_elements_by_xpath("//*[contains(text(),'Revoke Invite')]"):
            self.assertFalse(self.click(web_element=item), "Broken link at " + self.browser.current_url)

    @attr(genre="invite-member")
    @data(generate_list_of_members_types())
    @ddt_list
    def test_add_team_members(self, value):
        __name__ + """[Test] Add Team member as Engineer/Manager/Admin """

        self.browser.find_element_by_id("team_email").send_keys(self.config.login.test_user_engg)
        select = Select(self.browser.find_element_by_id("team_role"))
        select.select_by_visible_text(value)

        self.assertFalse(self.find_element_and_click(by=By.NAME, value='add-team-member'),
                         " Broken link at " + self.browser.current_url)

        #Get to yahoo mail to activate the link
        self.assertEqual(self.wait_for_email(), True, "Email not received waited until 10 mins")
        self.validate_team_member_got_subscribed(value)

    @attr(genre='invite-member')
    def test_register_new_app_with_ios_invite_members(self):
        __name__ + """ [Test] Registering a new IOS app with invitation to users """

        self.browser.get(page_url)
        app_name = "register-with-invite-" + str(random.random())
        self.browser.find_element_by_id("app-name").send_keys(app_name)
        #Inviting collabotor
        self.browser.find_element_by_id("team_members").send_keys(self.config.login.test_user_admin)
        self.assertFalse(self.find_element_and_submit(by=By.ID, value=BrowserConstants.COMMIT),
                         " Broken link at " + self.browser.current_url)

        web_element = self.browser.find_element_by_xpath(
            '//*[@id="app-table"]/tbody/*/td[2]/a[contains(text(),"' + app_name + '")]')
        self.assertEquals(web_element.text, app_name, "App creation failed")
        app_ids = team.get_id_from_app_name(browser=self.browser, app_name=app_name)
        team.delete_app_given_ids(browser=self.browser, app_ids=app_ids)



    def tearDown(self):
        app_ids = team.get_id_from_app_name(browser=self.browser, app_name=app_name)
        self.assertEquals(True, team.delete_app_given_ids(browser=self.browser, app_ids=app_ids), "Deleting App failed")
        pass

    @classmethod
    def tearDownClass(cls):
        super(AddTeamMemberSuite, cls).tearDownClass()
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
