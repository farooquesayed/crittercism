__author__ = 'farooque'

from src import clogger

logger = clogger.setup_custom_logger(__name__)


def get_all_links(browser=None):
    links = set()
    for link in browser.find_elements_by_xpath('//a'):
        try:
            url = link.get_attribute("href")
        except:
            continue
        #if "https" in url:
        logger.debug("Link is %s" % url)
        links.add(url)

    return links

