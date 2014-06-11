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
from src.page_helpers import crash
from src import config

__author__ = 'egeller'

logger = clogger.setup_custom_logger(__name__)
now = datetime.datetime.now()


class CrashDetailsTestSuite(baseTest.CrittercismTestCase):
    app_ids = []
    crash_names = []
    crash_statuses = []
    crash_first_occurred = []

    @classmethod
    def setUpClass(cls):
        """


        """
        super(CrashDetailsTestSuite, cls).setUpClass()
        CrashDetailsTestSuite.app_ids = team.get_id_from_app_name(browser=cls.browser,
                                                                  app_name=config.CliConfig().apps.android_with_data)

    def setUp(self):
        """
            Setup for the testcase


        """
        self.browser.get(self.config.common.url + "/developers/crash-summary/" + CrashDetailsTestSuite.app_ids[0])
        self.crash_names.append(self.get_web_element(By.XPATH,
                                                     value='//tbody/tr[1]/td[contains(@class, "title")]/a/span[@class="name"]').text)
        self.crash_statuses.append(self.get_web_element(By.XPATH,
                                                        value='//tbody/tr[1]/td[contains(@class, "title")]/a/span[@class="tag"]').text)
        self.crash_first_occurred.append(
            self.get_web_element(
                value='//tbody/tr[1]/td[3]/span[1]').text +
            self.get_web_element(
                value='//tbody/tr[1]/td[3]/span[1]').text
        )
        crash.goto_crash(suite=self, app_id= self.app_ids[0], idx=0)
        pass

    # ####TOP PANEL######
    @nose.plugins.attrib.attr(genre="crash-details")
    def test_1_title_box_elements(self):
        """
            Check title box of test elements
        """
        ###TIMELINE###
        with self.multiple_assertions():
            self.assertEqual(self.get_web_element(value='//h3[@id="title-text"]').text, self.crash_names[0],
                             msg="Crash Title didn't load properly")
            self.assertEqual(self.get_web_element(value='//div[@class="grid_50"]//span[@class="float-left"]').text,
                             "Number of Occurrences",
                             msg="'Number of Occurrences' header did not load properly")
            self.assertEqual(self.get_web_element(value='//a[@data-tab-top-link="timeline"]').text, "Timeline",
                             msg="'Timeline' button did not load properly")
            self.assertEqual(self.get_web_element(value='//a[@data-tab-top-link="world-map"]').text, "World Map",
                             msg="'World Map' button did not load properly")
            self.assertEqual(self.get_web_element(value='//*[@data-is-crash="True"]/div[1]/div[1]').text,
                             "Total Occurrences",
                             msg="'Total Occurrences' title did not load properly")
            self.assertNotEqual(self.get_web_element(value='//*[@data-is-crash="True"]/div[1]/div[2]/span').text, "",
                                msg="Number of Total Occurences failed to show up")
            self.assertEqual(self.get_web_element(value='//*[@data-is-crash="True"]/div[2]/div[1]').text,
                             "Total Affected Users",
                             msg="'Total Affected Users' title failed to show up")
            self.assertEqual(self.get_web_element(value='//*[@data-is-crash="True"]/div[2]/div[2]/span').text, "1500",
                             msg="Number of Total Affected Users failed to show up")

    @nose.plugins.attrib.attr(genre="crash-details")
    def test_2_post_crash_note(self):
        """
            Ensure that a note can be posted on crash details
        """
        note = crash.post_team_note(suite=self, app_id=CrashDetailsTestSuite.app_ids[0])
        with self.multiple_assertions():
            most_recent_note_path = '//*[@id="previous-notes"]/div[@class="note-mine"][1]'

            self.assertEqual(
                self.get_web_element(
                    value=most_recent_note_path + '/div[@class="note-content"]').text,
                note,
                msg="most recent note's content does not match the posted note!")

            self.assertEqual(
                self.get_web_element(
                    value=most_recent_note_path + '/div[@class="name"]').text[:18],
                'Nellian Solaiappan',
                msg="most recent note's author does not match the posted note!")

            ###Last Occurred, Current Status,