import unittest
import time
import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys as keys
import nose.plugins.attrib

from src import clogger
from src import baseTest
import src.constants as constants
from src.page_helpers import team
from src.page_helpers import utils

__author__ = 'egeller'

logger = clogger.setup_custom_logger(__name__)
now = datetime.datetime.now()

class CrashDetailsTestSuite(baseTest.CrittercismTestCase):
    app_ids= []
    crash_name = []
    crash_status = []
    crash_first_occurred = []

    @classmethod
    def setUpClass(cls):
        """


        """
        super(CrashDetailsTestSuite, cls).setUpClass()
        CrashDetailsTestSuite.app_ids = team.get_id_from_app_name(browser=cls.browser, app_name="Cactii crash 'em high")

    def setUp(self):
        """
            Setup for the testcase


        """
        self.browser.get(self.config.common.url + "/developers/crash-summary/" + CrashDetailsTestSuite.app_ids[0])
        self.crash_name.append(self.get_web_element(By.XPATH, value='//tbody/tr[1]/td[@class="title "]/a/span[@class="name"]').text)
        self.crash_status.append(self.get_web_element(By.XPATH, value='//tbody/tr[1]/td[@class="title "]/a/span[@class="tag"]').text)
        self.crash_first_occurred.append(self.get_web_element(value=''))
        self.find_element_and_click(
            value='//a[@href="/developers/crash-details/f54c3b5bf255dcf6bd470ecab28f92a8d290717d5676e166fddbb516"]')
        pass

    #####TOP PANEL######
    @nose.plugins.attrib.attr(genre="crash-details")
    def test_1_title_box_elements(self):
        """
            Check title box of test elements
        """
        ###TIMELINE###
        with self.multiple_assertions():
            self.assertEqual(self.get_web_element(value='//h3[@id="title-text"]').text, self.crash_name[0],
                             msg="Crash Title didn't load properly")
            self.assertEqual(self.get_web_element(value='//div[@class="grid_50"]//span[@class="float-left"]').text, "Number of Occurrences",
                             msg="'Number of Occurrences' header did not load properly")
            self.assertEqual(self.get_web_element(value='//a[@data-tab-top-link="timeline"]').text, "Timeline",
                             msg="'Timeline' button did not load properly")
            self.assertEqual(self.get_web_element(value='//a[@data-tab-top-link="world-map"]').text, "World Map",
                             msg="'World Map' button did not load properly")
            self.assertEqual(self.get_web_element(value='//*[@data-is-crash="True"]/div[1]/div[1]').text, "Total Occurrences",
                             msg="'Total Occurrences' title did not load properly")
            self.assertNotEqual(self.get_web_element(value='//*[@data-is-crash="True"]/div[1]/div[2]/span').text, "",
                                msg="Number of Total Occurences failed to show up")
            self.assertEqual(self.get_web_element(value='//*[@data-is-crash="True"]/div[2]/div[1]').text, "Total Affected Users",
                                msg="'Total Affected Users' title failed to show up")
            self.assertEqual(self.get_web_element(value='//*[@data-is-crash="True"]/div[2]/div[2]/span').text, "1500",
                                msg="Number of Total Affected Users failed to show up")
        ###Last Occurred, Current Status,



