from yopenstackqe_tests.common.utils.ui.elements.confirmation_dialog import ConfirmationDialog
from yopenstackqe_tests.common.utils.ui.wait_utils import Waiter


class MoreActionsDropdown(object):
    more_link_css = "a.dropdown-toggle"

    root_css = "ul.dropdown-menu"
    edit_action_css = "a[id*='action_edit']"
    view_log_action_css = "a[id*='action_log']"
    reboot_action_css = "button[id*='action_reboot']"
    terminate_action_css = "button[id*='action_terminate']"
    delete_action_css = "button[id*='action_delete']"

    def __init__(self, driver, parent_css):
        self.driver = driver
        self.waiter = Waiter(driver, 20, 1)
        self.parent_css = parent_css
        self.confirm = ConfirmationDialog(self.driver)

    def wait_for_visible(self):
        """ This method waits until More actions dropdown becomes visible
        """
        self.waiter.wait_until_visible_by_css(
            self.parent_css + ' ' + self.root_css)

    def open_dropdown(self):
        button_class = self.driver.find_element_by_css_selector(
            self.parent_css).find_element_by_css_selector(
            self.more_link_css).find_element_by_xpath(
            '..').get_attribute('class')
        if not 'open' in button_class:
            self.driver.find_element_by_css_selector(
                self.parent_css).find_element_by_css_selector(
                self.more_link_css).click()
            self.wait_for_visible()

    def click_edit(self):
        self.open_dropdown()
        self.driver.find_element_by_css_selector(
            self.parent_css).find_element_by_css_selector(
            self.edit_action_css).click()
        self.confirm.wait_for_visible()

    def click_view_log(self):
        current_url = self.driver.current_url
        self.open_dropdown()
        self.driver.find_element_by_css_selector(
            self.parent_css).find_element_by_css_selector(
            self.view_log_action_css).click()
        self.waiter.wait_until_page_changed(current_url)

    def click_reboot(self):
        self.open_dropdown()
        self.driver.find_element_by_css_selector(
            self.parent_css).find_element_by_css_selector(
            self.reboot_action_css).click()
        self.confirm.wait_for_visible()

    def click_terminate(self):
        self.open_dropdown()
        self.driver.find_element_by_css_selector(
            self.parent_css).find_element_by_css_selector(
            self.terminate_action_css).click()
        self.confirm.wait_for_visible()

    def click_delete(self):
        self.open_dropdown()
        self.driver.find_element_by_css_selector(
            self.parent_css).find_element_by_css_selector(
            self.delete_action_css).click()
        self.confirm.wait_for_visible()
