from selenium.webdriver.firefox.webdriver import WebDriver
from yopenstackqe_tests import config
from yopenstackqe_tests.common.utils.ui.elements.images_table \
    import ImagesTable
from yopenstackqe_tests.common.utils.ui.elements.launch_dialog \
    import LaunchDialog
from yopenstackqe_tests.common.utils.ui.elements.left_menu import LeftMenu
from yopenstackqe_tests.common.utils.ui.elements.snapshots_table \
    import SnapshotsTable
from yopenstackqe_tests.common.utils.ui.wait_utils import Waiter


class ImagesPage:
    page_url = config.BrowserConfig().browser.horizon_url + \
               "/project/images_and_snapshots/"


    def __init__(self, driver):
        self.driver = driver
        self.left_menu = LeftMenu(driver)
        self.images_table = ImagesTable(driver)
        self.snapshots_table = SnapshotsTable(driver)
        self.launch_dialog = LaunchDialog(driver)
        self.waiter = Waiter(driver, 30, 1)

    def get(self):
        self.driver.get(self.page_url)

    def launch_instance_from_image(
            self, image_name, instance_name, flavor, script=None):
        self.images_table.click_launch_item(image_name)
        self.launch_dialog.launch_instance(
            None, None, instance_name, flavor, script)
        self.waiter.wait_until_page_changed(self.page_url)

    def launch_instance_from_snapshot(
            self, snapshot_name, instance_name, flavor, script=None):
        self.snapshots_table.click_launch_item(snapshot_name)
        self.launch_dialog.launch_instance(
            None, None, instance_name, flavor, script)
        self.waiter.wait_until_page_changed(self.page_url)

    def delete_snapshot_using_actions(self, name):
        self.snapshots_table.delete_snapshot_using_actions(name)

    def delete_snapshot(self, name):
        self.snapshots_table.delete_item(name)

    def delete_snapshots(self, names):
        self.snapshots_table.delete_items(names)
