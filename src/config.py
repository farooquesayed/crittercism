import os
import sys
import ConfigParser

from yopenstackqe_tests.common.utils import data_utils
from yopenstackqe_tests.common.utils import yLogger
from yopenstackqe_tests.common.utils.linux import ExecuteCommands


logger = yLogger.setup_custom_logger(__name__)


class BaseConfig(object):
    SECTION_NAME = None

    def __init__(self, conf):
        self.conf = conf

    def get(self, item_name, default_value=None, raw=True):
        try:
            return self.conf.get(self.SECTION_NAME, item_name, raw=raw)
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            return default_value


class HorizonConfig(BaseConfig):
    """ Provides configuration information for browser config """

    SECTION_NAME = "Horizon"

    @property
    def chromedriver_path(self):
        return self.get("chromedriver_path", "/home/y/bin/chromedriver")

    @property
    def horizon_url(self):
        return self.get("horizon_url", None)

    @property
    def image_name(self):
        return self.get("image_name", None)

    @property
    def flavor_name(self):
        return self.get("flavor_name", None)


class CommonConfig(BaseConfig):
    """Provides configuration information for common config."""

    SECTION_NAME = "common"

    @property
    def sql_connection(self):
        """SQL connection details"""
        return self.get("sql_connection", None)

    @property
    def keystone_sql_connection(self):
        """Keystone SQL connection details"""
        return self.get("keystone_sql_connection", None)

    @property
    def glance_sql_connection(self):
        """Glance SQL connection details"""
        return self.get("glance_sql_connection", None)

    @property
    def log_file(self):
        """Log file to capture test output """
        return self.get("log_file", "/tmp/yopenstackqe_tests.log")

    @property
    def known_failure_filename(self):
        """Log file to capture test output """
        return self.get("known_failure_filename", "/home/y/conf/yopenstackqe_tests/known_failures.txt")


class YProperties(BaseConfig):
    """Provides configuration information for accessiing RolesDb, OpsDb, DnsDb."""

    SECTION_NAME = "yProperties"

    @property
    def opsdb_user(self):
        """OpsDB readonly user """
        return self.get('opsdb_user', None)

    @property
    def opsdb_pw(self):
        """OpsDB password. Read from keydb """
        return CliConfig().read_keydb(self.get("opsdb_pw", None))

    @property
    def yahoo_opsdb_get_url(self):
        """URL used to search OPS DB records in test OPSDB"""
        return self.get("yahoo_opsdb_get_url",
                        'http://test1.api.opsdb.ops.yahoo.com:4080/V3/Node.Get')

    @property
    def dnsdb_user(self):
        """DnsDB readonly user """
        return self.get('dnsdb_user', None)

    @property
    def dnsdb_pw(self):
        """dnsDB password """
        return CliConfig().read_keydb(self.get("dnsdb_pw", None))

    @property
    def yahoo_dnsdb_find_url(self):
        """URL used to search DNS DB records in test DNS"""
        return self.get("yahoo_dnsdb_find_url",
                        'http://test2.api.dns.ops.yahoo.com:4080/rest/V2/Record.FindBasic')

    @property
    def rolesdb_user(self):
        """rolesDB readonly with RolesDb"""
        return self.get('rolesdb_user')

    @property
    def rolesdb_pw(self):
        """rolesDB password """
        return self.get('rolesdb_pw')


class OsNativeConfig(BaseConfig):
    """Provides configuration information for osNative config."""

    SECTION_NAME = "osNative"

    @property
    def OS_USERNAME(self):
        """Username to access nativeOS service"""
        return self.get("OS_USERNAME", os.environ.get('OS_USERNAME'))

    @property
    def OS_TENANT_NAME(self):
        """Username to access nativeOS service"""
        return self.get("OS_TENANT_NAME", os.environ.get('OS_TENANT_NAME'))

    @property
    def OS_AUTH_URL(self):
        """Username to access nativeOS service"""
        authurl = self.get("OS_AUTH_URL", os.environ.get('OS_AUTH_URL'))
        logger.debug("AUTH-URL: " + authurl)
        return authurl


