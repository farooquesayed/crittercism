from logging import config
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.safari.webdriver import WebDriver
import unittest2 as unittest


#from nose.tools import with_setup
from nose.plugins.attrib import attr
from src import  clogger
from src import baseTest

#from src.data_driven_test_wrapper import ddt_list, data, data_driven_test

from ddt import ddt, data, file_data, unpack



logger = clogger.setup_custom_logger(__name__)

def generate_list_of_data():
    row_list = [1,2,3]
    return row_list


@ddt
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
    @data(1,2,3,4)
    # @ddt_list
    def test_larger_than_two(self, value):
        self.assertEquals(1,value,"Argument didn't matched")

    def tearDown(self):
        #Can override the base class setUp here
        pass


    @classmethod
    def tearDownClass(self):
        super(SampleTestSuite, self).tearDownClass()
        logger.info("Finished executing SampleTestSuite")
        pass
