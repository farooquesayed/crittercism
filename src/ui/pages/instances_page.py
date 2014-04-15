from selenium.webdriver.firefox.webdriver import WebDriver
from yopenstackqe_tests import config
from yopenstackqe_tests.common.utils.ui.elements.instances_table import \
    InstancesTable
from yopenstackqe_tests.common.utils.ui.elements.launch_dialog import \
    LaunchDialog
from yopenstackqe_tests.common.utils.ui.elements.left_menu import \
    LeftMenu


class InstancesPage:
    page_url = config.BrowserConfig().browser.horizon_url + \
               "/project/instances/"

    def __init__(self, driver):
        self.driver = driver
        self.left_menu = LeftMenu(driver)
        self.instances_table = InstancesTable(driver)
        self.launch_dialog = LaunchDialog(driver)

    def get(self):
        self.driver.get(self.page_url)

    def launch_instance(
            self, instance_source, image, instance_name, flavor, script=None):
        self.instances_table.click_launch()
        self.launch_dialog.launch_instance(
            instance_source, image, instance_name, flavor, script)

    def terminate_instance_using_actions(self, name):
        self.instances_table.terminate_instance_using_actions(name)

    def terminate_instance(self, name):
        self.instances_table.delete_item(name)

    def terminate_instances(self, names):
        self.instances_table.delete_items(names)
