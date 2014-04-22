from nose.plugins.attrib import attr

__author__ = 'farooque'

from src import baseTest
from src import clogger

logger = clogger.setup_custom_logger(__name__)

page_url = "https://app.crittercism.com/account/billing_faq"

class FAQSuite(baseTest.SeleniumTestCase):

    @classmethod
    def setUpClass(self):
        super(FAQSuite, self).setUpClass()
        pass

    def setUp(self):
        pass

    @attr(genre="faq")
    def test_FAQ(self):
        self.browser.find_element_by_link_text("Billing FAQ").click()

    def tearDown(self):
        #Can override the base class setUp here
        pass


    @classmethod
    def tearDownClass(self):
        super(FAQSuite, self).tearDownClass()
        logger.info("Finished executing SampleTestSuite")
        pass


