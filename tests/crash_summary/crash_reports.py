import unittest

__author__ = 'farooque'

import nose.plugins.attrib

import src
from src import baseTest
from src.data_driven_test_wrapper import ddt_list, data, data_driven_test


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


@data_driven_test
class CrashReportTestSuite(baseTest.CrittercismTestCase):
    @classmethod
    def setUpClass(cls):
        super(CrashReportTestSuite, cls).setUpClass()

    def setUp(self):
        self.browser.get(self.config.common.url + "/developers/crash-summary/52fb0fdb8b2e3365c6000008")



    @nose.plugins.attrib.attr(sample=True, genre="crash-report")
    @data(generate_list_of_crash_types())
    @ddt_list
    def test_crash_data(self, value=None):
        __name__ + """ [Test] Verify the crash data of all crash types"""

        for period in self.browser.find_elements_by_xpath("//label/span[@class='ui-button-text']"):
            logger.debug("working on period %s" % period.text)
            period.click()
            with self.multiple_assertions():
                self.assertEqual(self.browser.find_element_by_id("stats-number-today").text,"0",
                                 ("Expecting No crash but found %s" % self.browser.find_element_by_id("stats-number-today").text) )

                self.assertEqual(self.browser.find_element_by_id("stats-number-week").text,"0",
                                 ("Expecting No crash but found %s" % self.browser.find_element_by_id("stats-number-week").text) )

                self.assertEqual(self.browser.find_element_by_id("stats-number-all-time").text,"0",
                                 ("Expecting No crash but found %s" % self.browser.find_element_by_id("stats-number-all-time").text) )


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        super(CrashReportTestSuite, cls).tearDownClass()
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
