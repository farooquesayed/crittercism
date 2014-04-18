import unittest2 as unittest
from nose.plugins.attrib import attr
from src import baseTest
from src.baseTest import logger

__author__ = 'farooque'

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

    @attr(genre='register_application', smoke='TRUE')
    def test_register_new_app_with_default_parameters(self):
        __name__ + """[Test] Registering a new parameters """
        self.browser.find_element_by_id("app-name").send_keys("auto-1")
        self.browser.find_element_by_id("commit").click()


    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        logger.info("Finished teardownClass RegisterApplication")
        pass
    if __name__ == '__main__':
        unittest.main(verbosity=2)
