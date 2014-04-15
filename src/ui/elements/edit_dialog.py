from yopenstackqe_tests.common.utils.ui.elements.confirmation_dialog import \
    ConfirmationDialog


class EditDialog(ConfirmationDialog):
    confirm_button_css = "#modal_wrapper input.btn.btn-primary"
    name_id = 'id_name'

    def __init__(self, driver):
        super(EditDialog, self).__init__(driver)

    def set_name(self, name):
        self.driver.find_element_by_id(self.name_id).send_keys(name)
