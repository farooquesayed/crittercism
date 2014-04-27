from nose.plugins.attrib import attr

__author__ = 'farooque'

from src import baseTest
class NetworkTestSuite(baseTest.CrittercismTestCase):
    page_url = 'https://app.crittercism.com/developers/network/52fb0fdb8b2e3365c6000008/location/world/service/youtube/latency'
    @classmethod
    def setUpClass(cls):
        super(NetworkTestSuite, cls).setUpClass()

    def setUp(self):
        page_url = "https://app.crittercism.com/developers/register_application"
        self.browser.get(page_url)

    @attr(genre='latency-check')
    def test_verify_new_app_page_default_parameter_platform(self):
        pass
