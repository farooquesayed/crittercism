__author__ = 'farooque'

def get_id_from_app_name(browser=None, app_name=None):

    browser.get("https://app.crittercism.com/developers")

    table = browser.find_element_by_id("app-table")

    app_list = table.find_elements_by_xpath('//*[@id="app-table"]/tbody/*/td[2]/a[contains(text(),"' + app_name + '")]')
    app_ids = []
    for app in app_list:
        id = app.get_attribute("href").split('/')
        app_ids.append(id[id.__len__() - 1 ])

    return app_ids

def delete_app_given_ids(browser=None, app_ids=None, config=None):

    for app_id in app_ids:
        url = config.common.url + '/app-settings/' + app_id + '#delete-app'
        browser.get( url )
        browser.find_element_by_id('delete-app-' + app_id).click()
        alert = browser.switch_to_alert()
        alert.accept()

    return True