class IdentityConfig(BaseConfig):
    """Provides configuration information for authenticating with Keystone."""

    SECTION_NAME = "identity"

    @property
    def catalog_type(self):
        """Catalog type of the Identity service."""
        return self.get("catalog_type", 'identity')

    @property
    def host(self):
        """Host IP for making Identity API requests."""
        return self.get("host", "127.0.0.1")

    @property
    def port(self):
        """Port for the Identity service."""
        return self.get("port", "8773")

    @property
    def api_version(self):
        """Version of the Identity API"""
        return self.get("api_version", "v1.1")

    @property
    def path(self):
        """Path of API request"""
        return self.get("path", "/")

    @property
    def auth_url(self):
        """The Identity URL (derived)"""
        auth_url = data_utils.build_url(self.host,
                                        self.port,
                                        self.api_version,
                                        self.path,
                                        use_ssl=False)
        return auth_url

    @property
    def use_ssl(self):
        """Specifies if we are using https."""
        return self.get("use_ssl", 'false').lower() != 'false'

    @property
    def strategy(self):
        """Which auth method does the environment use? (basic|keystone)"""
        return self.get("strategy", 'keystone')

    @property
    def aria_vm_name(self):
        """Log file to capture test output """
        return self.get("aria_vm_name", "vm_booter_auto")


