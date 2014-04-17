import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class HorizonTestCase(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.addCleanup(self.browser.quit)

    @unittest.skip("TEst")
    def testPageTitle(self):
        """

        :type self: object
        """
        self.browser.get('http://openhouse.corp.yahoo.com/')


    def testSignIn(self):
        self.browser.get('http://openhouse.corp.yahoo.com/')
        self.assertIn("Login - Yahoo! OpenStack Dashboard",self.browser.title)
        inputElement = self.browser.find_element_by_css_selector ("button.btn")
        inputElement.submit()
        self.assertIn('Instance Overview', self.browser.title)

if __name__ == '__main__':
    unittest.main(verbosity=2)
