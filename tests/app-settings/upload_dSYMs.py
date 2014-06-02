import random

from selenium.webdriver.common.by import By
import unittest2 as unittest
from nose.plugins.attrib import attr

from src import clogger
from src import baseTest
from src.page_helpers import team
from src import config


__author__ = 'farooque'

page_url = config.CliConfig().common.url + "/developers/register-application"

#app_name = "TiborTestAPP"
app_name = "IOS-" + str(random.random())

logger = clogger.setup_custom_logger(__name__)


class UploadDSymSuite(baseTest.CrittercismTestCase):
    @classmethod
    def setUpClass(cls):
        super(UploadDSymSuite, cls).setUpClass()
        pass

    def setUp(self):
        self.browser.get(page_url)

        self.browser.find_element_by_id("app-name").send_keys(app_name)
        self.assertFalse(self.find_element_and_click(by=By.ID, value='commit'),
                         " Broken link at " + self.browser.current_url)

    @attr(genre="upload-dsym")
    def test_double_quote_around_source_root(self):
        __name__ + """[Test] double quote on source root  : https://crittercism.atlassian.net/browse/PP-1216 """

        app_id = team.get_id_from_app_name(browser=self.browser, app_name=app_name)
        logger.debug("Found the ID = %s" % app_id[0])
        self.browser.get(self.config.common.url + "/developers/app-settings/" + app_id[0] + "#upload-mapping")

        web_element = self.browser.find_element_by_xpath('//*[@id="upload-dsym"]/div[1]/pre/code')

        self.assertIn('"{SRCROOT}"/CrittercismSDK/dsym_upload.sh', web_element.text,
                      ("Expecting SRCROOT to be surronded by double quotes but found %s" % web_element.text))

    def tearDown(self):
        app_ids = team.get_id_from_app_name(browser=self.browser, app_name=app_name)
        self.assertEquals(True, team.delete_app_given_ids(browser=self.browser, app_ids=app_ids),
                          "Deleting App failed")
        pass

    @classmethod
    def tearDownClass(cls):
        super(UploadDSymSuite, cls).tearDownClass()
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)