class ComputeConfig(BaseConfig):
    SECTION_NAME = "compute"

    @property
    def allow_tenant_isolation(self):
        """
        Allows test cases to create/destroy tenants and users. This option
        enables isolated test cases and better parallel execution,
        but also requires that OpenStack Identity API admin credentials
        are known.
        """
        return self.get("allow_tenant_isolation", 'false').lower() != 'false'

    @property
    def allow_tenant_reuse(self):
        """
        If allow_tenant_isolation is True and a tenant that would be created
        for a given test already exists (such as from a previously-failed run),
        re-use that tenant instead of failing because of the conflict. Note
        that this would result in the tenant being deleted at the end of a
        subsequent successful run.
        """
        return self.get("allow_tenant_reuse", 'true').lower() != 'false'

    @property
    def username(self):
        """Username to use for Nova API requests."""
        return self.get("username", "demo")

    @property
    def tenant_name(self):
        """Tenant name to use for Nova API requests."""
        return self.get("tenant_name", "demo")

    @property
    def password(self):
        """API key to use when authenticating. Read from keydb"""
        return CliConfig().read_keydb(self.get("password", None))

    @property
    def alt_username(self):
        """Username of alternate user to use for Nova API requests."""
        return self.get("alt_username")

    @property
    def alt_tenant_name(self):
        """Alternate user's Tenant name to use for Nova API requests."""
        return self.get("alt_tenant_name", None)

    @property
    def alt_password(self):
        """API key to use when authenticating as alternate user. Read from keydb"""
        return CliConfig().read_keydb(self.get("alt_password", None))

    @property
    def image_ref(self):
        """Valid primary image to use in tests."""
        return self.get("image_ref", "{$IMAGE_ID}")

    @property
    def user_data(self):
        """The contents of this file are sent with user-data argument of 'nova boot' for password-less access"""
        return self.get("user_data", None)

    @property
    def key_filename(self):
        """This file should contain the private key of the user created during 'nova boot' """
        return self.get("key_filename", None, raw=False)

    @property
    def image_ref_alt(self):
        """Valid secondary image reference to be used in tests."""
        return self.get("image_ref_alt", "{$IMAGE_ID_ALT}")

    @property
    def minimum_image_list(self):
        """Valid secondary image reference to be used in tests."""
        return self.get("minimum_image_list", "openstack_image_rhel_6_4-2_1,ylinux-5.6.1-14,ylinux-5.8.1-14")

    @property
    def boot_timeout(self):
        """Maximum time to wait for VM to become active before giving up."""
        return self.get("boot_timeout", 300)

    @property
    def flavor_ref(self):
        """Valid primary flavor to use in tests."""
        return self.get("flavor_ref", 1)

    @property
    def flavor_ref_alt(self):
        """Valid secondary flavor to be used in tests."""
        return self.get("flavor_ref_alt", 2)

    @property
    def resize_available(self):
        """Does the test environment support resizing?"""
        return self.get("resize_available", 'false').lower() != 'false'

    @property
    def live_migration_available(self):
        return self.get(
            "live_migration_available", 'false').lower() == 'true'

    @property
    def use_block_migration_for_live_migration(self):
        return self.get(
            "use_block_migration_for_live_migration", 'false'
        ).lower() == 'true'

    @property
    def change_password_available(self):
        """Does the test environment support changing the admin password?"""
        return self.get("change_password_available", 'false').lower() != 'false'

    @property
    def create_image_enabled(self):
        """Does the test environment support snapshots?"""
        return self.get("create_image_enabled", 'false').lower() != 'false'

    @property
    def build_interval(self):
        """Time in seconds between build status checks."""
        return float(self.get("build_interval", 10))

    @property
    def build_timeout(self):
        """Timeout in seconds to wait for an instance to build."""
        return float(self.get("build_timeout", 300))

    @property
    def run_ssh(self):
        """Does the test environment support snapshots?"""
        return self.get("run_ssh", 'false').lower() != 'false'

    @property
    def ssh_user(self):
        """User name used to authenticate to an instance."""
        return self.get("ssh_user", "root")

    @property
    def ssh_timeout(self):
        """Timeout in seconds to wait for authentcation to succeed."""
        return float(self.get("ssh_timeout", 180))

    @property
    def network_for_ssh(self):
        """Network used for SSH connections."""
        return self.get("network_for_ssh", "default")

    @property
    def ip_version_for_ssh(self):
        """IP version used for SSH connections."""
        return int(self.get("ip_version_for_ssh", 4))

    @property
    def catalog_type(self):
        """Catalog type of the Compute service."""
        return self.get("catalog_type", 'compute')

    @property
    def log_level(self):
        """Level for logging compute API calls."""
        return self.get("log_level", 'ERROR')

    @property
    def whitebox_enabled(self):
        """Does the test environment support whitebox tests for Compute?"""
        return self.get("whitebox_enabled", 'false').lower() != 'false'

    @property
    def db_uri(self):
        """Connection string to the database of Compute service"""
        return self.get("db_uri", None)

    @property
    def source_dir(self):
        """Path of nova source directory"""
        return self.get("source_dir", "/opt/stack/nova")

    @property
    def config_path(self):
        """Path of nova configuration file"""
        return self.get("config_path", "/etc/nova/nova.conf")

    @property
    def bin_dir(self):
        """Directory containing nova binaries such as nova-manage"""
        return self.get("bin_dir", "/usr/local/bin/")

    @property
    def path_to_private_key(self):
        """Path to a private key file for SSH access to remote hosts"""
        return self.get("path_to_private_key")

    @property
    def yahoo_default_hostname_template(self):
        """Default hostname format, as defined in /etc/nova/nova.conf """
        return self.get("yahoo_default_hostname_template",
                        "oxy-%(zone)s-%(ip)s.%(colo)s.yahoo.com")

    @property
    def yahoo_opsdb_property(self):
        """Used in looking up hosts in OpsDb """
        return self.get("yahoo_opsdb_property", "openstack.us")

    @property
    def yahoo_colo(self):
        """As defined in /etc/nova/nova.conf """
        return self.get("yahoo_colo", "test.stg.sp2")

    @property
    def yahoo_zone(self):
        """As defined in /etc/nova/nova.conf """
        return self.get("yahoo_zone", None)

    @property
    def yahoo_ssh_user(self):
        """Used to SSH into the created VM """
        return self.get("yahoo_ssh_user", 'op_stack')

    @property
    def data_location(self):
        """ Data used while creating VMs """
        return self.get("data_location", None)

    @property
    def ssh_config_filename(self):
        """This file controls the entries into ~/.ssh/known_hosts, wiht the
            presence of 'UserKnownHostsFile=/dev/null' entry in it. Needed
            because else SSHs into VMs fail because of conflicting key entries
            in known_hosts"""
        home = os.getenv("HOME")
        return home + "/.ssh/config"

    @property
    def yahoo_special_role(self):
        """ This role is defined in policy.json (API node) """
        return self.get("yahoo_special_role", "SomeRole")

    @property
    def hypevisor_name_begins_with(self):
        """ This value is used with the test for 'nova list --host <hypervisor>'.
            As the hypervisors are caller differently in different environments,
            one would want to make this value configurable """
        return self.get("hypevisor_name_begins_with", "cloudtest")

    @property
    def custom_hostname(self):
        """ used in custom_hostname test case """
        return self.get("custom_hostname", None)

    @property
    def yrole(self):
        """ results in --yrole argument getting passed to 'nova boot'"""
        return self.get("yrole", "--yrole openstack.cm3.devlab")

    @property
    def roles_host(self):
        """ 'rocl' would search for yrole on this API server """
        return self.get("roles_host", None)


