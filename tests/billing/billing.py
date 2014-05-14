import unittest

from nose.plugins.attrib import attr

from src.page_helpers import utils


__author__ = 'farooque'

from src import baseTest
from src import clogger
from src import config

logger = clogger.setup_custom_logger(__name__)

page_url = config.CliConfig().common.url + "/account/billing"

class FAQSuite(baseTest.CrittercismTestCase):

    @classmethod
    def setUpClass(cls):
        super(FAQSuite, cls).setUpClass()
        pass

    def setUp(self):
        self.browser.get(page_url)
        pass

    @attr(genre="faq", smoke=True)
    def test_billing_page(self):
        self.assertFalse(utils.is_url_broken(browser=self.browser,link=page_url), " Oops page was found at " + page_url)

    @attr(genre="faq", smoke=True)
    def test_billing_plan(self):
        plan_type = self.browser.find_element_by_xpath('//*[contains(text(),"Your Plan:")]').text
        self.assertIn("Enterprise", plan_type, " Expecting Entripise but found " + plan_type)


    def tearDown(self):
        #Can override the base class setUp here
        pass


    @classmethod
    def tearDownClass(self):
        super(FAQSuite, self).tearDownClass()
        logger.info("Finished executing SampleTestSuite")
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
