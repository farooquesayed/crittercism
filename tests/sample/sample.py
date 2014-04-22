from logging import config
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.safari.webdriver import WebDriver
import unittest2 as unittest


from nose.plugins.attrib import attr
from src import  clogger
from src import baseTest

from src.data_driven_test_wrapper import ddt_list, data, data_driven_test


logger = clogger.setup_custom_logger(__name__)

def generate_list_of_data():
    row_list = []
    row_list.append(1)
    row_list.append(2)
    row_list.append(3)
    row_list.append(4)
    return row_list


@data_driven_test
class SampleTestSuite(baseTest.SeleniumTestCase):

    @classmethod
    def setUpClass(self):
        super(SampleTestSuite, self).setUpClass()

    def setUp(self):
        #Can override the base class setUp here
        pass


    @attr(genre='sample')
    @unittest.skip("Reason : why it is skipped")
    def test_sample(self):
        __name__ + """[Test] test_quick_check """
        with self.multiple_assertions():
            self.assertEquals(0,1,"Continue on assert")
            self.assertEquals(0,1,"Continue on assert again")
            pass

    def test_login(self):
        url = "https://www.irctc.co.in/"

        #======= login to portal =========
        self.browser.get(url)
        self.browser.find_element_by_name('userName').send_keys("nasirhere")
        self.browser.find_element_by_name('password').send_keys("123456")
        self.browser.find_element_by_name('button').submit()

        self.browser.find_element_by_name('stationFrom').send_keys("MUMBAI CST (CSTM)" + Keys.RETURN)
        self.browser.find_element_by_name('stationTo').send_keys("AJMER JN (AII)" + Keys.RETURN)
        self.browser.find_element_by_xpath('//*[@value="Find Trains"]').submit()




    @attr(genre="ddt")
    @data(generate_list_of_data())
    @ddt_list
    #@unpack
    def test_data_driven_test(self, value):
        __name__ + " Data driven test example"

        self.assertGreater(value,1,"Argument didn't matched")

    @attr(genre="ma")
    def test_multiple_assertion(self):
        __name__ + " Multiple Assertion example"
        with self.multiple_assertions():
            self.assertEquals(1,0, "Continue on Failure")
            self.assertEquals(1,0, "Continue on Failure")
            self.assertEquals(1,0, "Continue on Failure")

    def tearDown(self):
        #Can override the base class setUp here
        pass


    @classmethod
    def tearDownClass(self):
        super(SampleTestSuite, self).tearDownClass()
        logger.info("Finished executing SampleTestSuite")
        pass
