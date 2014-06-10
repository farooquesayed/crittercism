import unittest
import os
import threading
import time
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys as keys
import nose.plugins.attrib

from src import clogger
from src import baseTest
from src.constants import ALERT_TYPES
from src.page_helpers import team
from src.page_helpers import utils
from src.page_helpers import alert_mgmt


__author__ = 'egeller'

logger = clogger.setup_custom_logger(__name__)

class AlertTestSuite(baseTest.CrittercismTestCase):
    app_ids = []

    @classmethod
    def setUpClass(cls):
        """


        """
        super(AlertTestSuite, cls).setUpClass()
        cls.app_ids.append(team.get_id_from_app_name(cls.browser, "Cactii crash 'em high")[0])


    def setUp(self):
        """
            Setup for the testcase


        """
        self.browser.get(self.config.common.url + "/developers/alerts/" + self.app_ids[0])
        pass


    @nose.plugins.attrib.attr(genre="alerts")
    def test_1_create_alert(self):
        """
            1) Test a generic alert creation
        """

        threshold = random.randint(1, 9999)

        alert_type = random.randint(0, 11)

        alert_name = alert_mgmt.create_new_alert(self, app_id=self.app_ids[0], alert_type=alert_type, threshold=threshold)

        self.setUp()

        alert_detail = self.get_web_element(value='(//div[@class="span10 detail"])[1]')

        with self.multiple_assertions():
            bold_elements = '(/span[@class="bold"])['
            self.assertEqual(alert_detail.find_element_by_xpath(bold_elements + 1 + ']').text, alert_name,
                             msg="alert_type was not properly displayed!")
            self.assertEqual(alert_detail.find_element_by_xpath(bold_elements + 2 + ']').text, str(threshold),
                                                                msg="threshold was not properly displayed!")
            self.assertEqual(alert_detail.find_element_by_xpath(bold_elements + 7 + ']').text, "Nellian Solaiappan",
                             msg="alert assignee was not properly displayed!")




    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):

        super(AlertTestSuite, cls).tearDownClass()

        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)