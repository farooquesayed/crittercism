###################################################################################
#     This file provides the REST API for calls into Keystone that cannot be called
#     directly from where the CLI tests run. 
#     This also supports a call into the Bouncer, for Cookie based Authentication
###################################################################################
import json
import httplib2
import logging
import time
import bouncer  
from bouncer import utils as bouncer_utils
from yopenstackqe_tests.common.utils import yLogger
from yopenstackqe_tests import exceptions

# redrive rate limited calls at most twice
MAX_RECURSION_DEPTH = 2


class RestClient(object):
    TYPE = "json"

    def __init__(self, config, user, password, auth_url, tenant_name=None):
        #self.log = logging.getLogger(__name__)
        self.log = yLogger.setup_custom_logger(__name__)
        #self.log.setLevel(getattr(logging, config.compute.log_level))
        self.log.setLevel(getattr(logging, 'INFO'))
        self.config = config
        self.user = user
        self.password = password
        self.auth_url = auth_url
        self.tenant_name = tenant_name

        self.service = None
        self.token = None
        self.base_url = None
        self.config = config
        self.region = 0
        self.endpoint_url = 'publicURL'
        self.strategy = self.config.identity.strategy
        self.headers = {'Content-Type': 'application/%s' % self.TYPE,
                        'Accept': 'application/%s' % self.TYPE}
        self.build_interval = config.compute.build_interval
        self.build_timeout = config.compute.build_timeout

    def _set_auth(self):
        """
        Sets the token and base_url used in requests based on the strategy type
        """
        if self.strategy == 'keystone':
            self.token, self.base_url = self.keystone_auth(self.user,
                                                           self.password,
                                                           self.auth_url,
                                                           self.service,
                                                           self.tenant_name)
            self.log.info("GOT TOKEN" + self.token)
        else:
            self.token, self.base_url = self.basic_auth(self.user,
                                                        self.password,
                                                        self.auth_url)

    def clear_auth(self):
        """
        Can be called to clear the token and base_url so that the next request
        will fetch a new token and base_url
        """

        self.token = None
        self.base_url = None

    def get_auth(self):
        """Returns the token of the current request or sets the token if
        none"""

        if not self.token:
            self._set_auth()

        return self.token

    def basic_auth(self, user, password, auth_url):
        """
        Provides authentication for the target API
        """

        params = {}
        params['headers'] = {'User-Agent': 'Test-Client', 'X-Auth-User': user,
                             'X-Auth-Key': password}

        self.http_obj = httplib2.Http()
        resp, body = self.http_obj.request(auth_url, 'GET', **params)
        try:
            return resp['x-auth-token'], resp['x-server-management-url']
        except:
            raise

    def _fetch_cookie(self, user, password):
        DEFAULT_BOUNCER_URL = 'https://by.bouncer.login.yahoo.com/login/'
        DEFAULT_BOUNCER_TIMEOUT = 10
        debug_level = 0
        by_ck = bouncer_utils.fetch_cookie(user, password,
                                           DEFAULT_BOUNCER_URL, 
                                           float(DEFAULT_BOUNCER_TIMEOUT))
        self.log.info("Fetched cookie as:" + str(by_ck))
        
        return str(by_ck)

    def keystone_auth(self, user, password, auth_url, service, tenant_name):
        """
        Provides authentication via Keystone
        """

        creds = {
            'auth': {
                'passwordCredentials': {
                    'username': user,
                    'password': self._fetch_cookie(user,password),
                },
                'tenantName': tenant_name,
            }
        }

        self.http_obj = httplib2.Http()
        headers = {'Content-Type': 'application/json'}
        body = json.dumps(creds)
        self.log.info("Auth URL::::::::::::::")
        self.log.info(auth_url)
        self.log.info("Auth URL::::::::::::::")
        self.log.info("Headers::::::::::::::")
        self.log.info(headers)
        self.log.info("Headers::::::::::::::")
        self.log.info("BODY::::::::::::::")
        self.log.info(body)
        self.log.info("BODY::::::::::::::")
        resp, body = self.http_obj.request(auth_url, 'POST',
                                           headers=headers, body=body)

        if resp.status == 200:
            self.log.info(json.loads(body)['access'])
            try:
                auth_data = json.loads(body)['access']
                token = auth_data['token']['id']
            except Exception, e:
                print "Failed to obtain token for user: %s" % e
                raise

            mgmt_url = None
            for ep in auth_data['serviceCatalog']:
                if ep["type"] == service and service != 'volume':
                    mgmt_url = ep['endpoints'][self.region][self.endpoint_url]
                    tenant_id = auth_data['token']['tenant']['id']
                    break

                elif (ep["type"] == service and ep['name'] == 'cinder' and
                      service == 'volume'):
                    mgmt_url = ep['endpoints'][self.region][self.endpoint_url]
                    tenant_id = auth_data['token']['tenant']['id']
                    break

            if mgmt_url is None:
                raise exceptions.EndpointNotFound(service)

            if service == 'network':
                # Keystone does not return the correct endpoint for
                # quantum. Handle this separately.
                mgmt_url = (mgmt_url + self.config.network.api_version +
                            "/tenants/" + tenant_id)

            return token, mgmt_url

        elif resp.status == 401:
            raise exceptions.AuthenticationFailure(user=user,
                                                   password=password)

    def post(self, url, body, headers):
        return self.request('POST', url, headers, body)

    def get(self, url, headers=None):
        return self.request('GET', url, headers)

    def delete(self, url, headers=None):
        return self.request('DELETE', url, headers)

    def put(self, url, body, headers):
        return self.request('PUT', url, headers, body)

    def head(self, url, headers=None):
        return self.request('HEAD', url, headers=None)

    def _log(self, req_url, body, resp, resp_body):
        self.log.error('Request URL: ' + req_url)
        self.log.error('Request Body: ' + str(body))
        self.log.error('Response Headers: ' + str(resp))
        self.log.error('Response Body: ' + str(resp_body))

    def _parse_resp(self, body):
        return json.loads(body)

    def request(self, method, url, headers=None, body=None, depth=0):
        """A simple HTTP request interface."""

        if (self.token is None) or (self.base_url is None):
            self._set_auth()

        self.http_obj = httplib2.Http()
        if headers is None:
            headers = {}
        headers['X-Auth-Token'] = self.token

        req_url = "%s/%s" % (self.base_url, url)
        req_url = req_url.replace("5000s", "35357")
        self.log.info("Constructed req_url as:" + req_url)
        resp, resp_body = self.http_obj.request(req_url, method,
                                                headers=headers, body=body)
        if resp.status == 401 or resp.status == 403:
            self._log(req_url, body, resp, resp_body)
            raise exceptions.Unauthorized()

        if resp.status == 404:
            self._log(req_url, body, resp, resp_body)
            raise exceptions.NotFound(resp_body)

        if resp.status == 400:
            resp_body = self._parse_resp(resp_body)
            self._log(req_url, body, resp, resp_body)
            raise exceptions.BadRequest(resp_body)

        if resp.status == 409:
            resp_body = self._parse_resp(resp_body)
            self._log(req_url, body, resp, resp_body)
            raise exceptions.Duplicate(resp_body)

        if resp.status == 413:
            resp_body = self._parse_resp(resp_body)
            self._log(req_url, body, resp, resp_body)
            if 'overLimit' in resp_body:
                raise exceptions.OverLimit(resp_body['overLimit']['message'])
            elif 'limit' in resp_body['message']:
                raise exceptions.OverLimit(resp_body['message'])
            elif depth < MAX_RECURSION_DEPTH:
                delay = resp['Retry-After'] if 'Retry-After' in resp else 60
                time.sleep(int(delay))
                return self.request(method, url, headers, body, depth + 1)
            else:
                raise exceptions.RateLimitExceeded(
                    message=resp_body['overLimitFault']['message'],
                    details=resp_body['overLimitFault']['details'])

        if resp.status in (500, 501):
            resp_body = self._parse_resp(resp_body)
            self._log(req_url, body, resp, resp_body)
            #I'm seeing both computeFault and cloudServersFault come back.
            #Will file a bug to fix, but leave as is for now.

            if 'cloudServersFault' in resp_body:
                message = resp_body['cloudServersFault']['message']
            elif 'computeFault' in resp_body:
                message = resp_body['computeFault']['message']
            elif 'error' in resp_body:  # Keystone errors
                message = resp_body['error']['message']
                raise exceptions.IdentityError(message)
            elif 'message' in resp_body:
                message = resp_body['message']
            else:
                message = resp_body

            raise exceptions.ComputeFault(message)

        if resp.status >= 400:
            resp_body = self._parse_resp(resp_body)
            self._log(req_url, body, resp, resp_body)
            raise exceptions.TempestException(str(resp.status))

        return resp, resp_body

    def wait_for_resource_deletion(self, id):
        """Waits for a resource to be deleted"""
        start_time = int(time.time())
        while True:
            if self.is_resource_deleted(id):
                return
            if int(time.time()) - start_time >= self.build_timeout:
                raise exceptions.TimeoutException
            time.sleep(self.build_interval)

    def is_resource_deleted(self, id):
        """
        Subclasses override with specific deletion detection.
        """
        return False
