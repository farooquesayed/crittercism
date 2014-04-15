from yopenstackqe_tests.common.utils.ui.wait_utils import Waiter


class ConfirmationDialog(object):
    confirm_popup_css = "div.modal.hide.in"
    confirm_button_css = "#modal_wrapper a.btn.btn-primary"

    def __init__(self, driver):
        self.driver = driver
        self.waiter = Waiter(driver, 30, 1)

    def wait_for_visible(self):
        """ This method waits until Launch dialog becomes visible
        """
        self.waiter.wait_until_exist_by_css(self.confirm_button_css)
        self.waiter.wait_until_visible_by_css(self.confirm_button_css)

    def click_submit(self):
        self.driver.find_element_by_css_selector(
            self.confirm_button_css).click()

        self.waiter.wait_until_not_exist_by_css(
            self.confirm_popup_css)
