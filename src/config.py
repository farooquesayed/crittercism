import os
import ConfigParser

from src import clogger


logger = clogger.setup_custom_logger(__name__)


class BaseConfig(object):
    SECTION_NAME = None

    def __init__(self, conf):
        self.conf = conf

    def get(self, item_name, default_value=None, raw=True):
        try:
            return self.conf.get(self.SECTION_NAME, item_name, raw=raw)
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            return default_value


class LoginConfig(BaseConfig):
    """ Provides configuration information for browser config """

    SECTION_NAME = "login"


    @property
    def login_url(self):
        return self.get("login_url", "https://app.crittercism.com/developers/login")


    @property
    def username(self):
        return self.get("username", "nsolaiappan@crittercism.com")

    @property
    def password(self):
        return self.get("password", "CritPass123")

    @property
    def test_user_engg(self):
        return self.get("test_user_engg", "critterrism.eng@gmail.com")

    @property
    def test_user_manager(self):
        return self.get("test_user_man", "critterrism.manager@gmail.com")

    @property
    def test_user_admin(self):
        return self.get("test_user_admin", "critterrism.eng@gmail.com")

    @property
    def test_user_password(self):
        return self.get("test_user_password", "testUserPassword123")


class CommonConfig(BaseConfig):
    """Provides configuration information for common config."""

    SECTION_NAME = "common"

    @property
    def chrome_driver_path(self):
        return self.get("chromedriver_path", "./bin/chromedriver")

    @property
    def known_bugs_filename(self):
        """Log file to capture tests output """
        return self.get("known_bugs_filename", "./conf/knownBugs.txt")


    @property
    def data_location(self):
        """ Data used while Running test """
        return self.get("data_location", "./data/")

    @property
    def url(self):
        """ Data used while Running test """
        return self.get("url", "https://app.crittercism.com/developers")



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

        path = os.environ.get('CONFIG_FILE','../../config/webtesting.conf')
        #path =  "../../config/webtesting.conf"

        if path is None or not os.path.exists(path):
            msg = "Config file %(path)s not found" % locals()
            raise RuntimeError(msg)

        logger.info("Running using cli config file '%s'" % path)

        self._conf = self.load_config(path)

        self.common = CommonConfig(self._conf)
        self.login = LoginConfig(self._conf)
        self.knownBugList = []


    def load_config(self, path):
        """Read configuration from given path and return a config object."""
        config = ConfigParser.SafeConfigParser()
        config.read(path)
        return config

@Singleton
class BrowserConfig:
    """ Provides OpenStack Horizon configuration information """

    def __init__(self):
        path = os.environ.get('CONFIG_FILE','/Users/farooque/PycharmProjects/crittercism/config/webtesting.conf')
        #path =  "../../config/webtesting.conf"
        if path is None or not os.path.exists(path):
            msg = "Config file %(path)s not found" % locals()
            raise RuntimeError(msg)

        logger.info("Running using cli config file '%s'" % path)

        self._conf = self.load_config(path)

        self.login = LoginConfig(self._conf)


    def load_config(self, path):
        """Read configuration from given path and return a config object."""
        config = ConfigParser.SafeConfigParser()
        config.read(path)
        return config

