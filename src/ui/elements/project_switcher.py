from selenium.webdriver.firefox.webdriver import WebDriver

class ProjectSwitcher(object):

    root_id = 'tenant_switcher'
    toggle_switcher_xpath = '//a'
    selected_project_xpath = '//a/h3'
    project_list_id = 'tenant_list'

    def __init__(self, driver):
        self.driver = driver

    def toggle_list(self):
        self.driver.find_element_by_id(self.root_id). \
            find_element_by_xpath(self.toggle_switcher_xpath).click()

    def open_list(self):
        switcher_class = self.driver.find_element_by_id(
            self.root_id).get_attribute('class')

        if str(switcher_class).find('open') == -1:
            self.toggle_list()

    def close_list(self):
        switcher_class = self.driver.find_element_by_id(
            self.root_id).get_attribute('class')

        if str(switcher_class).find('open') != -1:
            self.toggle_list()

    def select_project(self, project):

        selected_project = self.driver.find_element_by_id(self.root_id). \
            find_element_by_xpath(self.selected_project_xpath).text
        if project == selected_project:
            return

        self.open_list()
        projects = self.driver.find_element_by_id(
            self.project_list_id).find_elements_by_tag_name('li')

        for item in projects:
            link = item.find_elements_by_xpath('//a')
            if len(link) > 0:
                if link[1].text == project:
                    link[1].click()
                    return

        message = 'No such project in list: ' + project
        raise AssertionError(message=message)