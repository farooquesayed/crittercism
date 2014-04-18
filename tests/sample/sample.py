import unittest2 as unittest


#from nose.tools import with_setup
from nose.plugins.attrib import attr
from src import  logger
#from src.data_driven_test_wrapper import data_driven_test, ddt_list, data
from src import baseTest


logger = logger.setup_custom_logger(__name__)

def generate_list_of_data():
    row_list = []
    return row_list


#@data_driven_test
class SampleTestSuite(baseTest.BaseCliTest):

    @classmethod
    def setUpClass(self):
        super(SampleTestSuite, self).setUpClass()

    def setUp(self):
        #Can override the base class setUp here
        pass


    @attr(genre='sample')
    @unittest.skip("Reason : why it is skipped")
    def test_sample(self):
        __name__ + """[Test] test_quick_check """
        with self.multiple_assertions():
            self.assertEquals(0,1,"Continue on assert")
            self.assertEquals(0,1,"Continue on assert again")
            pass


    """
    @data(generate_list_of_data())
    @ddt_list
    def test_sample_ddt(self, *args, **kwargs):

        first_argument = kwargs.values()[0][0]
        second_argument = kwargs.values()[0][1]
        self.assertEquals(first_argument,second_argument,"Argument didn't matched")
    """

    def tearDown(self):
        #Can override the base class setUp here
        pass


    @classmethod
    def tearDownClass(cls):
        logger.info("Finished executing SampleTestSuite")
        pass
