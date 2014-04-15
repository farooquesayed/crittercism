from selenium.webdriver.support.select import Select
from yopenstackqe_tests.common.utils.ui.wait_utils import Waiter


class InstanceSource(object):
    """ Values for "Instance Source" dropdown list
    """
    IMAGE = 'image_id'
    SNAPSHOT = 'instance_snapshot_id'


class LaunchDialog(object):
    root_css = "div.workflow.modal.hide.in.dropdown_fix"
    instance_source_id = 'id_source_type'
    image_id = 'id_image_id'
    snapshot_id = 'id_instance_snapshot_id'
    instance_name_id = 'id_name'
    flavor_id = 'id_flavor'
    launch_button_css = "input.btn.btn-primary.pull-right"

    user_data_link_css = 'a[href="#launch_instance__customizeaction"]'
    custom_script_id = "id_customization_script"

    def __init__(self, driver, root_css=None):
        self.driver = driver
        self.waiter = Waiter(driver, 20, 1)
        if root_css:
            self.root_css = root_css

    @classmethod
    def wait_for_visible(cls, driver):
        """ This method waits until Launch dialog becomes visible
        """
        waiter = Waiter(driver, 20, 1)

        waiter.wait_until_exist_by_id(LaunchDialog.instance_source_id)
        waiter.wait_until_visible_by_id(LaunchDialog.instance_source_id)

    def select_instance_source(self, source=InstanceSource.IMAGE):
        select = Select(
            self.driver.find_element_by_id(self.instance_source_id))
        select.select_by_value(source)

    def select_image(self, image_name='Select Image'):
        select = Select(
            self.driver.find_element_by_id(self.image_id))
        select.select_by_visible_text(image_name)

    def select_snapshot(self, snapshot_name='Select Instance Snapshot'):
        select = Select(
            self.driver.find_element_by_id(self.snapshot_id))
        select.select_by_visible_text(snapshot_name)

    def set_instance_name(self, name):
        self.driver.find_element_by_id(self.instance_name_id).send_keys(name)

    def select_flavor(self, flavor_name):
        select = Select(
            self.driver.find_element_by_id(self.flavor_id))
        select.select_by_visible_text(flavor_name)

    def set_user_script(self, script):
        self.driver.find_element_by_css_selector(
            self.root_css).find_element_by_css_selector(
            self.user_data_link_css).click()
        scr_str = "$('#" + self.custom_script_id + "').val('" + script.replace(
            '\n', '\\n') + "')"
        self.driver.execute_script(scr_str)

    def submit_form(self):
        self.driver.find_element_by_css_selector(
            self.root_css).find_element_by_css_selector(
            self.launch_button_css).click()

        self.waiter.wait_until_not_exist_by_css(self.root_css)

    def launch_instance(
            self, instance_source, image, instance_name, flavor, script):
        if instance_source:
            self.select_instance_source(instance_source)
        if (instance_source == InstanceSource.IMAGE):
            if image:
                self.select_image(image)
        elif (instance_source == InstanceSource.SNAPSHOT):
            if image:
                self.select_snapshot(image)
        self.set_instance_name(instance_name)
        self.select_flavor(flavor)
        if script:
            self.set_user_script(script)
        self.submit_form()

