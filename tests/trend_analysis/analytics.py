from datetime import time
import inspect
from selenium.webdriver.common.by import By

import random
import selenium.webdriver.common.keys
import unittest2 as unittest
import nose.plugins.attrib

import src
from src import baseTest
from src.page_helpers import team
from src.data_driven_test_wrapper import ddt_list, data, data_driven_test
from src.page_helpers import utils

__author__ = 'ethan'

logger = src.clogger.setup_custom_logger(__name__)

def generate_list_of_crash_types():
    """



    :rtype : object
    :return:
    """
    crash_types = []
    crash_types.append("all")
    crash_types.append("resolved")
    crash_types.append("known")
    crash_types.append("unresolved")
    return crash_types

class AnalyticsTestSuite(baseTest.CrittercismTestCase):
    app_ids= []

    @classmethod
    def setUpClass(cls):
        """


        """
        super(AnalyticsTestSuite, cls).setUpClass()
        #cls.browser.get(cls.config.common.url + "/developers/analytics/52fb0fdb8b2e3365c6000008")
        AnalyticsTestSuite.app_ids = team.get_id_from_app_name(browser=cls.browser, app_name="Crittercism Demo")

    def setUp(self):
        """
        Setup for the testcase


        """
        self.browser.get(self.config.common.url + "/developers/analytics/" + AnalyticsTestSuite.app_ids[0])
        pass


    @nose.plugins.attrib.attr(genre='analytics')
    #@unittest.skip("Reason : why it is skipped")
    def test_au_text(self):
        """
            1) ensures that Today's DAU and MAU have been returned successfully

        """
        __name__ + """[Test] test that DAU is returned below graph"""
        empty_string = ""
        #data is a dummy string that will later be replaced with actual data
        with self.multiple_assertions():
            self.assertNotEqual(first= utils.get_web_element(browser=self.browser, value="/html/body/div[3]/div/div[2]/div/div[3]/span").text,
                                second=empty_string,
                                msg="DAU result does not appear")
            self.assertNotEqual(first= utils.get_web_element(browser=self.browser, value="/html/body/div[3]/div/div[3]/div/div[3]/span").text,
                                second=empty_string,
                                msg="MAU result does not appear")

            pass

    @nose.plugins.attrib.attr(genre='analytics')
    def test_todays_apploads_crashes(self):
        """
            2) tests list of crashes vs application loads by version
        """
        versions = []
        versions.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div/div/div/div[2]/div[2]/strong").text)
        versions.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div/div/div/div[2]/div[3]/strong").text)

        crashes = []
        crashes.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div/div/div/div[2]/div[2]/span").text)
        crashes.append(utils.get_web_element(browser=self.browser,

                                         value="/html/body/div[3]/div/div[4]/div/div/div/div[2]/div[3]/span").text)
        crash_table = dict(zip(versions, crashes))
        blank_data = {"1.0.0.0":"0.0%",
                      "0.4.2":"7.23%"}

        self.assertTrue(crash_table == blank_data, "Listed apploads data does not match given data")


    @nose.plugins.attrib.attr(genre='analytics')
    def test_todays_dau_crashes(self):
        """
            3) tests list of crashes vs DAU by version
        """
        versions = []
        versions.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div/div[2]/div/div[2]/div[2]/strong").text)
        versions.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div/div[2]/div/div[2]/div[3]/strong").text)

        crashes = []
        crashes.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div/div[2]/div/div[2]/div[2]/span").text)
        crashes.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div/div[2]/div/div[2]/div[3]/span").text)
        crash_table = dict(zip(versions, crashes))
        blank_data = {"1.0.0.0":"0%",
                      "0.4.2":"62%"}

        self.assertEqual(crash_table, blank_data, "Daily Active Users that crashed by version does not match given data")

    @nose.plugins.attrib.attr(genre='analytics')
    def test_todays_apploads(self):
        """
            4) tests list of app loads by version
        """
        versions = []
        versions.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div[2]/div/div/div[2]/div[2]/strong").text)
        versions.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div[2]/div/div/div[2]/div[3]/strong").text)

        crashes = []
        crashes.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div[2]/div/div/div[2]/div[2]/span").text)
        crashes.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div[2]/div/div/div[2]/div[3]/span").text)
        crash_table = dict(zip(versions, crashes))

        blank_data = {"1.0.0.0":"89",
                      "0.4.2":"5090"}


        self.assertEqual(crash_table, blank_data, "App loads by version does not match given data")

    @nose.plugins.attrib.attr(genre='analytics')
    def test_todays_dau(self):
        """
            5) tests list of daily active users by version
        """
        versions = []
        versions.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div[2]/div[2]/div/div[2]/div[2]/strong").text)
        versions.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div[2]/div[2]/div/div[2]/div[3]/strong").text)

        crashes = []
        crashes.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div[2]/div[2]/div/div[2]/div[2]/span").text)
        crashes.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div[2]/div[2]/div/div[2]/div[3]/span").text)
        crash_table = dict(zip(versions, crashes))
        blank_data = {"1.0.0.0":"0",
                      "0.4.2":"0"}

        self.assertEqual(crash_table, blank_data, "Daily Active Users by version does not match given data")

    @nose.plugins.attrib.attr(genre='analytics')
    def test_todays_crashes(self):
        """
            6) tests list of crashes by version
        """
        versions = []
        versions.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div[3]/div/div/div[2]/div[2]/strong").text)
        versions.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div[3]/div/div/div[2]/div[3]/strong").text)

        crashes = []
        crashes.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div[3]/div/div/div[2]/div[2]/span").text)
        crashes.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div[3]/div/div/div[2]/div[3]/span").text)
        crash_table = dict(zip(versions, crashes))
        blank_data = {"1.0.0.0":"0",
                      "0.4.2":"0"}
        self.assertEqual(crash_table, blank_data, "Crashes by version does not match given data")

    @nose.plugins.attrib.attr(genre='analytics')
    def test_todays_affected_users(self):
        """
            7) tests list of users affected by at least one crash by version
        """
        versions = []
        versions.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div[3]/div[2]/div/div[2]/div[2]/strong").text)
        versions.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div[3]/div[2]/div/div[2]/div[3]/strong").text)

        crashes = []
        crashes.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div[3]/div[2]/div/div[2]/div[2]/span").text)
        crashes.append(utils.get_web_element(browser=self.browser,
                                         value="/html/body/div[3]/div/div[4]/div[3]/div[2]/div/div[2]/div[3]/span").text)
        crash_table = dict(zip(versions, crashes))
        blank_data = {"1.0.0.0":"0",
                      "0.4.2":"62"}

        self.assertEqual(crash_table, blank_data, "Affected users by version does not match given data")


    def tearDown(self):
       pass


    @classmethod
    def tearDownClass(cls):
        super(AnalyticsTestSuite, cls).tearDownClass()
        logger.info("Finished executing AnalyticsTestSuite")
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
