import unittest

from nose.plugins.attrib import attr
from selenium.webdriver.common.keys import Keys


__author__ = 'farooque'

from src import baseTest
from src import clogger
from src import config

logger = clogger.setup_custom_logger(__name__)

page_url = config.CliConfig().common.url + "/account/billing"

class BillingSuite(baseTest.CrittercismTestCase):

    @classmethod
    def setUpClass(cls):
        super(BillingSuite, cls).setUpClass()
        pass

    def setUp(self):
        self.browser.get(page_url)
        pass

    @attr(genre="billing", smoke=True)
    def test_billing_page(self):
        self.assertFalse(self.is_url_broken(link=page_url), " Oops page was found at " + page_url)

    @attr(genre="billing", smoke=True)
    def test_billing_plan(self):
        __name__ + """ [Test] Billing Plan Type """

        plan_type = self.browser.find_element_by_xpath('//*[contains(text(),"Your Plan:")]').text
        self.assertIn(self.config.common.plan_type, plan_type,  (" Expecting %s but found %s " % (self.config.common.plan_type, plan_type )))

    @attr(genre="billing")
    def test_billing_search_by_email(self):
        __name__ + """ [Test] Verify User's Email Address and Credit Card through admin login """

        search_page_url = config.CliConfig().common.url +  "/admin/search"
        email_id = "nsolaiappan+finarcbasicsignup@crittercism.com"
        self.browser.get(search_page_url)
        self.browser.find_element_by_id("search-email").send_keys(email_id + Keys.ENTER)

        email_link = self.browser.find_element_by_xpath("//a[contains(text(),'" + email_id + "')]").get_attribute("href")
        self.browser.get(email_link)

        actual_email = self.browser.find_element_by_xpath("//table//*/*[contains(text(),'nsolaiappan+finarcbasicsignup@crittercism.com')]").text
        self.assertEqual(actual_email, email_id, ("Expecting %s email but found %s instead" % (actual_email, email_id)))

        billed_plan_caption = self.browser.find_element_by_xpath('//*[@id="admin-portal"]/div/table[1]/tbody/tr[13]/td[1]/strong').text
        billed_plan_value = self.browser.find_element_by_xpath('//*[@id="admin-portal"]/div/table[1]/tbody/tr[13]/td[2]').text
        self.assertEqual("Basic", billed_plan_value, ("Expecting Basic but found %s" % billed_plan_value) )

        pay_via_caption = self.browser.find_element_by_xpath('//*[@id="admin-portal"]/div/table[1]/tbody/tr[16]/td[1]/strong').text
        pay_via_value = self.browser.find_element_by_xpath('//*[@id="admin-portal"]/div/table[1]/tbody/tr[16]/td[2]').text
        self.assertEqual("Credit Card", pay_via_value, ("Expecting Credit Card but found %s" % pay_via_value) )


    def tearDown(self):
        #Can override the base class setUp here
        pass


    @classmethod
    def tearDownClass(self):
        super(BillingSuite, self).tearDownClass()
        logger.info("Finished executing SampleTestSuite")
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
