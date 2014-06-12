import re
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
from src import config


__author__ = 'egeller'

logger = clogger.setup_custom_logger(__name__)


class AlertTestSuite(baseTest.CrittercismTestCase):
    app_ids = []

    @classmethod
    def setUpClass(cls):
        """


        """
        super(AlertTestSuite, cls).setUpClass()
        app_name = config.CliConfig().apps.android_with_data
        cls.app_ids.append(team.get_id_from_app_name(cls.browser, app_name)[0])


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

        alert_list = alert_mgmt.create_new_alert(self, app_id=self.app_ids[0], alert_type=alert_type,
                                                 threshold=threshold)
        alert_name = alert_list[0]
        threshold = alert_list[1]
        #self.setUp()

        alert_detail = '(//div[@class="span10 detail"])[1]'

        with self.multiple_assertions():
            bold_elements = alert_detail + '//span[@class="bold"]['
            pattern = re.compile('[^\d|^\.]+')
            self.assertEqual(self.get_web_element(value= bold_elements + '1' + ']').text, alert_name,
                             msg="alert_type was not properly displayed!")
            self.assertEqual(
                pattern.sub('', self.get_web_element(value= bold_elements + '2' + ']').text),
                str(threshold),
                             msg="threshold was not properly displayed!")
            self.assertEqual(self.get_web_element(value= bold_elements + '7' + ']').text, "Nellian Solaiappan",
                             msg="alert assignee was not properly displayed!")
        alert_mgmt.delete_alert(self, app_id=self.app_ids[0], idx=0)

    #TODO: test Alert Integrations

    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        super(AlertTestSuite, cls).tearDownClass()

        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)