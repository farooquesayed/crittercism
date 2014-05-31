__author__ = 'farooque'

from requests.exceptions import InvalidSchema, MissingSchema, ConnectionError

from src import clogger, config


logger = clogger.setup_custom_logger(__name__)


def get_all_links(browser=None):
    """
        Return all the link from the current page

        :Args:
         - browser = Current instance of browser to search for links

        :Usage:
            utils.is_url_broken(self.browser)
    """
    links = set()
    links.add(browser.current_url)
    for link in browser.find_elements_by_xpath('//a'):
        try:
            url = link.get_attribute("href")
        except:
            continue
        if url is not None and "crittercism" in url:
            logger.debug("Link is %s" % url)
            links.add(url)

    return links


def is_url_broken_deleteme(browser=None, link=""):
    """
        Checks if the URL supplied or current page is broken or not

        :Args:
         - browser = Current instance of browser to check for broken links
         - link = Optional Value: if not passed then current page is used to test

        :Usage:
            utils.is_url_broken(self.browser)
    """
    try:
        # Navigate to the link if it is not there already
        if link != browser.current_url and link != "":
            browser.get(link)
        #Needs to login instead any of the link redirect us to login page
        if "login" in browser.current_url and browser.find_elements_by_id('email').__len__() > 1:
            login()

        element = browser.find_elements_by_xpath(
            '//*[contains(text(),"Well, this is embarrassing - you found a broken link.")]').__len__()
        return element
    except (InvalidSchema, MissingSchema, ConnectionError):
        logger.error("Hit an exception while traversing the URL")
        return True


def login(browser=None, username=config.CliConfig().login.username, password=config.CliConfig().login.password):
    """
        Login to crittercism using username and password supplied.
        If no login credential is passed then it use from the config file

        :Args:
         - browser = Current instance of browser to use to login
         - username = Optional Value: username to login into yahoo
         - password = Optional Value: password to login. Yes, the password is in plain text at the moment will encrypt it soon

        :Usage:
            utils.login(self.browser)
    """
    browser.get(config.CliConfig().common.url + "/developers/login")
    browser.find_element_by_id('email').send_keys(username)
    browser.find_element_by_name('password').send_keys(password)
    browser.find_element_by_id('commit').submit()


def login_to_yahoo(browser=None, username=config.CliConfig().login.test_user_engg,
                   password=config.CliConfig().login.password):
    """
        Login to yahoo mail using username and password supplied.
        If no login credential is passed then it use from the config file

        :Args:
         - browser = Current instance of browser to use to login
         - username = Optional Value: username to login into yahoo
         - password = Optional Value: password to login. Yes, the password is in plain text at the moment will encrypt it soon

        :Usage:
            utils.login_to_yahoo(self.browser)
    """
    browser.get("https://mail.yahoo.com")
    if browser.find_elements_by_id("username").__len__() == 0:
        logger.debug("Already logged in. Hence quitting")
        return

    browser.find_element_by_id("username").send_keys(username)
    browser.find_element_by_id("passwd").send_keys(password)
    browser.find_element_by_id(".save").submit()
    logger.debug("Hit the login button to login to yahoo")
