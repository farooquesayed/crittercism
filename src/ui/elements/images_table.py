from yopenstackqe_tests.common.utils.ui.elements.common_table \
    import CommonTable


class ImagesTable(CommonTable):
    root_id = 'images'

    def __init__(self, driver):
        super(ImagesTable, self).__init__(driver)
        # self.driver = driver
        # self.waiter = Waiter(self.driver, 30, 2)

    def _name_css(self, i):
        """ Returns css for instance name element for i-th line of the table.
        i starts from 1
        """
        return self.table_row_css + ':nth-child(' + str(i) + ') td>a'

    def _status_css(self, i):
        """ Returns css for instance status element for i-th line of the table.
        i starts from 1
        """
        return self.table_row_css + ':nth-child(' + str(
            i) + ') td:nth-child(2)'

    def _launch_button_css(self, i):
        """ Returns css for launch button for i-th line of the table.
        i starts from 1
        """
        return self.table_row_css + ':nth-child(' + str(
            i) + ') td:nth-child(5)>a'
