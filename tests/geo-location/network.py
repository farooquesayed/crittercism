import unittest

from nose.plugins.attrib import attr


__author__ = 'farooque'

from src import baseTest
from src import config

page_url = config.CliConfig().common.url + '/developers/network/52fb0fdb8b2e3365c6000008/location/world/service/youtube/latency'


class NetworkTestSuite(baseTest.CrittercismTestCase):
    @classmethod
    def setUpClass(cls):
        super(NetworkTestSuite, cls).setUpClass()

    def setUp(self):
        self.browser.get(self.config.common.url + "/developers/register_application")

    @attr(genre='latency-check')
    def test_verify_new_app_page_default_parameter_platform(self):
        __name__ + """[Test] Find all Broken Links from Developers landing page """

        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)

