import random

__author__ = 'egeller'

def goto_crash(suite=None, app_id=None, idx=0):
    suite.browser.get(suite.config.common.url + "/developers/crash-summary/" + app_id)
    suite.find_element_and_click(value='//tbody/tr[' + str(idx+1) + ']/td[contains(@class, "title")]/a')

def post_team_note(suite=None, app_id=None, note=None):
    goto_crash(suite,app_id, 0)
    if not note:
        note = "I think that " + str(random.random()) + "is a fine number"
    suite.get_web_element(value= '//textarea[@id="custom-note"]').send_keys(note)
    suite.find_element_and_click(value='//input[@value="Add Note"]')
    return note