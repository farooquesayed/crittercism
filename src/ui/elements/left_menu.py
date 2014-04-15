from selenium.webdriver.firefox.webdriver import WebDriver
from yopenstackqe_tests.common.utils.ui.elements.project_switcher import \
    ProjectSwitcher


class LeftMenu(object):
    project_switcher = None

    root_xpath = "//div[@class='sidebar']"
    project_link_xpath = root_xpath + "/div/ul/li/a"
    menu_xpath = "/ul[@class='main_nav']"
    overview_xpath = "/li[1]/a"
    instances_xpath = "/li[2]/a"
    images_xpath = "/li[3]/a"
    access_xpath = "/li[4]/a"

    def __init__(self, driver):
        self.driver = driver
        self.project_switcher = ProjectSwitcher(driver)

    def click_overview(self):
        self.driver.find_element_by_xpath(
            self.root_xpath + self.menu_xpath + self.overview_xpath).click()

    def click_instances(self):
        self.driver.find_element_by_xpath(
            self.root_xpath + self.menu_xpath + self.instances_xpath).click()

    def click_images(self):
        self.driver.find_element_by_xpath(
            self.root_xpath + self.menu_xpath + self.images_xpath).click()

    def click_access(self):
        self.driver.find_element_by_xpath(
            self.root_xpath + self.menu_xpath + self.access_xpath).click()

