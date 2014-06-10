from src import config
from src.constants import ALERT_TYPES
#from src.wait_utils import Waiter
import random

__author__ = 'egeller'

def create_new_alert(suite=None, app_id='52fb11934002051d02000004', alert_type= ALERT_TYPES.APP_LOADS, threshold=1):
    suite.browser.get(suite.config.common.url + "/developers/alerts/" + app_id)

    #Waiter.wait_until_visible_by_xpath(self=suite, xpath='//span[contains(@class, createAlertLink)]', timeout=5, pool_period=2)
    suite.browser.implicitly_wait(6)
    suite.find_element_and_click(value='//span[contains(text(), Create Alert)]')
    suite.find_element_and_click(value='//*[@id="alertSelector_metric_chosen"]')
    suite.find_element_and_click(value='//li[@data-option-array-index="' + alert_type + '"]')
    alert_name = suite.get_element(value='//a[@class="chosen-single"]/span').text
    suite.get_element(value='//input[@data-attr="threshold"]').send_keys(str(threshold))
    #TODO: Add filter support (under 'more details')
    suite.find_element_and_click(value='//input[@id="alertCreate-submit"]')

    return alert_name

