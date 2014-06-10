import unittest2 as unittest
import nose.plugins.attrib

from src import clogger
from src import baseTest
from src.page_helpers import team
from src import config


__author__ = 'ethan'

logger = clogger.setup_custom_logger(__name__)


class AnalyticsTestSuite(baseTest.CrittercismTestCase):
    app_ids = []

    @classmethod
    def setUpClass(cls):
        """


        """
        super(AnalyticsTestSuite, cls).setUpClass()
        #cls.browser.get(cls.config.common.url + "/developers/analytics/52fb0fdb8b2e3365c6000008")
        AnalyticsTestSuite.app_ids = team.get_id_from_app_name(browser=cls.browser, app_name= config.CliConfig().apps.android_with_data)

    def setUp(self):
        """
        Setup for the testcase


        """
        self.browser.get(self.config.common.url + "/developers/analytics/" + AnalyticsTestSuite.app_ids[0])
        pass


    @nose.plugins.attrib.attr(genre='analytics')
    #@unittest.skip("Reason : why it is skipped")
    def test_1_au_version(self):
        """
            1) Today's DAU and MAU

        """
        __name__ + """[Test] test that DAU is returned below graph"""
        empty_string = ""
        #data is a dummy string that will later be replaced with actual data
        with self.multiple_assertions():
            self.assertNotEqual(first=self.get_web_element(value='//*[@id="dau-container"]/../div[3]/strong').text,
                                second=empty_string,
                                msg="DAU result does not appear")
            self.assertNotEqual(first=self.get_web_element(value='//*[@id="dau-container"]/../div[3]/span').text,
                                second=empty_string,
                                msg="MAU result does not appear")

            pass

    ######### BY VERSION ############
    @nose.plugins.attrib.attr(genre='analytics')
    def test_2_todays_apploads_crashes_version(self):
        """
            2) crashes vs application loads by version
        """
        versions = []
        versions.append(self.get_web_element(
            value='//*[@id="crashes-ratio-container"]/../div[2]/div[2]/strong').text)
        #versions.append(self.get_web_element(
        #   value='//*[@id="crashes-ratio-container"]/../div[2]/div[3]/strong').text)

        crashes = []
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-ratio-container"]/../div[2]/div[2]/span').text)
        #crashes.append(self.get_web_element(
        #    value='//*[@id="crashes-ratio-container"]/../div[2]/div[3]/span').text)
        crash_table = dict(zip(versions, crashes))
        blank_data = {"1.0.0.0": "",
                      "0.4.2": ""}

        self.assertFalse(crash_table == blank_data, "Listed apploads data does not match given data")


    @nose.plugins.attrib.attr(genre='analytics')
    def test_3_todays_dau_crashes_version(self):
        """
            3) crashes vs DAU by version
        """
        versions = []
        versions.append(self.get_web_element(
            value='//*[@id="crashes-ratio-container"]/../div[2]/div[2]/strong').text)
        #versions.append(self.get_web_element(
        #    value='//*[@id="crashes-ratio-container"]/../div[2]/div[3]/strong').text)

        crashes = []
        crashes.append(self.get_web_element(
            value='//*[@id="affected-users-ratio-container"]/../div[2]/div[2]/span').text)
        #crashes.append(self.get_web_element(
        #    value='//*[@id="affected-users-ratio-container"]/../div[2]/div[3]/span').text)
        crash_table = dict(zip(versions, crashes))
        blank_data = {"1.0.0.0": "",
                      "0.4.2": ""}

        self.assertNotEqual(crash_table, blank_data,
                            "Daily Active Users that crashed by version does not match given data")

    @nose.plugins.attrib.attr(genre='analytics')
    def test_4_todays_apploads_version(self):
        """
            4) app loads by version
        """
        versions = []
        versions.append(self.get_web_element(
            value='//*[@id="app-load-version-container"]/../div[2]/div[2]/strong').text)
        #versions.append(self.get_web_element(
        #    value='//*[@id="app-load-version-container"]/../div[2]/div[3]/strong').text)

        crashes = []
        crashes.append(self.get_web_element(
            value='//*[@id="app-load-version-container"]/../div[2]/div[2]/span').text)
        #crashes.append(self.get_web_element(
        #    value='//*[@id="app-load-version-container"]/../div[2]/div[3]/span').text)
        crash_table = dict(zip(versions, crashes))

        blank_data = {"1.0.0.0": "",
                      "0.4.2": ""}

        self.assertNotEqual(crash_table, blank_data, "App loads by version does not match given data")

    @nose.plugins.attrib.attr(genre='analytics')
    def test_5_todays_dau_version(self):
        """
            5) daily active users by version
        """
        versions = []
        versions.append(self.get_web_element(
            value='//*[@id="dau-version-container"]/../div[2]/div[2]/strong').text)
        #versions.append(self.get_web_element(
        #    value='//*[@id="dau-version-container"]/../div[2]/div[3]/strong').text)

        crashes = []
        crashes.append(self.get_web_element(
            value='//*[@id="dau-version-container"]/../div[2]/div[2]/span').text)
        #crashes.append(self.get_web_element(
        #    value='//*[@id="dau-version-container"]/../div[2]/div[3]/span').text)
        crash_table = dict(zip(versions, crashes))
        blank_data = {"1.0.0.0": "",
                      "0.4.2": ""}

        self.assertNotEqual(crash_table, blank_data, "Daily Active Users by version does not match given data")

    @nose.plugins.attrib.attr(genre='analytics')
    def test_6_todays_crashes_version(self):
        """
            6) crashes by version
        """
        versions = []
        versions.append(self.get_web_element(
            value='//*[@id="crashes-version-container"]/../div[2]/div[2]/strong').text)
        #versions.append(self.get_web_element(
        #    value='//*[@id="crashes-version-container"]/../div[2]/div[3]/strong').text)

        crashes = []
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-version-container"]/../div[2]/div[2]/span').text)
        #crashes.append(self.get_web_element(
        #    value='//*[@id="crashes-version-container"]/../div[2]/div[3]/span').text)
        crash_table = dict(zip(versions, crashes))
        blank_data = {"1.0.0.0": "",
                      "0.4.2": ""}
        self.assertNotEqual(crash_table, blank_data, "Crashes by version does not match given data")

    @nose.plugins.attrib.attr(genre='analytics')
    def test_7_todays_affected_users_version(self):
        """
            7) users affected by at least one crash by version
        """
        versions = []
        versions.append(self.get_web_element(
            value='//*[@id="affected-users-version-container"]/../div[2]/div[2]/strong').text)
        #versions.append(self.get_web_element(
        #    value='//*[@id="affected-users-version-container"]/../div[2]/div[3]/strong').text)

        crashes = []
        crashes.append(self.get_web_element(
            value='//*[@id="affected-users-version-container"]/../div[2]/div[2]/span').text)
        #crashes.append(self.get_web_element(
        #    value='//*[@id="affected-users-version-container"]/../div[2]/div[2]/span').text)
        crash_table = dict(zip(versions, crashes))
        blank_data = {"1.0.0.0": "",
                      "0.4.2": ""}

        self.assertNotEqual(crash_table, blank_data, "Affected users by version does not match given data")

    ############ BY DEVICE ##############
    @nose.plugins.attrib.attr(genre='analytics')
    def test_8_todays_apploads_device(self):
        """
            8) App Loads by Device
        """
        versions = []
        versions.append(self.get_web_element(
            value='//*[@id="app-load-device-container"]/../div[2]/div[2]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="app-load-device-container"]/../div[2]/div[3]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="app-load-device-container"]/../div[2]/div[4]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="app-load-device-container"]/../div[2]/div[5]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="app-load-device-container"]/../div[2]/div[6]/strong').text)

        crashes = []
        crashes.append(self.get_web_element(
            value='//*[@id="app-load-device-container"]/../div[2]/div[2]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="app-load-device-container"]/../div[2]/div[3]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="app-load-device-container"]/../div[2]/div[4]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="app-load-device-container"]/../div[2]/div[5]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="app-load-device-container"]/../div[2]/div[6]/span').text)

        crash_table = dict(zip(versions, crashes))
        blank_data = {"iPhone 4s": "",
                      "iPhone 5 CDMA+LTE": "",
                      "iPhone 4 CDMA": "",
                      "2nd Gen iPad mini Retina, WiFi/Cellular": "",
                      "2nd Gen iPad mini Retina, WiFi": ""}

        self.assertNotEqual(crash_table, blank_data, "App loads by device does not match given data")

    @nose.plugins.attrib.attr(genre='analytics')
    def test_9_todays_crashes_device(self):
        """
            9) Crashes by Device
        """
        versions = []
        versions.append(self.get_web_element(
            value='//*[@id="crashes-device-container"]/../div[2]/div[2]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="crashes-device-container"]/../div[2]/div[3]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="crashes-device-container"]/../div[2]/div[4]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="crashes-device-container"]/../div[2]/div[5]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="crashes-device-container"]/../div[2]/div[6]/strong').text)

        crashes = []
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-device-container"]/../div[2]/div[2]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-device-container"]/../div[2]/div[3]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-device-container"]/../div[2]/div[4]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-device-container"]/../div[2]/div[5]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-device-container"]/../div[2]/div[6]/span').text)

        crash_table = dict(zip(versions, crashes))
        blank_data = {"iPhone 4s": "",
                      "iPhone 5 CDMA+LTE": "",
                      "iPhone 4 CDMA": "",
                      "2nd Gen iPad mini Retina, WiFi/Cellular": "",
                      "2nd Gen iPad mini Retina, WiFi": ""}

        self.assertNotEqual(crash_table, blank_data, "Crashes by device does not match given data")

    @nose.plugins.attrib.attr(genre='analytics')
    def test__10_todays_appload_crashes_device(self):
        """
            10) % of Apploads that Crashed by Device
        """
        versions = []
        versions.append(self.get_web_element(
            value='//*[@id="crashes-ratio-device-container"]/../div[2]/div[2]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="crashes-ratio-device-container"]/../div[2]/div[3]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="crashes-ratio-device-container"]/../div[2]/div[4]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="crashes-ratio-device-container"]/../div[2]/div[5]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="crashes-ratio-device-container"]/../div[2]/div[6]/strong').text)

        crashes = []
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-ratio-device-container"]/../div[2]/div[2]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-ratio-device-container"]/../div[2]/div[3]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-ratio-device-container"]/../div[2]/div[4]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-ratio-device-container"]/../div[2]/div[5]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-ratio-device-container"]/../div[2]/div[6]/span').text)

        crash_table = dict(zip(versions, crashes))
        blank_data = {"iPhone 4s": "",
                      "iPhone 5 CDMA+LTE": "",
                      "iPhone 4 CDMA": "",
                      "2nd Gen iPad mini Retina, WiFi/Cellular": "",
                      "2nd Gen iPad mini Retina, WiFi": ""}

        self.assertNotEqual(crash_table, blank_data, "Apploads that crashed by device does not match given data")

    ##############BREAKDOWN BY OS#######################
    @nose.plugins.attrib.attr(genre='analytics')
    def test__11_todays_apploads_os(self):
        """
            11) # of apploads by OS
        """
        versions = []
        versions.append(self.get_web_element(
            value='//*[@id="app-load-os-container"]/../div[2]/div[2]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="app-load-os-container"]/../div[2]/div[3]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="app-load-os-container"]/../div[2]/div[4]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="app-load-os-container"]/../div[2]/div[5]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="app-load-os-container"]/../div[2]/div[6]/strong').text)

        crashes = []
        crashes.append(self.get_web_element(
            value='//*[@id="app-load-os-container"]/../div[2]/div[2]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="app-load-os-container"]/../div[2]/div[3]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="app-load-os-container"]/../div[2]/div[4]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="app-load-os-container"]/../div[2]/div[5]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="app-load-os-container"]/../div[2]/div[6]/span').text)

        crash_table = dict(zip(versions, crashes))
        blank_data = {"ios 5.1.1": "",
                      "ios 4.2.1": "",
                      "6.1.4": "",
                      "6.1.5": "",
                      "7.0.1": ""}

        self.assertNotEqual(crash_table, blank_data, "Apploads by OS does not match given data")

    @nose.plugins.attrib.attr(genre='analytics')
    def test__12_todays_crashes_os(self):
        """
            12) # of crashes by OS
        """
        versions = []
        versions.append(self.get_web_element(
            value='//*[@id="crashes-os-container"]/../div[2]/div[2]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="crashes-os-container"]/../div[2]/div[3]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="crashes-os-container"]/../div[2]/div[4]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="crashes-os-container"]/../div[2]/div[5]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="crashes-os-container"]/../div[2]/div[6]/strong').text)

        crashes = []
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-os-container"]/../div[2]/div[2]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-os-container"]/../div[2]/div[3]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-os-container"]/../div[2]/div[4]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-os-container"]/../div[2]/div[5]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-os-container"]/../div[2]/div[6]/span').text)

        crash_table = dict(zip(versions, crashes))
        blank_data = {"ios 5.1.1": "",
                      "ios 4.2.1": "",
                      "6.1.4": "",
                      "6.1.5": "",
                      "7.0.1": ""}

        self.assertNotEqual(crash_table, blank_data, "crashes by OS does not match given data")

    @nose.plugins.attrib.attr(genre='analytics')
    def test__13_todays_appload_crashes_os(self):
        """
            13) % of apploads that crash by OS
        """
        versions = []
        versions.append(self.get_web_element(
            value='//*[@id="crashes-ratio-os-container"]/../div[2]/div[2]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="crashes-ratio-os-container"]/../div[2]/div[3]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="crashes-ratio-os-container"]/../div[2]/div[4]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="crashes-ratio-os-container"]/../div[2]/div[5]/strong').text)
        versions.append(self.get_web_element(
            value='//*[@id="crashes-ratio-os-container"]/../div[2]/div[6]/strong').text)

        crashes = []
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-ratio-os-container"]/../div[2]/div[2]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-ratio-os-container"]/../div[2]/div[3]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-ratio-os-container"]/../div[2]/div[4]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-ratio-os-container"]/../div[2]/div[5]/span').text)
        crashes.append(self.get_web_element(
            value='//*[@id="crashes-ratio-os-container"]/../div[2]/div[6]/span').text)

        crash_table = dict(zip(versions, crashes))
        blank_data = {"ios 5.1.1": "",
                      "ios 4.2.1": "",
                      "6.1.4": "",
                      "6.1.5": "",
                      "7.0.1": ""}

        self.assertNotEqual(crash_table, blank_data, "crashes by OS does not match given data")

    ###############TEST FILTER##################
    @nose.plugins.attrib.attr(genre='analytics')
    def test__14_date_filter(self):
        """
            14) test filters at top
        """

        fromPath = '//*[@id="date-from"]'
        toPath = '//*[@id="date-to"]'
        self.get_web_element(value=fromPath).send_keys("5/25/2014")
        self.get_web_element(value=toPath).send_keys("6/2/2014")
        self.find_element_and_click(value='/html/body/div[3]/div/div/form/input[3]')
        self.browser.implicitly_wait(2)
        self.assertEqual(self.get_web_element(value='//*[@id="dau-container"]/../div[3]/strong').text,
                         second='Average DAU for 05/25/2014 - 06/02/2014',
                         msg="filters did not appropriately refresh data")

    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        super(AnalyticsTestSuite, cls).tearDownClass()
        logger.info("Finished executing AnalyticsTestSuite")
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
