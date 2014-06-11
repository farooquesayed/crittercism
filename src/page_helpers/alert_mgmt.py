from src.constants import ALERT_TYPES
from src.wait_utils import Waiter

__author__ = 'egeller'

def alert_setup(suite=None, app_id=None):
    suite.assertTrue(app_id, "ERROR: Must assign app_id in alert_mgmt functions!")
    suite.browser.get(suite.config.common.url + "/developers/alerts/" + app_id)
    waiter = Waiter(driver=suite.browser)
    waiter.wait_until_visible_by_xpath(xpath='//span[contains(@class, createAlertLink)]',
                                       timeout=waiter.timeout, pool_period=waiter.pool_period)

def create_new_alert(suite=None, app_id=None, alert_type= ALERT_TYPES.APP_LOADS, threshold=1):
    """
        :return 0: alert name, 1: threshold
    """
    alert_setup(suite, app_id)
    suite.find_element_and_click(value='//span[contains(text(), "Create Alert")]')
    suite.find_element_and_click(value='//*[@id="alertSelector_metric_chosen"]')
    suite.find_element_and_click(value='//li[@data-option-array-index="' + str(alert_type) + '"]')
    suite.browser.implicitly_wait(5)
    alert_name = suite.get_web_element(value='//a[@class="chosen-single"]/span').text
    if "Percentage" or "Rate" in alert_name:
        threshold = round((threshold - 1) / 9999.0 * 100 + 1, 2)
    suite.get_web_element(value='//input[@data-attr="threshold"]').send_keys(str(threshold))
    #TODO: Add filter support (under 'more details')
    suite.find_element_and_click(value='//input[@id="alertCreate-submit"]')

    return [alert_name, str(threshold)]

def delete_alert(suite=None, app_id=None, idx=0):
    alert_setup(suite, app_id)
    div_str_idx = '//div[contains(@class, "moduleContents")]/div[' + str(idx + 1)
    suite.find_element_and_click(value=div_str_idx +']//a[contains(text(), "Delete")]')
    suite.find_element_and_click(value=div_str_idx +']//a[contains(text(), "Confirm")]')