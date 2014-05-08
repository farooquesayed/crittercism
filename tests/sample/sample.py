from datetime import time

import selenium.webdriver.common.keys
import unittest2 as unittest
import nose.plugins.attrib

import src
from src import baseTest
from src.data_driven_test_wrapper import ddt_list, data, data_driven_test


logger = src.clogger.setup_custom_logger(__name__)


def generate_list_of_data():
    """



    :rtype : object
    :return:
    """
    row_list = []
    row_list.append(1)
    row_list.append(2)
    row_list.append(3)
    row_list.append(4)
    return row_list


@data_driven_test
class SampleTestSuite(baseTest.SeleniumTestCase):
    @classmethod
    def setUpClass(cls):
        """


        """
        super(SampleTestSuite, cls).setUpClass()

    def setUp(self):
        """
        Setup for the testcase


        """
        pass


    @nose.plugins.attrib.attr(genre='sample')
    @unittest.skip("Reason : why it is skipped")
    def test_sample(self):
        """
            1) Sample to test multiple assertion

        """
        __name__ + """[Test] test_quick_check """
        with self.multiple_assertions():
            self.assertEquals(0, 1, "Continue on assert")
            self.assertEquals(0, 1, "Continue on assert again")
            pass

    @nose.plugins.attrib.attr(genre='sample')
    @unittest.skip("Reason : why it is skipped")
    def test_login(self):
        """
        1) Sample for Skip

        """
        url = "https://www.irctc.co.in/"

        #======= login to portal =========
        self.browser.get(url)
        self.browser.find_element_by_name('userName').send_keys("nasirhere")
        self.browser.find_element_by_name('password').send_keys("123456")
        self.browser.find_element_by_name('button').submit()

        self.browser.find_element_by_name('stationFrom').send_keys(
            "MUMBAI CST (CSTM)" + selenium.webdriver.common.keys.Keys.RETURN)
        self.browser.find_element_by_name('stationTo').send_keys(
            "AJMER JN (AII)" + selenium.webdriver.common.keys.Keys.RETURN)
        self.browser.find_element_by_xpath('//*[@value="Find Trains"]').submit()


    @nose.plugins.attrib.attr(sample=True, genre="sample")
    @data(generate_list_of_data())
    @ddt_list
    #@unpack
    def test_data_driven_test(self, value):
        """
        1) Example test for data driven test
        2) Data are coming the generate_list_of_data methods
        :param value:
            generated from the functions
        """
        __name__ + " Data driven test example"

        self.assertGreater(value, 0, "Argument didn't matched")

    @nose.plugins.attrib.attr(sample=True)
    def test_switch_between_windows(self):
        self.wait_for_email()
        for handle in self.browser.window_handles:
            self.browser.switch_to_window(handle)

        self.browser.find_element_by_id('email').send_keys(self.config.login.test_user_engg)
        self.browser.find_element_by_name('password').send_keys(self.config.login.password)
        self.browser.find_element_by_id('commit').submit()

        with self.multiple_assertions():
            self.assertIn ("developers/app-settings/", self.browser.current_url, "Not able to redirect to App-Setting page")
            self.assertEqual(self.browser.find_element_by_name("name").get_attribute("value"), app_name, "Not able to see the correct App name")

    def tearDown(self):

        """
        Can override the base class setUp here
        Cleanup code for every testcase

        """
        pass


    @classmethod
    def tearDownClass(cls):
        """
        Cleanup code for the entire class

        """
        super(SampleTestSuite, cls).tearDownClass()
        logger.info("Finished executing SampleTestSuite")
        pass

    def wait_for_email(self):
        counter = 0
        self.browser.get("https://mail.yahoo.com")
        self.browser.find_element_by_id("username").send_keys(self.config.login.test_user_engg)
        self.browser.find_element_by_id("passwd").send_keys(self.config.login.password)
        self.browser.find_element_by_id(".save").click()
        app_name = "IOS-0.292169889366"
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

if __name__ == '__main__':
    unittest.main(verbosity=2)
