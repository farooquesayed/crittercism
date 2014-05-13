__author__ = 'farooque'

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

def login(browser=None):
    browser.get(config.CliConfig().login.login_url)
    browser.find_element_by_id('email').send_keys(config.CliConfig().login.username)
    browser.find_element_by_name('password').send_keys(config.CliConfig().login.password)
    browser.find_element_by_id('commit').submit()
