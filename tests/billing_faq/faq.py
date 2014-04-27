from nose.plugins.attrib import attr

__author__ = 'farooque'

from src import baseTest
from src import clogger

logger = clogger.setup_custom_logger(__name__)


class FAQSuite(baseTest.CrittercismTestCase):

    @classmethod
    def setUpClass(cls):
        super(FAQSuite, cls).setUpClass()
        pass

    def setUp(self):
        page_url = "https://app.crittercism.com/account/billing_faq"
        self.browser.get(page_url)
        pass

    @attr(genre="faq")
    def test_FAQ(self):
        #Need Assert statement here
        pass

    def tearDown(self):
        #Can override the base class setUp here
        pass


    @classmethod
    def tearDownClass(self):
        super(FAQSuite, self).tearDownClass()
        logger.info("Finished executing SampleTestSuite")
        pass


