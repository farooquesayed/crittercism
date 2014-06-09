import time
import random
import src.constants as constants
from selenium.webdriver.common.by import By


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
    browser.find_element_by_id('email').clear()
    browser.find_element_by_id('email').send_keys(username)
    browser.find_element_by_name('password').send_keys(password)
    browser.find_element_by_id('commit').submit()

def logout(self):
        self.browser.get(self.config.common.url + "/developers/logout")


def sign_up_new_account(self, accnt):
    def generate_account_types():
        account_types= []
        account_types.append("basic")
        account_types.append("pro")
        account_types.append("ent")
        account_types.append("pro_plus")
        return account_types

    account_types = generate_account_types()
    logout(self)
    # self.browser.implicitly_wait(3)
    self.browser.get(self.config.common.url + "/signup?plan=" + accnt)
    random_email = (self.config.login.test_user_engg).replace('@', str(random.random()) + '@')
    self.browser.find_element_by_id("firstname").send_keys("test_user_" + accnt)
    self.browser.find_element_by_id("lastname").send_keys("crittercism")
    self.browser.find_element_by_id("company").send_keys("crittercism")
    self.browser.find_element_by_id("phone").send_keys("123-456-7890")
    self.browser.find_element_by_id("email").send_keys(random_email)
    self.browser.find_element_by_id("password").send_keys(self.config.login.password)
    self.find_element_and_submit(by=By.XPATH, value="//*[contains(@class,'grid_8 push_2')]")


def create_new_app(self, platform):
    page_url = self.config.common.url + "/developers/register-application"
    self.browser.get(page_url)

    p_str = platform.PREFIX
    self.find_element_and_click(value='//label[@for=' + platform.PLATFORM + ']')
    app_name = p_str + str(random.random())
    self.browser.find_element_by_id("app-name").send_keys(app_name)
    self.assertFalse(self.find_element_and_submit(by=By.ID, value=constants.BrowserConstants.COMMIT),
                     " Broken link at " + self.browser.current_url)
    return app_name

def delete_all_yahoo_email(browser=None):
    """
      Delete all the email from Inbox and Spam folders
      :Args:
       - browser = current instance of browser already logged into yahoo email
    """
    login_to_yahoo(browser=browser)
    #Delete all the existing emails after login
    #for folder in ["//*[@class='inbox-label icon-text']", "//*[@id='spam-label']"]:
    for folder in [
        "//*[@class='inbox-label icon-text']"]:  # Only deleting it from inbox as we are moving email from spam to inbox because links are non-clickable in spam
        try:
            browser.find_element(by=By.XPATH, value=folder).click()
            time.sleep(2)
            browser.find_element(by=By.XPATH, value="//*[@class='focusable neoFocusable enabled']").click()
            time.sleep(2)
            browser.find_element(by=By.XPATH, value="//*[@class='icon-delete']").click()
            time.sleep(2)
            #Only Clicking if confirmation appear because it only happens if we have more then 10 email to delete
            browser.find_element(by=By.XPATH, value="//*[@href='#'][contains(text(),'OK')]").click()
        except:
            continue


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