import abc
from selenium.common.exceptions import NoSuchElementException
from yopenstackqe_tests.common.utils.ui.elements.launch_dialog import \
    LaunchDialog
from yopenstackqe_tests.common.utils.ui.wait_utils import Waiter


class CommonTable(object):
    @abc.abstractproperty
    def root_id(self):
        pass

    @property
    def table_row_css(self):
        # self.table_row_css = "#" + self.root_id + ">tbody>tr"
        return "#" + self.root_id + ">tbody>tr"

    def __init__(self, driver, timeout=30, poll_period=2):
        self.driver = driver
        self.waiter = Waiter(self.driver, timeout, poll_period)

    @abc.abstractmethod
    def _name_css(self, index):
        pass

    @abc.abstractmethod
    def _launch_button_css(self, index):
        pass

    @abc.abstractmethod
    def _status_css(self, index):
        pass

    def _table_row_css(self, i):
        """ Returns xpath for instance name element for i-th line of the table.
        i starts from 1
        """
        return self.table_row_css + ':nth-child(' + str(i) + ') '

    def click_launch_item(self, name):
        index = self.find_item_by_name(name)
        if index != -1:
            self.driver.find_element_by_css_selector(
                self._launch_button_css(index)).click()
            LaunchDialog.wait_for_visible(self.driver)

    def find_item_by_name(self, name):
        """ Returns index of an item with the given name in the table.
        Index starts from 1.
        """
        row = self.driver.find_elements_by_css_selector(self._name_css(1))

        i = 1
        while (len(row) > 0):
            if (row[0].text == name):
                return i
            i += 1
            row = self.driver.find_elements_by_css_selector(self._name_css(i))

        return -1

    def contains_item(self, name):
        return self.find_item_by_name(name) != -1

    def get_item_status(self, name):
        index = self.find_item_by_name(name)
        if index == -1:
            raise NoSuchElementException(msg="No image with '%s' name" % name)
        return self.get_item_status_by_index(index)

    def get_item_status_by_index(self, index):
        table = self.driver.find_element_by_id(self.root_id)
        return table.find_element_by_css_selector(self._status_css(index)).text
