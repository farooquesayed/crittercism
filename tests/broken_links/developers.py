__author__ = 'farooque'

import nose.plugins.attrib

import src
from src import baseTest
from src import clogger
from src import config

logger = src.clogger.setup_custom_logger(__name__)

page_url = config.CliConfig().common.url + "/developers/"


class BrokenLinkTestSuite(baseTest.CrittercismTestCase):
    @classmethod
    def setUpClass(cls):
        super(BrokenLinkTestSuite, cls).setUpClass()

    def setUp(self):
        self.browser.get(page_url)
        pass


    @nose.plugins.attrib.attr(genre='links')
    def test_broken_links(self):

        links = []

        for link in self.browser.find_elements_by_xpath('//a'):
                try:
                    url = link.get_attribute("href")
                except:
                    continue
                if "https" in url:
                    logger.debug("Link is %s" %url)
                    links.append(url)

        with self.multiple_assertions():
            for link in links:
                logger.debug("Going to  '%s'" %link)
                self.browser.get(link)
                element = self.browser.find_elements_by_xpath('//*[contains(text(),"Well, this is embarrassing - you found a broken link.")]').__len__()
                self.assertGreater(1,element, "Found a broken LInk ar URL " + link)
                break

    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        super(BrokenLinkTestSuite, cls).tearDownClass()
        logger.info("Finished executing BrokenLinkTestSuite")
        pass

