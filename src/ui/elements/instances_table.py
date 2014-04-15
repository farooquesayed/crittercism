from yopenstackqe_tests.common.utils.ui.elements.edit_dialog import EditDialog
from yopenstackqe_tests.common.utils.ui.elements.editable_table \
    import EditableTable
from yopenstackqe_tests.common.utils.ui.elements.launch_dialog \
    import LaunchDialog
from yopenstackqe_tests.common.utils.ui.elements.more_actions_dropdown \
    import MoreActionsDropdown
from yopenstackqe_tests.common.utils.ui.elements.snapshots_table import \
    SnapshotsTable


class InstancesTable(EditableTable):
    root_id = 'instances'
    delete_item_id = 'instances__action_terminate'

    launch_instance_id = 'instances__action_launch'
    snapshot_button_css = "a[id*='action_snapshot']"

    def __init__(self, driver):
        super(InstancesTable, self).__init__(driver)

    def _name_css(self, i):
        """ Returns xpath for instance name element for i-th line of the table.
        i starts from 1
        """
        return self.table_row_css + ':nth-child(' + str(i) + ') td>a'

    def _status_css(self, i):
        """ Returns xpath for instance status element for i-th line of the
        table. i starts from 1
        """
        return self.table_row_css + ':nth-child(' + str(
            i) + ') td:nth-child(6)'

    def _checkbox_css(self, i):
        """ Returns xpath for checkbox element for i-th line of the table.
        i starts from 1
        """
        return self.table_row_css + ':nth-child(' + str(
            i) + ') td>input'

    def _ip_css(self, i):
        """ Returns xpath for instance IP element for i-th line of the table.
        i starts from 1
        """
        return self.table_row_css + ':nth-child(' + str(i) + ') td ul'

    def click_launch(self):
        self.driver.find_element_by_id(self.launch_instance_id).click()
        LaunchDialog.wait_for_visible(self.driver)

    def get_instance_ip(self, name):
        table = self.driver.find_element_by_id(self.root_id)
        index = self.find_item_by_name(name)
        return table.find_element_by_css_selector(self._ip_css(index)).text

    def terminate_instance_using_actions(self, name):
        index = self.find_item_by_name(name)
        actions = MoreActionsDropdown(self.driver, self._table_row_css(index))
        actions.click_terminate()

        self.confirm.click_submit()

    def reboot_vm(self, name):
        index = self.find_item_by_name(name)
        actions = MoreActionsDropdown(self.driver, self._table_row_css(index))
        actions.click_reboot()

        self.confirm.click_submit()

    def create_snapshot(self, instance_name, snapshot_name,
                        wait_for_active=True):
        current_url = self.driver.current_url
        index = self.find_item_by_name(instance_name)
        self.driver.find_element_by_css_selector(
            self._table_row_css(index)).find_element_by_css_selector(
            self.snapshot_button_css).click()

        snapshot_dialog = EditDialog(self.driver)
        snapshot_dialog.wait_for_visible()
        snapshot_dialog.set_name(snapshot_name)
        snapshot_dialog.click_submit()
        self.waiter.wait_until_page_changed(current_url)

        if wait_for_active:
            snapshots_table = SnapshotsTable(self.driver)
            snapshots_table.wait_for_item_appears(snapshot_name)
            snapshots_table.wait_for_active_status(snapshot_name, 240, 5)