class HaConfig(BaseConfig):
    """Provides configuration information for High Availabilit (HA)."""

    SECTION_NAME = "ha"

    @property
    def api_poc(self):
        """CNAME for the API Host cluster"""
        return self.get("api_poc", None)

    @property
    def api_cluster(self):
        """Nodes in the API cluster"""
        return self.get("api_cluster", None)

    @property
    def db_poc(self):
        """CNAME for the DB Host cluster"""
        return self.get("db_poc", None)

    @property
    def db_cluster(self):
        """Nodes in the DB cluster"""
        return self.get("db_cluster", None)

    @property
    def queue_server_poc(self):
        """CNAME for the DB Host cluster"""
        return self.get("queue_server_poc", None)

    @property
    def queue_server_cluster(self):
        """Nodes in the Queue Server cluster"""
        return self.get("queue_server_cluster", None)

    @property
    def hypervisor_cluster(self):
        """Hypervisor nodes"""
        return self.get("hypervisor_cluster", None)


def Singleton(self):
    """Simple wrapper for classes that should only have a single instance"""
    instances = {}

    def getinstance():
        if self not in instances:
            instances[self] = self()
        return instances[self]

    return getinstance


@Singleton
class CliConfig:
    """Provides OpenStack configuration information."""

    def __init__(self):
        """Initialize a configuration from a conf directory and conf file."""

        path = os.environ['CONFIG_FILE']
        if path is None or not os.path.exists(path):
            msg = "Config file %(path)s not found" % locals()
            raise RuntimeError(msg)

        logger.info("Running using cli config file '%s'" % path)

        self._conf = self.load_config(path)

        self.common = CommonConfig(self._conf)
        self.identity = IdentityConfig(self._conf)
        self.compute = ComputeConfig(self._conf)
        self.yProperties = YProperties(self._conf)
        self.osNative = OsNativeConfig(self._conf)
        self.haConfig = HaConfig(self._conf)
        self.knownFailureList = []
        self.defaultImage = None
        self.defaultImageAlt = None

    def read_keydb(self, key):
        if os.environ.get(key) is not None:
            logger.info("Read password from Env (memory):" + key + "::: <REDACTED>")
            return os.environ[key]

        cmdAsList = ["sudo", "/home/y/bin64/keydbgetkey", key]
        logger.info("Keydb read invoked /home/y/bin64/keydbgetkey with key :" + key)
        exec_command = ExecuteCommands.LocalCommands(cmdAsList)
        stdIoErrDetails = exec_command.execute()

        if stdIoErrDetails['retCode'] == 0:
            logger.info("Successfully read password from keydb, for:" + key)
        else:
            logger.error("Could not read keydbgetkey[" + str(stdIoErrDetails['stdErr']) + "]")
            sys.exit(1)

        os.environ[key] = stdIoErrDetails['stdOut']

        return stdIoErrDetails['stdOut']

    def load_config(self, path):
        """Read configuration from given path and return a config object."""
        config = ConfigParser.SafeConfigParser()
        config.read(path)
        return config

@Singleton
class BrowserConfig:
    """ Provides OpenStack Horizon configuration information """

    def __init__(self):
        path = os.environ['CONFIG_FILE']
        if path is None or not os.path.exists(path):
            msg = "Config file %(path)s not found" % locals()
            raise RuntimeError(msg)

        logger.info("Running using cli config file '%s'" % path)

        self._conf = self.load_config(path)

        self.browser = HorizonConfig(self._conf)

    def load_config(self, path):
        """Read configuration from given path and return a config object."""
        config = ConfigParser.SafeConfigParser()
        config.read(path)
        return config

