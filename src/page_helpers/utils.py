__author__ = 'farooque'

from requests.exceptions import InvalidSchema, MissingSchema, ConnectionError
from selenium.webdriver.common.by import By
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


def is_url_broken(browser=None, link=""):
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
        if link != browser.current_url and link != "" :
            browser.get(link)
        #Needs to login instead any of the link redirect us to login page
        if "login" in browser.current_url and browser.find_elements_by_id('email').__len__() > 1:
            login()

        element = browser.find_elements_by_xpath(
            '//*[contains(text(),"Well, this is embarrassing - you found a broken link.")]').__len__()
        return element
    except (InvalidSchema, MissingSchema, ConnectionError):
        return True


def login(browser=None, username=config.CliConfig().login.test_user_engg, password=config.CliConfig().login.password):
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

def login_to_yahoo(browser=None, username=config.CliConfig().login.test_user_engg, password=config.CliConfig().login.password):
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
    browser.find_element_by_id("username").send_keys(username)
    browser.find_element_by_id("passwd").send_keys(password)
    browser.find_element_by_id(".save").submit()

def find_element_and_click(browser=None, by=By.XPATH, value=None):
    """
        Locate an element on page by its attribute.
        If element is found click on it and verify that it does not result in 404 - page not found

        :Args:
         - browser = Current instance of browser to use to login
         - by = Optional Value: value to search the element by
         - value = element string to search for items

        :Usage:
            utils.find_element_and_click(self.browser, By.XPATH, "//div[contains(@class, 'foo')]")
    """
    #TODO: Add a check for existence of an element before blindly clicking or catch the exception and throw assertion
    browser.find_element(by=by, value=value).click()
    return is_url_broken(browser=browser)

def find_element_and_submit(browser=None, by=By.XPATH, value=None):
    """
        Locate an element on page by its attribute.
        If element is found submit on it and verify that it does not result in 404 - page not found

        :Args:
         - browser = Current instance of browser to use to login
         - by = Optional Value: value to search the element by
         - value = element string to search for items

        :Usage:
            utils.find_element_and_click(self.browser, By.XPATH, "//div[contains(@class, 'foo')]")
    """
    #TODO: Add a check for existence of an element before blindly clicking or catch the exception and throw assertion
    browser.find_element(by=by, value=value).submit()
    return is_url_broken(browser=browser)


def click(browser=None, web_element=None):
    """
        Performs an click action on the element and verify it does not result in 404 - page not found
        :Args:
         - browser = Current instance of browser to use to login
         - web_element = Web Element to be clicked

        :Usage:
            utils.click(self.browser, web_element)
    """
    #TODO: Add a check for existence of an element before blindly clicking or catch the exception and throw assertion
    web_element.click()
    return is_url_broken(browser=browser)

