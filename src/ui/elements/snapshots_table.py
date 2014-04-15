from yopenstackqe_tests.common.utils.ui.elements.editable_table \
    import EditableTable
from yopenstackqe_tests.common.utils.ui.elements.more_actions_dropdown import \
    MoreActionsDropdown


class SnapshotsTable(EditableTable):
    root_id = 'snapshots'
    delete_item_id = 'snapshots__action_delete'

    def __init__(self, driver, timeout=240, poll_period=2):
        super(SnapshotsTable, self).__init__(driver, timeout, poll_period)

    def _name_css(self, i):
        """ Returns xpath for instance name element for i-th line of the table.
        i starts from 1
        """
        return self.table_row_css + ':nth-child(' + str(
            i) + ') td>a'

    def _status_css(self, i):
        """ Returns xpath for instance status element for i-th line of the
        table. i starts from 1
        """
        return self.table_row_css + ':nth-child(' + str(
            i) + ') td:nth-child(3)'

    def _launch_button_css(self, i):
        """ Returns css for launch button for i-th line of the table.
        i starts from 1
        """
        return self.table_row_css + ':nth-child(' + str(
            i) + ') td:nth-child(6) a:first-child'

    def _checkbox_css(self, i):
        """ Returns xpath for checkbox element for i-th line of the table.
        i starts from 1
        """
        return self.table_row_css + ':nth-child(' + str(
            i) + ') td>input'

    def delete_snapshot_using_actions(self, name):
        index = self.find_item_by_name(name)
        actions = MoreActionsDropdown(self.driver, self._table_row_css(index))
        actions.click_delete()

        self.confirm.click_submit()
