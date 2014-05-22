__author__ = 'farooque'

from requests.exceptions import InvalidSchema, MissingSchema, ConnectionError

from src import clogger, config

logger = clogger.setup_custom_logger(__name__)


def get_all_links(browser=None):
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


def is_url_broken(browser=None, link=None):

    try:
        # Navigate to the link if it is not there already
        if link != browser.current_url :
            browser.get(link)
        #Needs to login instead any of the link redirect us to login page
        if "login" in browser.current_url and browser.find_elements_by_id('email').__len__() > 1:
            login()

        element = browser.find_elements_by_xpath(
            '//*[contains(text(),"Well, this is embarrassing - you found a broken link.")]').__len__()
        return element
    except (InvalidSchema, MissingSchema, ConnectionError):
        return True


def login(browser=None):
    browser.get(config.CliConfig().common.url + "/developers/login")
    browser.find_element_by_id('email').send_keys(config.CliConfig().login.username)
    browser.find_element_by_name('password').send_keys(config.CliConfig().login.password)
    browser.find_element_by_id('commit').submit()

def login_to_yahoo(browser=None, username=config.CliConfig().login.test_user_engg, password=config.CliConfig().login.password):
    browser.get("https://mail.yahoo.com")
    browser.find_element_by_id("username").send_keys(username)
    browser.find_element_by_id("passwd").send_keys(password)
    browser.find_element_by_id(".save").submit()
