import unittest

from src.page_helpers import utils


__author__ = 'farooque'

import nose.plugins.attrib
import requests

import src
from src import baseTest
from src import clogger

logger = src.clogger.setup_custom_logger(__name__)

page_url = "http://support.crittercism.com/"


class BrokenLinkTestSuite(baseTest.CrittercismTestCase):
    @classmethod
    def setUpClass(cls):
        super(BrokenLinkTestSuite, cls).setUpClass()

    def setUp(self):
        self.browser.get(page_url)
        pass


    @nose.plugins.attrib.attr(genre='links1')
    def test_broken_links_support_page(self):
        session = requests.session()
        with self.multiple_assertions():
            for link in utils.get_all_links(self.browser):
                logger.debug("Going to  '%s'" % link)
                resp = session.get(link)
                self.assertTrue((resp.status_code not in [500, 404]),
                                ("Return code %s LInk %s URL " % (resp.status_code, link)))

                self.browser.get(link)
                element = self.browser.find_elements_by_xpath(
                    '//*[contains(text(),"Well, this is embarrassing - you found a broken link.")]').__len__()
                self.assertGreater(1, element, "Found a broken LInk ar URL " + link)
                break


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        super(BrokenLinkTestSuite, cls).tearDownClass()
        logger.info("Finished executing BrokenLinkTestSuite")
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
