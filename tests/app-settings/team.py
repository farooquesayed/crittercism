import time
import random
from selenium.webdriver.common.by import By

import unittest2 as unittest
from nose.plugins.attrib import attr
from selenium.webdriver.support.select import Select

from src.data_driven_test_wrapper import ddt_list, data, data_driven_test


__author__ = 'farooque'

from src import clogger
from src import baseTest
from src.page_helpers import team
from src import config
from src.page_helpers import utils

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

        while counter < 10 :
            if self.browser.find_elements_by_xpath('//*[contains(text(),"Added as a team member for ' + app_name + '")]').__len__():
                #self.browser.find_element_by_xpath('//*[contains(text(),"Added as a team member for ' + app_name + '")]').click()
                self.assertFalse(utils.find_element_and_click(self.browser,By.XPATH,
                                                '//*[contains(text(),"Added as a team member for ' + app_name + '")]'),
                                        " Broken link at " + self.browser.current_url)

                #self.browser.find_element_by_xpath('//a[contains(text(),"Click Here to")]').click()
                self.assertFalse(utils.find_element_and_click(self.browser, By.XPATH, '//a[contains(text(),"Click Here to")]'),
                                 " Broken link at " + self.browser.current_url)

                return True
            logger.debug("Email  not arrived. will try again after 10 seconds. So far %d seconds spent" % (counter * 10))
            time.sleep(10) # Sleeping for email to arrive
            counter += 1
            self.browser.refresh()

        return False

    def validate_team_member_got_subscribed(self,role=None):

        for handle in self.browser.window_handles:
            self.browser.switch_to_window(handle)
            if "Crittercism " in self.browser.title :
                break # Got the window we are looking for

        with self.multiple_assertions():
            self.assertIn ("developers/app-settings/", self.browser.current_url, ("Not able to redirect to App-Setting page for role = %s" % role))
            self.assertEqual(self.browser.find_element_by_name("name").get_attribute("value"), app_name, ("Not able to see the correct App name for role = %s" % role))

    @classmethod
    def setUpClass(cls):
        super(AddTeamMemberSuite, cls).setUpClass()
        pass

    def setUp(self):

        self.browser.get(page_url)

        #app_name = "IOS-" + str(random.random())
        self.browser.find_element_by_id("app-name").send_keys(app_name)
        #self.browser.find_element_by_id("commit").click()
        self.assertFalse(utils.find_element_and_click(self.browser, By.ID, 'commit'),
                                 " Broken link at " + self.browser.current_url)

        web_element = self.browser.find_element_by_xpath(
            '//*[@id="app-table"]/tbody/*/td[2]/a[contains(text(),"' + app_name + '")]')
        self.assertEquals(web_element.text, app_name, "App creation failed")

        app_id = team.get_id_from_app_name(browser=self.browser,app_name=app_name)
        logger.debug("Found the ID = %s" % app_id[0])
        self.browser.get(self.config.common.url + "/developers/app-settings/" + app_id[0] + "#team-members")

        # Remove existing permissions
        for item in self.browser.find_elements_by_xpath("//*[contains(text(),'Remove')]"):
            #item.click()
            #self.assertFalse(utils.is_url_broken(browser=self.browser), "Broken link at " + self.browser.current_url)
            self.assertFalse(utils.click(browser=self.browser, web_element=item), "Broken link at " + self.browser.current_url)


        for item in self.browser.find_elements_by_xpath("//*[contains(text(),'Revoke Invite')]"):
            #item.click()
            #self.assertFalse(utils.is_url_broken(browser=self.browser), "Broken link at " + self.browser.current_url)
            self.assertFalse(utils.click(browser=self.browser, web_element=item), "Broken link at " + self.browser.current_url)


    @attr(genre="invite-member")
    @unittest.skip("Covered in DDT")
    def test_add_team_member_engg(self):
        __name__ + """[Test] Add Team member as Engineer """

        self.browser.find_element_by_id("team_email").send_keys(self.config.login.test_user_engg)
        select = Select(self.browser.find_element_by_id("team_role"))
        select.select_by_visible_text("Engineer")
        #self.browser.find_element_by_name("add-team-member").click()
        self.assertFalse(utils.find_element_and_click(self.browser, By.NAME, 'add-team-member'),
                                 " Broken link at " + self.browser.current_url)


        #Get to yahoo mail to activate the link
        self.assertEqual(self.wait_for_email(), True, "Email not received waited until 10 mins")
        self.validate_team_member_got_subscribed("Engineer")



    @attr(genre="invite-member")
    @unittest.skip("Covered in DDT")
    def test_add_team_member_admin(self):
        __name__ + """[Test] Add Team member as Admin """

        self.browser.find_element_by_id("team_email").send_keys(self.config.login.test_user_engg)
        select = Select(self.browser.find_element_by_id("team_role"))
        select.select_by_visible_text("Admin")
        #self.browser.find_element_by_name("add-team-member").click()
        self.assertFalse(utils.find_element_and_click(self.browser, By.NAME, 'add-team-member'),
                                 " Broken link at " + self.browser.current_url)

        #Goto to yahoo mail to activate the link
        self.assertEqual(self.wait_for_email(), True, "Email not received waited until 10 mins")
        self.validate_team_member_got_subscribed("Admin")


    @attr(genre="invite-member")
    @unittest.skip("Covered in DDT")
    def test_add_team_member_manager(self):
        __name__ + """[Test] Add Team member as Manager """

        self.browser.find_element_by_id("team_email").send_keys(self.config.login.test_user_engg)
        select = Select(self.browser.find_element_by_id("team_role"))
        select.select_by_visible_text("Manager")
        #self.browser.find_element_by_name("add-team-member").click()
        self.assertFalse(utils.find_element_and_click(self.browser, By.NAME, 'add-team-member'),
                                 " Broken link at " + self.browser.current_url)

        #Get to yahoo mail to activate the link
        self.assertEqual(self.wait_for_email(), True, "Email not received waited until 10 mins")
        self.validate_team_member_got_subscribed("Manager")


    @attr(genre="invite-member")
    @data(generate_list_of_members_types())
    @ddt_list
    def test_add_team_members(self, value):
        __name__ + """[Test] Add Team member as Engineer/Manager/Admin """

        self.browser.find_element_by_id("team_email").send_keys(self.config.login.test_user_engg)
        select = Select(self.browser.find_element_by_id("team_role"))
        select.select_by_visible_text(value)
        self.assertFalse(utils.find_element_and_click(self.browser, By.NAME, 'add-team-member'),
                                 " Broken link at " + self.browser.current_url)

        #Get to yahoo mail to activate the link
        self.assertEqual(self.wait_for_email(), True, "Email not received waited until 10 mins")
        self.validate_team_member_got_subscribed(value)

    def tearDown(self):

        app_ids = team.get_id_from_app_name(browser=self.browser, app_name=app_name)
        self.assertEquals(True, team.delete_app_given_ids(browser=self.browser, app_ids=app_ids),
                          "Deleting App failed")
        pass

    @classmethod
    def tearDownClass(cls):
        super(AddTeamMemberSuite, cls).tearDownClass()
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
