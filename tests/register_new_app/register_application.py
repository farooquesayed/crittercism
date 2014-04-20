import random
from selenium.webdriver.support.wait import WebDriverWait
import unittest2 as unittest
from nose.plugins.attrib import attr
from src import baseTest
from src import logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0


__author__ = 'farooque'

mylogger = logger.setup_custom_logger(__name__)

class RegisterApplication(baseTest.SeleniumTestCase):

    @classmethod
    def setUpClass(self):
        super(RegisterApplication, self).setUpClass()

    def setUp(self):
        page_url = "https://app.crittercism.com/developers/register_application"
        self.browser.get(page_url)

    @attr(genre='register_application')
    def test_verify_new_app_page_default_parameter_platform(self):
        __name__ + "[Test] Verifing default option platform on New App register page"
        platform_checked = self.browser.find_element_by_id("platform-ios").get_attribute("value")
        self.assertEquals(platform_checked,"1", "Default platform should be IOS")

    @attr(genre='register_application')
    def test_verify_new_app_page_default_parameter_employee_facing(self):
        __name__ + "[Test] Verifing default employee facing option on New App register page"
        no_button = self.browser.find_element_by_xpath("//*[@for='is_internal_app_no']").get_attribute("aria-pressed")
        self.assertEquals(no_button,"true","Default App should be internal")

    @attr(genre='register_application')
    def test_verify_new_app_page_default_parameter_in_app_store(self):
        __name__ + "[Test] Verifing default in appstore option on New App register page"
        no_button = self.browser.find_element_by_xpath("//*[@for='in_app_store_no']").get_attribute("aria-pressed")
        self.assertEquals(no_button,"true","Default App should be in app-store")

    @attr(genre='register_application')
    def test_verify_new_app_page_default_permission(self):
        __name__ + "[Test] Verifing default in permission on New App register page"

        table = self.browser.find_element_by_xpath('//*[contains(text(),"Change Settings")]/..')
        count = table.find_elements_by_xpath ("./*[@class='disabled']")
        self.assertEquals(count.__len__(),2,"Only Admin should be checked")


    @attr(genre='register_application')
    def test_register_new_app_with_default_parameters_ios(self):
        __name__ + """[Test] Registering a new parameters """

        app_name = "IOS-" + str(random.random())
        self.browser.find_element_by_id("app-name").send_keys(app_name)
        self.browser.find_element_by_id("commit").click()
        web_element = self.browser.find_element_by_xpath('//*[@id="app-table"]/tbody/*/td[2]/a[contains(text(),"' + app_name + '")]')
        self.assertEquals(web_element.text, app_name, "App creation failed")


    @attr(genre='register_application')
    def test_register_new_app_with_default_parameters_android(self):
        __name__ + """[Test] Registering a new parameters """

        app_name = "Android-" + str(random.random())
        self.browser.find_element_by_id("app-name").send_keys(app_name)
        self.browser.find_element_by_xpath('//*[@id="all-platforms"]/label[2]').click()
        self.browser.find_element_by_id("commit").click()
        web_element = self.browser.find_element_by_xpath('//*[@id="app-table"]/tbody/*/td[2]/a[contains(text(),"' + app_name + '")]')
        self.assertEquals(web_element.text, app_name, "App creation failed")

    @attr(genre='register_application')
    def test_register_new_app_with_default_parameters_html5(self):
        __name__ + """[Test] Registering a new parameters """

        app_name = "HTML5-" + str(random.random())
        self.browser.find_element_by_id("app-name").send_keys(app_name)
        self.browser.find_element_by_xpath('//*[@id="all-platforms"]/label[3]').click()
        self.browser.find_element_by_id("commit").click()
        web_element = self.browser.find_element_by_xpath('//*[@id="app-table"]/tbody/*/td[2]/a[contains(text(),"' + app_name + '")]')
        self.assertEquals(web_element.text, app_name, "App creation failed")

    @attr(genre='register_application')
    def test_register_new_app_with_default_parameters_win8(self):
        __name__ + """[Test] Registering a new parameters """

        app_name = "HTML5-" + str(random.random())
        self.browser.find_element_by_id("app-name").send_keys(app_name)
        self.browser.find_element_by_xpath('//*[@id="all-platforms"]/label[4]').click()
        self.browser.find_element_by_id("commit").click()
        web_element = self.browser.find_element_by_xpath('//*[@id="app-table"]/tbody/*/td[2]/a[contains(text(),"' + app_name + '")]')
        self.assertEquals(web_element.text, app_name, "App creation failed")

    @attr(genre='register_application', smoke=True)
    def test_delete_all_app(self):
        __name__ + """[Test] Registering a new parameters """

        self.browser.get("https://app.crittercism.com/developers")

        table = self.browser.find_element_by_id("app-table")

        app_list = table.find_elements_by_xpath('//*[@id="app-table"]/tbody/*/td[2]/a[contains(text(),"App-")]')
        app_ids = []
        for app in app_list:
            id = app.get_attribute("href").split('/')
            app_ids.append(id[id.__len__() - 1 ])

        for app_id in app_ids:
            url = self.config.common.url + '/app-settings/' + app_id + '#delete-app'
            self.browser.get( url )
            self.browser.find_element_by_id('delete-app-' + app_id).click()
            alert = self.browser.switch_to_alert()
            alert.accept()


    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        mylogger.info("Finished teardownClass RegisterApplication")
        pass
    if __name__ == '__main__':
        unittest.main(verbosity=2)
