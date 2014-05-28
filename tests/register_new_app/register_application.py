import random
import time
from selenium.webdriver.common.by import By

import unittest2 as unittest
from nose.plugins.attrib import attr

from src import baseTest
from src import clogger
from src.page_helpers import team
from src import config
from src.page_helpers import utils
from src.constants import BrowserConstants


__author__ = 'farooque'

logger = clogger.setup_custom_logger(__name__)

page_url = config.CliConfig().common.url + "/developers/register-application"

class RegisterApplication(baseTest.CrittercismTestCase):
    @classmethod
    def setUpClass(cls):
        super(RegisterApplication, cls).setUpClass()
        for app_prefix in ["IOS-0", "Android-0", "HTML5-0", "Win8-0" ] :
            app_ids = team.get_id_from_app_name(browser=cls.browser, app_name=app_prefix)
            team.delete_app_given_ids(browser=cls.browser, app_ids=app_ids)


    def setUp(self):
        self.browser.get(page_url)

    @attr(genre='register-application', smoke=True)
    def test_verify_new_app_page_default_parameter_platform(self):
        __name__ + "[Test] Verifing default parameter platform is selected on New App register page"
        platform_checked = self.browser.find_element_by_id("platform-ios").get_attribute("value")
        self.assertEquals(platform_checked, "1", "Default platform should be IOS")

    @attr(genre='register-application')
    def test_verify_new_app_page_default_parameter_employee_facing(self):
        __name__ + "[Test] Verifing default employee facing is selected on New App register page"
        no_button = self.browser.find_element_by_xpath("//*[@for='is_internal_app_no']").get_attribute("aria-pressed")
        self.assertEquals(no_button, "true", "Default App should be internal")

    @attr(genre='register-application')
    def test_verify_new_app_page_default_parameter_in_app_store(self):
        __name__ + "[Test] Verifing default appstore is selected on New App register page"
        no_button = self.browser.find_element_by_xpath("//*[@for='in_app_store_no']").get_attribute("aria-pressed")
        self.assertEquals(no_button, "true", "Default App should be in app-store")

    @attr(genre='register-application')
    def test_verify_new_app_page_default_permission(self):
        __name__ + "[Test] Verifing default permission is selected on New App register page"

        table = self.browser.find_element_by_xpath('//*[contains(text(),"Change Settings")]/..')
        count = table.find_elements_by_xpath("./*[@class='disabled']")
        self.assertEquals(count.__len__(), 2, "Only Admin should be checked")


    @attr(genre='register-application', smoke=True)
    def test_register_new_app_with_default_parameters_ios(self):
        __name__ + """ [Test] Registering a new IOS app with default parameters """

        app_name = "IOS-" + str(random.random())
        self.browser.find_element_by_id("app-name").send_keys(app_name)
        self.assertFalse(utils.find_element_and_submit(self.browser, By.ID, BrowserConstants.COMMIT),
                                 " Broken link at " + self.browser.current_url)

        web_element = self.browser.find_element_by_xpath(
            '//*[@id="app-table"]/tbody/*/td[2]/a[contains(text(),"' + app_name + '")]')
        self.assertEquals(web_element.text, app_name, "App creation failed")

        app_ids = team.get_id_from_app_name(browser=self.browser, app_name=app_name)
        team.delete_app_given_ids(browser=self.browser, app_ids=app_ids)


    @attr(genre='register-application')
    def test_register_new_app_with_default_parameters_android(self):
        __name__ + """ [Test] Registering a new android app """

        app_name = "Android-" + str(random.random())
        self.browser.find_element_by_id("app-name").send_keys(app_name)

        #self.browser.find_element_by_xpath('//*[@id="all-platforms"]/label[2]').click()
        self.assertFalse(utils.find_element_and_click(self.browser, By.XPATH, '//*[@id="all-platforms"]/label[2]'),
                                 " Broken link at " + self.browser.current_url)

        self.assertFalse(utils.find_element_and_submit(self.browser, By.ID, BrowserConstants.COMMIT),
                                 " Broken link at " + self.browser.current_url)
        web_element = self.browser.find_element_by_xpath(
            '//*[@id="app-table"]/tbody/*/td[2]/a[contains(text(),"' + app_name + '")]')
        self.assertEquals(web_element.text, app_name, "App creation failed")
        app_ids = team.get_id_from_app_name(browser=self.browser, app_name=app_name)
        team.delete_app_given_ids(browser=self.browser, app_ids=app_ids)


    @attr(genre="register-application")
    def test_register_new_app_default_check_table_content_crash_data(self):
        __name__ + """ [Test] Content of the crash data """
        
        self.browser.get(page_url)
        table = self.browser.find_element_by_xpath('//*[contains(text(),"View Crash Data")]/..')
        count = table.find_elements_by_xpath("./*[@class='disabled']")
        self.assertEquals(count.__len__(), 2, "Expecting Disabled found Enabled")


    @attr(genre='register-application')
    def test_register_new_app_with_default_parameters_html5(self):
        __name__ + """ [Test] Registering a new html5 app """

        app_name = "HTML5-" + str(random.random())
        self.browser.find_element_by_id("app-name").send_keys(app_name)
        #self.browser.find_element_by_xpath('//*[@id="all-platforms"]/label[3]').click()
        self.assertFalse(utils.find_element_and_click(self.browser, By.XPATH, '//*[@id="all-platforms"]/label[3]'),
                                 " Broken link at " + self.browser.current_url)

        self.assertFalse(utils.find_element_and_submit(self.browser, By.ID, BrowserConstants.COMMIT),
                                 " Broken link at " + self.browser.current_url)
        web_element = self.browser.find_element_by_xpath(
            '//*[@id="app-table"]/tbody/*/td[2]/a[contains(text(),"' + app_name + '")]')
        self.assertEquals(web_element.text, app_name, "App creation failed")
        app_ids = team.get_id_from_app_name(browser=self.browser, app_name=app_name)
        team.delete_app_given_ids(browser=self.browser, app_ids=app_ids)


    @attr(genre='register-application')
    def test_register_new_app_with_default_parameters_win8(self):
        __name__ + """ [Test] Registering a new win8 application """

        app_name = "Win8-" + str(random.random())
        self.browser.find_element_by_id("app-name").send_keys(app_name)
        #self.browser.find_element_by_xpath('//*[@id="all-platforms"]/label[4]').click()
        self.assertFalse(utils.find_element_and_click(self.browser, By.XPATH, '//*[@id="all-platforms"]/label[4]'),
                                 " Broken link at " + self.browser.current_url)

        #self.browser.find_element_by_id("commit").click()
        self.assertFalse(utils.find_element_and_submit(self.browser, By.ID, BrowserConstants.COMMIT),
                                 " Broken link at " + self.browser.current_url)
        web_element = self.browser.find_element_by_xpath(
            '//*[@id="app-table"]/tbody/*/td[2]/a[contains(text(),"' + app_name + '")]')
        self.assertEquals(web_element.text, app_name, "App creation failed")
        app_ids = team.get_id_from_app_name(browser=self.browser, app_name=app_name)
        team.delete_app_given_ids(browser=self.browser, app_ids=app_ids)

    @attr(genre='register-application')
    def test_register_new_app_with_ios_invite_members(self):
        __name__ + """ [Test] Registering a new IOS app with invitation to users """

        app_name = "register-with-invite-" + str(random.random())
        self.browser.find_element_by_id("app-name").send_keys(app_name)
        #Inviting collabotor
        self.browser.find_element_by_id("team_members").send_keys(self.config.login.test_user_admin)
        self.assertFalse(utils.find_element_and_submit(self.browser, By.ID, BrowserConstants.COMMIT),
                                 " Broken link at " + self.browser.current_url)
        web_element = self.browser.find_element_by_xpath(
            '//*[@id="app-table"]/tbody/*/td[2]/a[contains(text(),"' + app_name + '")]')
        self.assertEquals(web_element.text, app_name, "App creation failed")
        app_ids = team.get_id_from_app_name(browser=self.browser, app_name=app_name)
        team.delete_app_given_ids(browser=self.browser, app_ids=app_ids)

    @attr(genre='register-application', smoke1=True)
    def test_delete_all_app(self):
        __name__ + """ [Test] Deleting all the IOS- test apps """

        app_ids = team.get_id_from_app_name(browser=self.browser, app_name="IOS-")
        self.assertEquals(True, team.delete_app_given_ids(browser=self.browser, app_ids=app_ids),
                          "Deleting App failed")

    @attr(genre='register-application')
    #@unittest.skip("Because og Bug https://crittercism.atlassian.net/browse/PP-1159")
    def test_privacy_link(self):
        __name__ + """ [Test] Verify privacy link while Registering a new app """

        privacy_link = config.CliConfig().common.url + "/privacy.html"
        self.assertFalse(utils.is_url_broken(browser=self.browser,link=privacy_link), " Broken link at " + privacy_link)

    @attr(genre='register-application')
    #@unittest.skip("Because og Bug https://crittercism.atlassian.net/browse/PP-1159")
    def test_tos_link(self):
        __name__ + """ [Test] Verify privacy link while Registering a new app """

        tos_link = config.CliConfig().common.url + "/tos-v3.html"
        self.assertFalse(utils.is_url_broken(browser=self.browser,link=tos_link), " Broken link at " + tos_link)

if __name__ == '__main__':
    unittest.main(verbosity=2)
