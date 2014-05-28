__author__ = 'farooque'

from src import config

def get_id_from_app_name(browser=None, app_name=None):
    """
        Return an app_id given an app name
        :Args:
         - browser = Current instance of browser
         - app_name = Name of the app to look for

        :Usage:
            team.get_id_from_app_name(browser, app_name)
    """
    browser.get(config.CliConfig().common.url + "/developers")

    table = browser.find_element_by_id("app-table")

    app_list = table.find_elements_by_xpath('//*[@id="app-table"]/tbody/*/td[2]/a[contains(text(),"' + app_name + '")]')
    app_ids = []
    for app in app_list:
        id = app.get_attribute("href").split('/')
        app_ids.append(id[len(id) - 1 ])

    return app_ids

def delete_app_given_ids(browser=None, app_ids=None):
    """
        Delete the app(s) given an Ids
        :Args:
         - browser = Current instance of browser
         - app_ids = List of app_ids to delete

        :Usage:
            team.get_id_from_app_name(browser, app_ids)
    """
    for app_id in app_ids:
        url = config.CliConfig().common.url + '/developers/app-settings/' + app_id + '#delete-app'
        browser.get( url )
        browser.find_element_by_id('delete-app-' + app_id).click()
        alert = browser.switch_to_alert()
        alert.accept()

    return True
