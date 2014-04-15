import abc
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.webdriver import WebDriver
from yopenstackqe_tests.common.utils.common_utils import wait_for_event
from yopenstackqe_tests.common.utils.ui.elements.common_table \
    import CommonTable
from yopenstackqe_tests.common.utils.ui.elements.confirmation_dialog \
    import ConfirmationDialog


class EditableTable(CommonTable):
    messages_balloons_css = "div.messages>div"

    @abc.abstractproperty
    def delete_item_id(self):
        pass

    def __init__(self, driver, timeout=30, poll_period=2):
        super(EditableTable, self).__init__(driver, timeout, poll_period)
        self.confirm = ConfirmationDialog(self.driver)

    @abc.abstractmethod
    def _checkbox_css(self, index):
        pass

    def _messages_balloon_css(self, i):
        return self.messages_balloons_css + ':nth-child(' + str(i) + ')'


    def click_terminate(self):
        # Messages balloon can hide Terminate button so click on it can fail.
        # Wait for this balloon become hidden.
        self.wait_until_balloons_disappear()
        self.driver.find_element_by_id(self.delete_item_id).click()
        self.confirm.wait_for_visible()

    def delete_item(self, name):
        self.check_item(name)
        self.click_terminate()
        self.confirm.click_submit()

    def delete_items(self, names):
        for name in names:
            self.check_item(name)
        self.click_terminate()
        self.confirm.click_submit()

    def check_item(self, name):
        index = self.find_item_by_name(name)
        if index != -1:
            table = self.driver.find_element_by_id(self.root_id)
            table.find_element_by_css_selector(
                self._checkbox_css(index)).click()

    def wait_until_balloons_disappear(self):
        balloon_number = len(self.driver.find_elements_by_css_selector(
            self.messages_balloons_css))
        for i in range(balloon_number):
            self.waiter.wait_until_not_visible_by_css(
                self._messages_balloon_css(i+1), pool_period=1)

    def wait_for_active_status(self, name, timeout=60, poll_period=2):
        self.wait_for_item_appears(name)
        self.wait_for_status(name, 'Active', timeout, poll_period)

    def wait_for_status(self, name, status, timeout=30, pool_period=2):
        index = self.find_item_by_name(name)
        if index == -1:
            raise NoSuchElementException(
                msg="There is no instance with name '%s'" % name)

        wait_for_event(
            timeout, pool_period,
            "Expected status '%s' for VM hasn't been set" % status,
            lambda x: self.get_item_status_by_index(x) == status, index)

    def wait_for_item_appears(self, name):
        wait_for_event(10, 1, "Instance '%s' hasn't appeared" % name,
                       lambda x: self.contains_item(x) == True, name)

    def wait_for_item_disappears(self, name):
        wait_for_event(30, 2, "Instance '%s' hasn't disappeared",
                       lambda x: not (self.contains_item(x)), name)
