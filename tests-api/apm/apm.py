import json

import unittest2 as unittest
import nose.plugins.attrib
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import LegacyApplicationClient

import src
from src import baseTest


logger = src.clogger.setup_custom_logger(__name__)

#dictionary of test cases. maps between end points and payload.
test_cases = \
    {'https://developers.crittercism.com/v1.0/performanceManagement/pie':
         {
             "params":
                 {
                     "appIds":
                         [
                             #"52f40a0d97c8f24c47000006",
                             "52fb117497c8f23e71000001",
                             "52fb10288b2e337282000001",
                             "519d53101386202089000007",
                             "52fb0f2f8b2e3365cd00000a",
                             "52fb11d597c8f23853000002",
                             "52fb0f5997c8f23792000002",
                             "52f126fea7928a16d2000004",
                             "52fb0fdb8b2e3365c6000008",
                             "52fb11934002051d02000004",
                             "52fb11af8b2e3378f0000001",
                             "52fb10004002051d07000004"
                         ],
                     "graph": "volume",
                     "duration": 1440,
                     "groupBy": "carrier"
                 }
         }
    }


#@ddt
class APMTestSuite(baseTest.BaseCliTest):
    CritterAPISession = None

    @classmethod
    def setUpClass(cls):
        super(APMTestSuite, cls).setUpClass()
        user_name = 'tkerbosch+s8@crittercism.com'
        password = "crittercism"
        #client id for prod:
        client_id = 'zWhcO8gVKUeADMoFpjES9VaAK8Zzf0ma'
        token_url = 'https://developers.crittercism.com/v1.0/token'
        cls.CritterAPISession = cls.create_session(token_url, client_id, user_name, password)


    def setUp(self):
        pass


    #create Oauth2 session object, fetch token from server, and return session object containing a token instance
    @classmethod
    def create_session(self, token_url, client_id, username, password):
        client = LegacyApplicationClient(client_id)
        CritterAPISession = OAuth2Session(client_id, client, ['all'])
        CritterAPISession.fetch_token(token_url=token_url, username=username, password=password, auth=(client_id, None))
        return CritterAPISession

    #@unpack
    #@data( annotated({ "name" : "Testcase1","endpoint":"https://developers.crittercism.com/v1.0/performanceManagement/pie", "params": { "appIds": [ "52f40a0d97c8f24c47000006", "52fb117497c8f23e71000001", "52fb10288b2e337282000001", "519d53101386202089000007", "52fb0f2f8b2e3365cd00000a", "52fb11d597c8f23853000002", "52fb0f5997c8f23792000002", "52f126fea7928a16d2000004", "52fb0fdb8b2e3365c6000008", "52fb11934002051d02000004", "52fb11af8b2e3378f0000001", "52fb10004002051d07000004" ], "graph": "volume", "duration": 1440, "groupBy": "carrier" } }))
    #annotated({ "name" : "Testcase2", "endpoint" :"https://developers.crittercism.com/v1.0/performanceManagement/pie", "params": { "appIds": [ "52f40a0d97c8f24c47000006", "52fb117497c8f23e71000001", "52fb10288b2e337282000001", "519d53101386202089000007", "52fb0f2f8b2e3365cd00000a", "52fb11d597c8f23853000002", "52fb0f5997c8f23792000002", "52f126fea7928a16d2000004", "52fb0fdb8b2e3365c6000008", "52fb11934002051d02000004", "52fb11af8b2e3378f0000001", "52fb10004002051d07000004" ], "graph": "volume", "duration": 1440, "groupBy": "carrier" } }))
    @nose.plugins.attrib.attr(genre='apm', smoke=True)
    def test_apm(self):
        headers = {'content-type': 'application/json'}

        for api_end_point in test_cases.iterkeys():
            #APITestCase = self.run_test(self.CritterAPISession, api_end_point, test_cases[api_end_point])

            logger.debug("Request : %s Post body %s" % (api_end_point, test_cases[api_end_point]))
            APITestCase = self.CritterAPISession.post(api_end_point, data=json.dumps(test_cases[api_end_point]),
                                                      headers=headers)
            logger.debug("Response object : %s with code = %d" % (APITestCase.content, APITestCase.status_code))
            self.assertTrue((APITestCase.status_code not in [500, 404]),
                            ("Return code %d " % (APITestCase.status_code)))
            self.assertIn("application/json", APITestCase.headers['content-type'],
                          "Unexpected content type in API response : Expecting Json got %s" % (
                          APITestCase.headers['content-type']))


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        super(APMTestSuite, cls).tearDownClass()
        logger.info("Finished executing APMTestSuite")
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)