import os
from os.path import expanduser
import re
import time
import traceback

import sys

import unittest2 as unittest


#from nose.tools import with_setup
from nose.plugins.attrib import attr
from yopenstackqe_tests.common.utils.linux import ExecuteCommands
from yopenstackqe_tests.common.utils import yLogger
from yopenstackqe_tests.common.utils.data_utils import rand_name
from yopenstackqe_tests.common.utils.linux.remote_client import RemoteClient
from yopenstackqe_tests import config
from yopenstackqe_tests.common.utils.vm_utils import VirtualMachine
from yopenstackqe_tests.services.common import valHdlr
from yopenstackqe_tests.services.osNative import servers_client
from yopenstackqe_tests.services.osNative import opParser
from yopenstackqe_tests.services.osNative import novaCommands
from yopenstackqe_tests.common.utils.linux.remote_client import RemoteClient
from yopenstackqe_tests import config
from yopenstackqe_tests.common.utils.data_driven_test_wrapper import data, data_driven_test, ddt_list


logger = yLogger.setup_custom_logger(__name__)

def generate_list_of_images_and_flavors_new():
    images_flavors_list = []

    # Get all the images from the nova
    resp = novaCommands.NovaImageList().execute()
    novaImageListBO = opParser.NovaImageList(data=resp['stdOut']).get()

    # Get all the flavor
    resp = novaCommands.NovaFlavorList().execute()
    flavListBO = opParser.NovaFlavorList(data=resp['stdOut']).get()

    for imageItem in novaImageListBO:
        # filter out *-initrd and *-vmlinuz images (may change in the future)
        if ((imageItem.name.find("-initrd") >= 0) or (imageItem.name.find("-vmlinuz") >= 0) or (
                    imageItem.name.find("ylinux") < 0) ):
            logger.debug(
                "Skipping the image %s because it has image name *-initrd or *-vmlinuz or not a ylinux image" % imageItem.name)
            continue

        if (imageItem.status.find("ACTIVE") < 0):
            logger.debug("Skipping the image as state is not ACTIVE instead " + str(imageItem.status))
            continue;

        logger.debug("test_nova_boot_all_images: " + imageItem.name + " ...")
        #VMsToDelete = []
        for aFlav in flavListBO:
            # creating dict where key is concatenation of image and flavor names
            # value is a tuple of ImageBO and FlavorBO
            image_name = imageItem.name.replace(" ", "_").replace(".", "_")
            flavor_name = aFlav.name.replace(" ", "_").replace(".", "_")
            images_flavors_list.append({str("%s_%s" % (str(image_name), str(flavor_name))):
                                        (imageItem, aFlav)})
    return images_flavors_list


@data_driven_test
class NovaBootTestSuite(baseTest.BaseCliTest):
    #_multiprocess_can_split = True
    _multiprocess_shared_ = True
    username = config.CliConfig().compute.username
    password = config.CliConfig().compute.password
    tenant_name = config.CliConfig().compute.tenant_name
    auth_url = config.CliConfig().osNative.OS_AUTH_URL

    image_ref = config.CliConfig().defaultImage

    user_data = config.CliConfig().compute.user_data
    env = os.environ
    identity_auth_url = config.CliConfig().identity.auth_url
    yahoo_opsdb_property = config.CliConfig().compute.yahoo_opsdb_property
    data_location = config.CliConfig().compute.data_location
    yahoo_ssh_user = config.CliConfig().compute.yahoo_ssh_user
    key_filename = config.CliConfig().compute.key_filename
    flavor_ref = config.CliConfig().compute.flavor_ref
    custom_hostname = config.CliConfig().compute.custom_hostname
    yrole = config.CliConfig().compute.yrole
    roles_host = config.CliConfig().compute.roles_host
    aSmallFlavor = None

    @classmethod
    def setUpClass(self):
        super(NovaBootTestSuite, self).setUpClass()

    def setUp(self):
        #Can override the base class setUp here
        pass

    def tearDown(self):
        #Can override the base class setUp here
        pass

    @attr(genre='NOVA-BOOT', smoke='TRUE', aria='TRUE')
    def test_vm_boot_delete(self):
        __name__ + """[Test] test_quick_check """

        vmName = rand_name(config.CliConfig().identity.aria_vm_name)
        #NOVA BOOT
        resp = novaCommands.NovaBoot(name=vmName).execute(debug=True)
        self.log_assert(resp['retCode'], 0, "Nova boot exited with a non-zero return value \n"
                                            + str(resp['stdErr']) + '\n' + str(resp['stdOut']))

        # novaBootBO = opParser.NovaBoot(resp['stdOut']).get()
        # servClient = servers_client.ServersClientJSON(config.CliConfig(),
        #             NovaBootTestSuite.username,
        #             NovaBootTestSuite.password,
        #             NovaBootTestSuite.identity_auth_url,
        #             NovaBootTestSuite.tenant_name)
        # logger.info(novaBootBO.id)
        # resp, server = servClient.get_server(novaBootBO.id)
        # logger.info(server)
        #
        # #Get a linux client, to remote SSH into the VM
        # linux_client = RemoteClient(server,
        #             self.config.compute.yahoo_ssh_user,
        #             look_for_keys=True,
        #             key_filename=self.config.compute.key_filename)
        #
        # #Make sure that the linux client can authenticate
        # self.assertTrue(linux_client.can_authenticate())


        #NOVA DELETE
        resp = novaCommands.NovaDelete(ids=[vmName]).execute()
        self.log_assert(resp['retCode'], 0, "Nova delete exited with a non-zero return value \n"
                                            + str(resp['stdErr']) + '\n' + str(resp['stdOut']))


    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT', smoke='TRUE', fp="TRUE")
    def test_nova_boot_no_poll(self):
        __name__ + " Boot without polling"

        logger.info("[Test]test_nova_boot_no_poll ")

        #NOVA BOOT
        resp = novaCommands.NovaBoot(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            #flavor=NovaBootTestSuite.aSmallFlavor.id,
            flavor=NovaBootTestSuite.flavor_ref,
            image=NovaBootTestSuite.image_ref,
            user_data=NovaBootTestSuite.user_data,
            poll=False,
            name=rand_name("auto"),
            cwd=None,
            env=NovaBootTestSuite.env).execute()
        self.assertEqual(resp['retCode'], 0, "Nova boot exited with a non-zero return value \n"
                                             + str(resp['stdErr']) + '\n' + str(resp['stdOut']))

        novaBootBO = opParser.NovaBoot(resp['stdOut']).get()
        logger.info(NovaBootTestSuite.tenant_name)
        servClient = servers_client.ServersClientJSON(config.CliConfig(),
                                                      NovaBootTestSuite.username,
                                                      NovaBootTestSuite.password,
                                                      NovaBootTestSuite.identity_auth_url,
                                                      NovaBootTestSuite.tenant_name)
        resp, server = servClient.get_server(novaBootBO.id)
        logger.info(server)

        #Get a linux client, to remote SSH into the VM
        linux_client = RemoteClient(server,
                                    NovaBootTestSuite.yahoo_ssh_user,
                                    look_for_keys=True,
                                    key_filename=NovaBootTestSuite.key_filename)

        #Make sure that the linux client can authenticate
        self.assertTrue(linux_client.can_authenticate())

        #Validate
        valHdlr.Validator(linux_client=linux_client,
                          customHostName=None,
                          #flavorRef=NovaBootTestSuite.aSmallFlavor.id,
                          flavorRef=NovaBootTestSuite.flavor_ref,
                          opsDbProperty=None,
                          novaBootBO=novaBootBO,
                          createYroot=True
        ).validate()
        """
        #Reboot the VM to make sure it rebooted and pingable
        resp = novaCommands.NovaReboot(
                   username=NovaBootTestSuite.username,
                   password=NovaBootTestSuite.password,
                   tenant_name=NovaBootTestSuite.tenant_name,
                   os_auth_url=NovaBootTestSuite.auth_url,
                   name=novaBootBO.id,
                   cwd=None,
                   env=NovaBootTestSuite.env
                   ).execute()
        #TODO : Add Validation to check VM is in ACTIVE state

        time.sleep(30) # Because not waiting can cause VM to remain in shut off state
        
        # SSH to the VM which is rebooted
        linux_client = RemoteClient(server,
                   NovaBootTestSuite.yahoo_ssh_user,
                   look_for_keys=True,
                   key_filename=NovaBootTestSuite.key_filename)

        #Make sure that the linux client can authenticate
        self.assertTrue(linux_client.can_authenticate())


        #Reboot the VM to make sure it rebooted and pingable
        resp = novaCommands.NovaStop(
                   username=NovaBootTestSuite.username,
                   password=NovaBootTestSuite.password,
                   tenant_name=NovaBootTestSuite.tenant_name,
                   os_auth_url=NovaBootTestSuite.auth_url,
                   name=novaBootBO.id,
                   cwd=None,
                   env=NovaBootTestSuite.env
                   ).execute()

        time.sleep(30) # Because not waiting can cause VM to remain in shut off state

        resp = novaCommands.NovaStart(
                   username=NovaBootTestSuite.username,
                   password=NovaBootTestSuite.password,
                   tenant_name=NovaBootTestSuite.tenant_name,
                   os_auth_url=NovaBootTestSuite.auth_url,
                   name=novaBootBO.id,
                   cwd=None,
                   env=NovaBootTestSuite.env
                   ).execute()

        # SSH to the VM which is rebooted
        linux_client = RemoteClient(server,
                   NovaBootTestSuite.yahoo_ssh_user,
                   look_for_keys=True,
                   key_filename=NovaBootTestSuite.key_filename)

        #Make sure that the linux client can authenticate
        self.assertTrue(linux_client.can_authenticate())
        
        #Doing Validation again to make sure on reboot it still works
        valHdlr.Validator(linux_client=linux_client,
                    customHostName=None,
                    #flavorRef=NovaBootTestSuite.aSmallFlavor.id,
                    flavorRef=NovaBootTestSuite.flavor_ref,
                    opsDbProperty=None,
                    novaBootBO=novaBootBO,
                    createYroot=True
                    ).validate()
        """
        #NOVA DELETE
        resp = novaCommands.NovaDelete(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            ids=[novaBootBO.id],
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0)

        #Validate
        valHdlr.Validator(novaBootBO=novaBootBO).validateAfterDelete()

    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT')
    #@unittest.skip("ERROR: custom hostnames are disabled (HTTP 400)")
    def test_nova_boot_custom_hostname(self):
        self.__class__.__name__
        logger.info("[Test]test_nova_boot_custom_hostname ")
        #NOVA BOOT
        #custom_hostname = str(rand_name("customhostname") + ".qe.yahoo.com")
        custom_hostname = "%s.%s" % (rand_name("custom"), NovaBootTestSuite.custom_hostname)
        resp = novaCommands.NovaBoot(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            flavor=NovaBootTestSuite.flavor_ref,
            image=NovaBootTestSuite.image_ref,
            user_data=NovaBootTestSuite.user_data,
            poll=True,
            hostname=custom_hostname,
            name=rand_name("auto"),
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0, "Nova boot exited with a non-zero return value \n"
                                             + str(resp['stdErr']) + '\n' + str(resp['stdOut']))

        novaBootBO = opParser.NovaBoot(resp['stdOut']).get()

        servClient = servers_client.ServersClientJSON(config.CliConfig(),
                                                      NovaBootTestSuite.username,
                                                      NovaBootTestSuite.password,
                                                      NovaBootTestSuite.identity_auth_url,
                                                      NovaBootTestSuite.tenant_name)
        logger.info(novaBootBO.id)
        resp, server = servClient.get_server(novaBootBO.id)
        logger.info(server)

        #Get a linux client, to remote SSH into the VM
        linux_client = RemoteClient(server,
                                    self.config.compute.yahoo_ssh_user,
                                    look_for_keys=True,
                                    key_filename=self.config.compute.key_filename)

        #Make sure that the linux client can authenticate
        self.assertTrue(linux_client.can_authenticate())

        #Validate
        valHdlr.Validator(linux_client=linux_client,
                          #customHostName='auto-cstm.qe.yahoo.com',
                          customHostName=custom_hostname,
                          #flavorRef=NovaBootTestSuite.aSmallFlavor.id,
                          flavorRef=NovaBootTestSuite.flavor_ref,
                          opsDbProperty=None,
                          novaBootBO=novaBootBO,
                          createYroot=False).validate()

        #NOVA DELETE
        resp = novaCommands.NovaDelete(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            ids=[novaBootBO.id],
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0)

        #Validate
        valHdlr.Validator(novaBootBO=novaBootBO).validateAfterDelete()


    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT')
    def test_nova_boot_duplicate_custom_hostname(self):
        self.__class__.__name__

        logger.info("[Test]test_nova_boot_custom_hostname ")
        #NOVA BOOT
        #custom_hostname = str(rand_name("customhostname") + ".qe.yahoo.com")
        custom_hostname = "%s.%s" % (rand_name("custom"), NovaBootTestSuite.custom_hostname)
        vmName = rand_name("auto")
        resp = novaCommands.NovaBoot(
            hostname=custom_hostname,
            name=vmName,
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0, "Nova boot exited with a non-zero return value \n"
                                             + str(resp['stdErr']) + '\n' + str(resp['stdOut']))

        resp = novaCommands.NovaBoot(
            hostname=custom_hostname,
            name=rand_name("auto"),
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], -1, "Able to boot 2 VMs with same custom hostname \n"
                                              + str(resp['stdErr']) + '\n' + str(resp['stdOut']))


        #NOVA DELETE
        resp = novaCommands.NovaDelete(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            name=vmName,
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0)


    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT', p3="TRUE")
    #@unittest.skip("Temporary")
    def test_nova_boot_copy_5_files(self):
        self.__class__.__name__
        logger.info("[Test]test_nova_boot_copy_5_files ")
        fileArg = ''
        for index in range(1, 6):
            fileArg = fileArg + "--file" + " " + "/tmp/copy" + str(index) \
                      + ".txt=" + NovaBootTestSuite.data_location \
                      + "/" + "copy" + str(index) + ".txt"
            #NOVA BOOT
        resp = novaCommands.NovaBoot(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            #flavor=NovaBootTestSuite.aSmallFlavor.id,
            flavor=NovaBootTestSuite.flavor_ref,
            image=NovaBootTestSuite.image_ref,
            user_data=NovaBootTestSuite.user_data,
            poll=True,
            name=rand_name("auto"),
            file=fileArg,
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0, "Nova boot exited with a non-zero return value \n"
                                             + str(resp['stdErr']) + '\n' + str(resp['stdOut']))

        novaBootBO = opParser.NovaBoot(resp['stdOut']).get()

        servClient = servers_client.ServersClientJSON(config.CliConfig(),
                                                      NovaBootTestSuite.username,
                                                      NovaBootTestSuite.password,
                                                      NovaBootTestSuite.identity_auth_url,
                                                      NovaBootTestSuite.tenant_name)
        logger.info(novaBootBO.id)
        resp, server = servClient.get_server(novaBootBO.id)
        logger.info(server)

        #Get a linux client, to remote SSH into the VM
        linux_client = RemoteClient(server,
                                    self.config.compute.yahoo_ssh_user,
                                    look_for_keys=True,
                                    key_filename=self.config.compute.key_filename)

        #Get the contents of the copied file
        data = linux_client.get_contentsOfCopiedFiles(files='/tmp/copy*.txt')
        data = data.split('\n')
        data = "".join(data)

        for num in range(1, 5):
            pat = str(num) * 5
            self.assertTrue(re.search(pat, data) is not None)

        #Make sure that the linux client can authenticate
        self.assertTrue(linux_client.can_authenticate())

        #Validate
        valHdlr.Validator(linux_client=linux_client,
                          customHostName=None,
                          #flavorRef=NovaBootTestSuite.aSmallFlavor.id,
                          flavorRef=NovaBootTestSuite.flavor_ref,
                          opsDbProperty=None,
                          novaBootBO=novaBootBO,
                          createYroot=False).validate()

        #NOVA DELETE
        resp = novaCommands.NovaDelete(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            ids=[novaBootBO.id],
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0)

        #Validate
        valHdlr.Validator(novaBootBO=novaBootBO).validateAfterDelete()

    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT')
    #@unittest.skip("Already run")
    def test_nova_boot_copy_1_file(self):
        """[Test] test_nova_boot_copy__1_file """
        logger.info("[Test]test_nova_boot_copy_1_file ")
        fileArg = ''
        for index in range(1, 2):
            fileArg = fileArg + "--file" + " " + "/tmp/copy" + str(index) \
                      + ".txt=" + NovaBootTestSuite.data_location \
                      + "/" + "copy" + str(index) + ".txt"
            #NOVA BOOT
        resp = novaCommands.NovaBoot(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            #flavor=NovaBootTestSuite.aSmallFlavor.id,
            flavor=NovaBootTestSuite.flavor_ref,
            image=NovaBootTestSuite.image_ref,
            user_data=NovaBootTestSuite.user_data,
            poll=True,
            name=rand_name("auto"),
            file=fileArg,
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0, "Nova boot exited with a non-zero return value \n"
                                             + str(resp['stdErr']) + '\n' + str(resp['stdOut']))

        novaBootBO = opParser.NovaBoot(resp['stdOut']).get()

        servClient = servers_client.ServersClientJSON(config.CliConfig(),
                                                      NovaBootTestSuite.username,
                                                      NovaBootTestSuite.password,
                                                      NovaBootTestSuite.identity_auth_url,
                                                      NovaBootTestSuite.tenant_name)
        logger.info(novaBootBO.id)
        resp, server = servClient.get_server(novaBootBO.id)
        logger.info(server)

        #Get a linux client, to remote SSH into the VM
        linux_client = RemoteClient(server,
                                    self.config.compute.yahoo_ssh_user,
                                    look_for_keys=True,
                                    key_filename=self.config.compute.key_filename)

        #Make sure that the linux client can authenticate
        self.assertTrue(linux_client.can_authenticate())

        #Get the contents of the copied file
        data = linux_client.get_contentsOfCopiedFiles(files='/tmp/copy*.txt')
        data = data.split('\n')
        data = "".join(data)

        for num in range(1, 2):
            pat = str(num) * 5
            self.assertTrue(re.search(pat, data) is not None)

        #Validate
        valHdlr.Validator(linux_client=linux_client,
                          customHostName=None,
                          #flavorRef=NovaBootTestSuite.aSmallFlavor.id,
                          flavorRef=NovaBootTestSuite.flavor_ref,
                          opsDbProperty=None,
                          novaBootBO=novaBootBO,
                          createYroot=False).validate()

        #NOVA DELETE
        resp = novaCommands.NovaDelete(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            ids=[novaBootBO.id],
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0)

    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT')
    #@unittest.skip("Temporary")
    def test_nova_boot_copy_file_diff_name(self):
        """[Test] test_nova_boot_copy_file_diff_name """
        logger.info("[Test]test_nova_boot_copy_file_diff_name ")
        fileArg = ''
        for index in range(1, 6):
            fileArg = fileArg + "--file" + " " + "/home/auto/copyyyy" + str(index) \
                      + ".txt=" + NovaBootTestSuite.data_location \
                      + "/" + "copy" + str(index) + ".txt"
            #NOVA BOOT
        resp = novaCommands.NovaBoot(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            #flavor=NovaBootTestSuite.aSmallFlavor.id,
            flavor=NovaBootTestSuite.flavor_ref,
            image=NovaBootTestSuite.image_ref,
            user_data=NovaBootTestSuite.user_data,
            poll=True,
            name=rand_name("auto"),
            file=fileArg,
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0, "Nova boot exited with a non-zero return value \n"
                                             + str(resp['stdErr']) + '\n' + str(resp['stdOut']))

        novaBootBO = opParser.NovaBoot(resp['stdOut']).get()

        servClient = servers_client.ServersClientJSON(config.CliConfig(),
                                                      NovaBootTestSuite.username,
                                                      NovaBootTestSuite.password,
                                                      NovaBootTestSuite.identity_auth_url,
                                                      NovaBootTestSuite.tenant_name)
        logger.info(novaBootBO.id)
        resp, server = servClient.get_server(novaBootBO.id)
        logger.info(server)

        #Get a linux client, to remote SSH into the VM
        linux_client = RemoteClient(server,
                                    self.config.compute.yahoo_ssh_user,
                                    look_for_keys=True,
                                    key_filename=self.config.compute.key_filename)

        #Get the contents of the copied file
        data = linux_client.get_contentsOfCopiedFiles(files='/home/auto/copy*.txt')
        data = data.split('\n')
        data = "".join(data)

        for num in range(1, 5):
            pat = str(num) * 5
            self.assertTrue(re.search(pat, data) is not None)

        #Make sure that the linux client can authenticate
        self.assertTrue(linux_client.can_authenticate())

        #Validate
        valHdlr.Validator(linux_client=linux_client,
                          customHostName=None,
                          #flavorRef=NovaBootTestSuite.aSmallFlavor.id,
                          flavorRef=NovaBootTestSuite.flavor_ref,
                          opsDbProperty=None,
                          novaBootBO=novaBootBO,
                          createYroot=False).validate()

        #NOVA DELETE
        resp = novaCommands.NovaDelete(
            ids=[novaBootBO.id],
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0)


    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT')
    def test_scp_file_to_VM_and_back(self):
        #NOVA BOOT
        resp = novaCommands.NovaBoot(name=rand_name("auto")).execute()
        self.assertEqual(resp['retCode'], 0, "Nova boot exited with a non-zero return value \n"
                                             + str(resp['stdErr']) + '\n' + str(resp['stdOut']))

        novaBootBO = opParser.NovaBoot(resp['stdOut']).get()
        servClient = servers_client.ServersClientJSON(config.CliConfig(),
                                                      NovaBootTestSuite.username,
                                                      NovaBootTestSuite.password,
                                                      NovaBootTestSuite.identity_auth_url,
                                                      NovaBootTestSuite.tenant_name)
        resp, server = servClient.get_server(novaBootBO.id)

        #Get a linux client, to remote SSH into the VM
        linux_client = RemoteClient(server,
                                    self.config.compute.yahoo_ssh_user,
                                    look_for_keys=True,
                                    key_filename=self.config.compute.key_filename)

        #Make sure that the linux client can authenticate and ready for ssh
        self.assertTrue(linux_client.can_authenticate())

        MAX_SCP_TIME_SECONDS = 150
        TEST_DATA_FILE_NAME = "/tmp/file_to_scp_to_VM_and_back.txt"
        FILE_SIZE = "2GB"

        #Create a local file to run the test for SCP
        cmd_to_create_test_file = []
        cmd_to_create_test_file.append("truncate")
        cmd_to_create_test_file.append("-s")
        cmd_to_create_test_file.append(FILE_SIZE)
        cmd_to_create_test_file.append(TEST_DATA_FILE_NAME)

        resp = ExecuteCommands.LocalCommands(cmd_to_create_test_file).execute()
        self.assertEqual(resp['retCode'], 0, "Unable to create the test data file " \
                                             + str(resp['stdErr']) + '\n' + str(resp['stdOut']))
        logger.debug("Created File of size = " + FILE_SIZE)
        # From local host to VM
        scp_to_vm = []
        scp_to_vm.append("scp")
        scp_to_vm.append("-i")
        scp_to_vm.append(self.config.compute.key_filename)
        scp_to_vm.append("-o")
        scp_to_vm.append("ConnectTimeout=5")
        scp_to_vm.append("-o")
        scp_to_vm.append("StrictHostKeychecking=no")
        scp_to_vm.append("-o")
        scp_to_vm.append("UserKnownHostsFile=/dev/null")
        scp_to_vm.append(TEST_DATA_FILE_NAME)
        scp_to_vm.append(
            self.config.compute.yahoo_ssh_user + "@" + novaBootBO.default_network + ":" + TEST_DATA_FILE_NAME)

        start = time.time()
        resp = ExecuteCommands.LocalCommands(scp_to_vm).execute()
        elapsed = (time.time() - start)  # Seconds

        self.assertEqual(resp['retCode'], 0, "SCP to VM failed " \
                                             + str(resp['stdErr']) + '\n' + str(resp['stdOut']))

        if elapsed > MAX_SCP_TIME_SECONDS:
            self.assertEqual(1, 0, "SCP to VM took more time to copy then usual. Expected less then " + \
                                   str(MAX_SCP_TIME_SECONDS) + " seconds but took " + str(elapsed))
        # From VM to local host
        scp_from_vm = []
        scp_from_vm.append("scp")
        scp_from_vm.append("-i")
        scp_from_vm.append(self.config.compute.key_filename)
        scp_from_vm.append("-o")
        scp_from_vm.append("ConnectTimeout=5")
        scp_from_vm.append("-o")
        scp_from_vm.append("StrictHostKeychecking=no")
        scp_to_vm.append("-o")
        scp_to_vm.append("UserKnownHostsFile=/dev/null")
        scp_from_vm.append(
            self.config.compute.yahoo_ssh_user + "@" + novaBootBO.default_network + ":" + TEST_DATA_FILE_NAME)
        scp_from_vm.append(TEST_DATA_FILE_NAME)

        start = time.time()
        resp = ExecuteCommands.LocalCommands(scp_from_vm).execute()
        elapsed = (time.time() - start)  # Seconds

        self.assertEqual(resp['retCode'], 0, "SCP from VM failed " \
                                             + str(resp['stdErr']) + '\n' + str(resp['stdOut']))

        if elapsed > MAX_SCP_TIME_SECONDS:
            self.assertEqual(1, 0, "SCP from VM took more time to copy then usual. Expected less then " \
                                   + str(MAX_SCP_TIME_SECONDS) + " seconds but took " + str(elapsed))
        #NOVA DELETE
        resp = novaCommands.NovaDelete(ids=[novaBootBO.id]).execute()
        self.assertEqual(resp['retCode'], 0, "VM delete failed " \
                                             + str(resp['stdErr']) + '\n' + str(resp['stdOut']))


    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT')
    #@unittest.skip("Temporary")
    def test_nova_boot_meta_data(self):
        """[Test] test_nova_boot_meta_data """
        logger.info("[Test]test_nova_boot_meta_data ")
        metaData = {'key1': 'val1',
                    'description': '\'Used for testing\'',
                    'creator': 'automation',
                    'key2': '\'value 2\''}

        #NOVA BOOT
        resp = novaCommands.NovaBoot(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            #flavor=NovaBootTestSuite.aSmallFlavor.id,
            flavor=NovaBootTestSuite.flavor_ref,
            image=NovaBootTestSuite.image_ref,
            user_data=NovaBootTestSuite.user_data,
            poll=True,
            name=rand_name("auto"),
            meta=metaData,
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0, "Nova boot exited with a non-zero return value \n"
                                             + str(resp['stdErr']) + '\n' + str(resp['stdOut']))

        novaBootBO = opParser.NovaBoot(resp['stdOut']).get()

        servClient = servers_client.ServersClientJSON(config.CliConfig(),
                                                      NovaBootTestSuite.username,
                                                      NovaBootTestSuite.password,
                                                      NovaBootTestSuite.identity_auth_url,
                                                      NovaBootTestSuite.tenant_name)
        logger.info(novaBootBO.id)
        resp, server = servClient.get_server(novaBootBO.id)
        logger.info(server)

        #Get a linux client, to remote SSH into the VM
        linux_client = RemoteClient(server,
                                    self.config.compute.yahoo_ssh_user,
                                    look_for_keys=True,
                                    key_filename=self.config.compute.key_filename)

        #Make sure that the linux client can authenticate
        self.assertTrue(linux_client.can_authenticate())

        #Validate
        valHdlr.Validator(linux_client=linux_client,
                          customHostName=None,
                          #flavorRef=NovaBootTestSuite.aSmallFlavor.id,
                          flavorRef=NovaBootTestSuite.flavor_ref,
                          opsDbProperty=None,
                          novaBootBO=novaBootBO,
                          createYroot=False).validate()

        #NOVA DELETE
        resp = novaCommands.NovaDelete(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            ids=[novaBootBO.id],
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0)

    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT')
    #@unittest.skip("Temporary")
    def test_nova_boot_opsdb_argument_1(self):
        """[Test] test_nova_boot_opsdb_argument_1 (--yproperty openstack.us)"""
        logger.info("[Test]test_nova_boot_opsdb_argument_1(--yproperty openstack.us) ")
        #NOVA BOOT
        resp = novaCommands.NovaBoot(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            #flavor=NovaBootTestSuite.aSmallFlavor.id,
            flavor=NovaBootTestSuite.flavor_ref,
            image=NovaBootTestSuite.image_ref,
            user_data=NovaBootTestSuite.user_data,
            poll=True,
            name=rand_name("auto"),
            yproperty='openstack.US',
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0, "Nova boot exited with a non-zero return value \n"
                                             + str(resp['stdErr']) + '\n' + str(resp['stdOut']))

        novaBootBO = opParser.NovaBoot(resp['stdOut']).get()

        servClient = servers_client.ServersClientJSON(config.CliConfig(),
                                                      NovaBootTestSuite.username,
                                                      NovaBootTestSuite.password,
                                                      NovaBootTestSuite.identity_auth_url,
                                                      NovaBootTestSuite.tenant_name)
        logger.info(novaBootBO.id)
        resp, server = servClient.get_server(novaBootBO.id)
        logger.info(server)

        #Get a linux client, to remote SSH into the VM
        linux_client = RemoteClient(server,
                                    self.config.compute.yahoo_ssh_user,
                                    look_for_keys=True,
                                    key_filename=self.config.compute.key_filename)

        #Make sure that the linux client can authenticate
        self.assertTrue(linux_client.can_authenticate())

        #Validate
        valHdlr.Validator(linux_client=linux_client,
                          #flavorRef=NovaBootTestSuite.aSmallFlavor.id,
                          flavorRef=NovaBootTestSuite.flavor_ref,
                          opsDbProperty='openstack.US',
                          novaBootBO=novaBootBO,
                          createYroot=False).validate()

        #NOVA DELETE
        resp = novaCommands.NovaDelete(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            ids=[novaBootBO.id],
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0)

        #Validate
        valHdlr.Validator(novaBootBO=novaBootBO).validateAfterDelete()

    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT')
    #@unittest.skip("Temporary")
    def test_nova_boot_opsdb_argument_2(self):
        """[Test] test_nova_boot_opsdb_argument_2 (--yproperty vm-ops.US)"""
        logger.info("[Test]test_nova_boot_opsdb_argument_2(--yproperty vm-ops.US) ")
        #NOVA BOOT
        resp = novaCommands.NovaBoot(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            #flavor=NovaBootTestSuite.aSmallFlavor.id,
            flavor=NovaBootTestSuite.flavor_ref,
            image=NovaBootTestSuite.image_ref,
            user_data=NovaBootTestSuite.user_data,
            poll=True,
            name=rand_name("auto"),
            yproperty='vm-ops.US',
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0, "Nova boot exited with a non-zero return value \n"
                                             + str(resp['stdErr']) + '\n' + str(resp['stdOut']))

        novaBootBO = opParser.NovaBoot(resp['stdOut']).get()

        servClient = servers_client.ServersClientJSON(config.CliConfig(),
                                                      NovaBootTestSuite.username,
                                                      NovaBootTestSuite.password,
                                                      NovaBootTestSuite.identity_auth_url,
                                                      NovaBootTestSuite.tenant_name)
        logger.info(novaBootBO.id)
        resp, server = servClient.get_server(novaBootBO.id)
        logger.info(server)

        #Get a linux client, to remote SSH into the VM
        linux_client = RemoteClient(server,
                                    self.config.compute.yahoo_ssh_user,
                                    look_for_keys=True,
                                    key_filename=self.config.compute.key_filename)

        #Make sure that the linux client can authenticate
        self.assertTrue(linux_client.can_authenticate())

        #Validate
        valHdlr.Validator(linux_client=linux_client,
                          #flavorRef=NovaBootTestSuite.aSmallFlavor.id,
                          flavorRef=NovaBootTestSuite.flavor_ref,
                          opsDbProperty='vm-ops.US',
                          novaBootBO=novaBootBO,
                          createYroot=False).validate()

        #NOVA DELETE
        resp = novaCommands.NovaDelete(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            ids=[novaBootBO.id],
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0)

        #Validate
        valHdlr.Validator(novaBootBO=novaBootBO).validateAfterDelete()

    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT')
    @unittest.skip("Skipping the test as this is covered in boot with all images and flavor testcases")
    def test_nova_boot_all_images(self):
        """[Test] test_nova_boot_all_images """
        logger.info("[Test]test_nova_boot_all_images ")

        logger.info("test_nova_boot_all_images: nova image-list ")
        resp = novaCommands.NovaImageList(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url
        ).execute()
        novaImageListBO = opParser.NovaImageList(data=resp['stdOut']).get()

        responseList = []

        with self.multiple_assertions():
            for imageItem in novaImageListBO:
                # filter out *-initrd and *-vmlinuz images (may change in the future)
                if ((imageItem.name.find("-initrd") >= 0) or (imageItem.name.find("-vmlinuz") >= 0) or (
                            imageItem.name.find("ylinux") < 0) ):
                    logger.debug(
                        "Skipping the image %s because it has image name *-initrd or *-vmlinuz or not a ylinux image" % imageItem.name)
                    continue

                if (imageItem.status.find("ACTIVE") < 0):
                    logger.debug("Skipping the image as state is not ACTIVE instead " + str(imageItem.status))
                    continue;

                logger.info("test_nova_boot_all_images: " + imageItem.name + " ...")
                #NOVA BOOT
                resp = novaCommands.NovaBoot(
                    username=NovaBootTestSuite.username,
                    password=NovaBootTestSuite.password,
                    tenant_name=NovaBootTestSuite.tenant_name,
                    os_auth_url=NovaBootTestSuite.auth_url,
                    flavor=NovaBootTestSuite.flavor_ref,
                    image=imageItem.name,
                    user_data=NovaBootTestSuite.user_data,
                    name=rand_name("auto") + "-" + imageItem.name,
                    cwd=None,
                    env=NovaBootTestSuite.env
                ).execute()
                self.assertEqual(resp['retCode'], 0, "Nova boot failed having " + imageItem.name +
                                                     " with non-zero return code" + str(resp['stdErr']) + '\n' + str(
                    resp['stdOut']))
                responseList.append(resp['stdOut'])

            time.sleep(30)
            for response in responseList:
                novaBootBO = opParser.NovaBoot(response).get()

                servClient = servers_client.ServersClientJSON(config.CliConfig(),
                                                              NovaBootTestSuite.username,
                                                              NovaBootTestSuite.password,
                                                              NovaBootTestSuite.identity_auth_url,
                                                              NovaBootTestSuite.tenant_name)
                resp, server = servClient.get_server(novaBootBO.id)

                try:
                    #Get a linux client, to remote SSH into the VM
                    linux_client = RemoteClient(server,
                                                NovaBootTestSuite.yahoo_ssh_user,
                                                look_for_keys=True,
                                                key_filename=NovaBootTestSuite.key_filename)
                    #Validate
                    validations = valHdlr.Validator(linux_client=linux_client,
                                                    flavorRef=novaBootBO.flavor,
                                                    novaBootBO=novaBootBO,
                                                    createYroot=False)
                    validations.validate()
                except:
                    self.assertEqual(1, 0, "Exception happen during ssh / validation phase ")

                logger.info("Validation Ends ....")
                #NOVA DELETE
                resp = novaCommands.NovaDelete(
                    username=NovaBootTestSuite.username,
                    password=NovaBootTestSuite.password,
                    tenant_name=NovaBootTestSuite.tenant_name,
                    os_auth_url=NovaBootTestSuite.auth_url,
                    ids=[novaBootBO.id],
                    cwd=None,
                    env=NovaBootTestSuite.env
                ).execute()
                self.assertEqual(resp['retCode'], 0, "Nova delete failed with non-zero return code")

                #Validate
                valHdlr.Validator(novaBootBO=novaBootBO).validateAfterDelete()

                logger.info("test_nova_boot_all_images: " + imageItem.name + " done")

    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT')
    #@unittest.skip("Temporary")
    def test_nova_boot_multiple_yrole(self):
        """[Test] test_nova_boot_multiple_yrole """
        logger.info("[Test]test_nova_boot_multiple_yrole ")
        yroleArgs = ""
        for index in range(1, 3):
            yroleArgs = yroleArgs + " --yrole" + " " + NovaBootTestSuite.yrole + str(index)

        #NOVA BOOT
        resp = novaCommands.NovaBoot(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            flavor=NovaBootTestSuite.flavor_ref,
            image=NovaBootTestSuite.image_ref,
            user_data=NovaBootTestSuite.user_data,
            poll=True,
            name=rand_name("auto"),
            yroleArgs=yroleArgs,
            cwd=None,
            env=NovaBootTestSuite.env).execute()
        self.assertEqual(resp['retCode'], 0, "Nova boot exited with a non-zero return value \n"
                                             + str(resp['stdErr']) + '\n' + str(resp['stdOut']))

        novaBootBO = opParser.NovaBoot(resp['stdOut']).get()

        servClient = servers_client.ServersClientJSON(config.CliConfig(),
                                                      NovaBootTestSuite.username,
                                                      NovaBootTestSuite.password,
                                                      NovaBootTestSuite.identity_auth_url,
                                                      NovaBootTestSuite.tenant_name)
        resp, server = servClient.get_server(novaBootBO.id)
        logger.info(server)

        #Read the VM hostname from 'nova show'
        resp = novaCommands.NovaShow(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            name=novaBootBO.name,
        ).execute()
        novaShowBO = opParser.NovaShow(resp['stdOut']).get()

        #Get a linux client, to remote SSH into the VM
        linux_client = RemoteClient(server,
                                    NovaBootTestSuite.yahoo_ssh_user,
                                    look_for_keys=True,
                                    key_filename=NovaBootTestSuite.key_filename)

        #Make sure that the linux client can authenticate
        self.assertTrue(linux_client.can_authenticate())

        #Validate
        validations = valHdlr.Validator(linux_client=linux_client,
                                        customHostName=None,
                                        flavorRef=NovaBootTestSuite.flavor_ref,
                                        opsDbProperty=None,
                                        novaBootBO=novaBootBO,
                                        roles_to_validate=yroleArgs
        )
        validations.validate()

        #NOVA DELETE
        resp = novaCommands.NovaDelete(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            ids=[novaBootBO.id],
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0)

        #Validate
        #valHdlr.Validator(novaBootBO=novaBootBO).validateAfterDelete()
        #Give it some time before checking for deletion from opsdb and rolesdb
        time.sleep(15)
        validations.validateAfterDelete(checkRolesDeletion=True)

    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT')
    def test_nova_boot_single_yrole(self):
        """[Test] test_nova_boot_single_yrole """
        logger.info("[Test]test_nova_boot_single_yrole ")
        yroleArgs = ""
        for index in range(1, 3):
            yroleArgs = yroleArgs + " --yrole" + " " + NovaBootTestSuite.yrole + str(index)

        #NOVA BOOT
        resp = novaCommands.NovaBoot(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            flavor=NovaBootTestSuite.flavor_ref,
            image=NovaBootTestSuite.image_ref,
            user_data=NovaBootTestSuite.user_data,
            poll=True,
            name=rand_name("auto"),
            yroleArgs=yroleArgs,
            cwd=None,
            env=NovaBootTestSuite.env).execute()
        self.assertEqual(resp['retCode'], 0, "Nova boot exited with a non-zero return value \n"
                                             + str(resp['stdErr']) + '\n' + str(resp['stdOut']))

        novaBootBO = opParser.NovaBoot(resp['stdOut']).get()

        servClient = servers_client.ServersClientJSON(config.CliConfig(),
                                                      NovaBootTestSuite.username,
                                                      NovaBootTestSuite.password,
                                                      NovaBootTestSuite.identity_auth_url,
                                                      NovaBootTestSuite.tenant_name)
        resp, server = servClient.get_server(novaBootBO.id)
        logger.info(server)

        #Read the VM hostname from 'nova show'
        resp = novaCommands.NovaShow(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            name=novaBootBO.name,
        ).execute()
        novaShowBO = opParser.NovaShow(resp['stdOut']).get()

        #Get a linux client, to remote SSH into the VM
        linux_client = RemoteClient(server,
                                    NovaBootTestSuite.yahoo_ssh_user,
                                    look_for_keys=True,
                                    key_filename=NovaBootTestSuite.key_filename)

        #Make sure that the linux client can authenticate
        self.assertTrue(linux_client.can_authenticate())

        #Validate
        validations = valHdlr.Validator(linux_client=linux_client,
                                        customHostName=None,
                                        flavorRef=NovaBootTestSuite.flavor_ref,
                                        opsDbProperty=None,
                                        novaBootBO=novaBootBO,
                                        roles_to_validate=yroleArgs
        )
        validations.validate()

        #NOVA DELETE
        resp = novaCommands.NovaDelete(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            ids=[novaBootBO.id],
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0)

        #Validate
        #Give it some time before checking for deletion from ROLESDB
        time.sleep(15)
        validations.validateAfterDelete(checkRolesDeletion=True)

    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT')
    #@unittest.skip("Temporary")
    def test_nova_boot_nonexistent_yrole(self):
        """[Test] test_nova_boot_nonexistent_yrole """
        logger.info("[Test]test_nova_boot_nonexistent_yrole ")
        yroleArgs = "nonexistent.role"

        #NOVA BOOT
        resp = novaCommands.NovaBoot(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            flavor=NovaBootTestSuite.flavor_ref,
            image=NovaBootTestSuite.image_ref,
            user_data=NovaBootTestSuite.user_data,
            poll=True,
            name=rand_name("auto"),
            yroleArgs=yroleArgs,
            cwd=None,
            env=NovaBootTestSuite.env).execute()
        self.assertEqual(resp['retCode'], 0, "Nova boot exited with a non-zero return value \n"
                                             + str(resp['stdErr']) + '\n' + str(resp['stdOut']))
        novaBootBO = opParser.NovaBoot(resp['stdOut']).get()

        #Read the failure details from 'nova show'
        resp = novaCommands.NovaShow(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            name=novaBootBO.name,
        ).execute()
        novaShowBO = opParser.NovaShow(resp['stdOut']).get()

        m = None
        m = re.findall(r"ROLESDB add host:" \
                       + ".* to role: " + yroleArgs + " failed with code: 400 msg" \
                       , novaShowBO.fault, re.MULTILINE)
        self.assertTrue(m is not None, "RegEx did not match expected ROLESDB error")
        #NOVA DELETE
        resp = novaCommands.NovaDelete(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            ids=[novaBootBO.id],
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0)
        #Validate
        valHdlr.Validator(novaBootBO=novaBootBO).validateAfterDelete()

    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT')
    @unittest.skip(
        "As the permissions on sandbox have been relaxed, to allow booting into (previously inaccessible) roles")
    def test_nova_boot_no_permission_yrole(self):
        """[Test] test_nova_boot_no_permission_yrole """
        logger.info("[Test]test_nova_boot_no_permission_yrole ")
        yroleArgs = "media.bf6"

        #NOVA BOOT
        resp = novaCommands.NovaBoot(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            flavor=NovaBootTestSuite.flavor_ref,
            image=NovaBootTestSuite.image_ref,
            user_data=NovaBootTestSuite.user_data,
            poll=True,
            name=rand_name("auto"),
            yroleArgs=yroleArgs,
            cwd=None,
            env=NovaBootTestSuite.env).execute()
        self.assertEqual(resp['retCode'], 0, "Nova boot exited with a non-zero return value \n"
                                             + str(resp['stdErr']) + '\n' + str(resp['stdOut']))
        novaBootBO = opParser.NovaBoot(resp['stdOut']).get()

        #Read the failure details from 'nova show'
        resp = novaCommands.NovaShow(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            name=novaBootBO.name,
        ).execute()
        novaShowBO = opParser.NovaShow(resp['stdOut']).get()

        m = None
        m = re.findall(r"ROLESDB add host:" \
                       + ".* to role: " + yroleArgs + " failed with code: 400 msg" \
                       , novaShowBO.fault, re.MULTILINE)
        self.assertTrue(m is not None, "RegEx did not match expected ROLESDB error")
        #NOVA DELETE
        resp = novaCommands.NovaDelete(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            ids=[novaBootBO.id],
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0)
        #Validate
        valHdlr.Validator(novaBootBO=novaBootBO).validateAfterDelete()

    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT')
    #@unittest.skip("Temporary")
    def test_nova_boot_invalid_format_yrole(self):
        """[Test] test_nova_boot_invalid_format_yrole """
        logger.info("[Test]test_nova_boot_invalid_format_yrole ")
        yroleArgs = "example"

        #NOVA BOOT
        resp = novaCommands.NovaBoot(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            flavor=NovaBootTestSuite.flavor_ref,
            image=NovaBootTestSuite.image_ref,
            user_data=NovaBootTestSuite.user_data,
            poll=True,
            name=rand_name("auto"),
            yroleArgs=yroleArgs,
            cwd=None,
            env=NovaBootTestSuite.env).execute()
        self.assertNotEqual(resp['retCode'], 0, "VM Booted, while it should" \
                                                + " have failed rolename regex " \
                                                + "^[A-Za-z0-9_-]+\.[A-Za-z0-9]([A-Za-z0-9]|[-'()+,.:=?;!*#@$_%])+")

    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT')
    #@unittest.skip("Temporary")
    def test_nova_boot_multi_vms_in_yrole(self):
        """[Test] test_nova_boot_multi_vms_in_yrole """
        logger.info("[Test]test_nova_boot_multi_vms_in_yrole ")
        yroleArgs = "example.boot_multi_vms_in_me"
        novaBootBoList = []
        validations = []
        for count in range(0, 2):
            #NOVA BOOT
            resp = novaCommands.NovaBoot(
                username=NovaBootTestSuite.username,
                password=NovaBootTestSuite.password,
                tenant_name=NovaBootTestSuite.tenant_name,
                os_auth_url=NovaBootTestSuite.auth_url,
                flavor=NovaBootTestSuite.flavor_ref,
                image=NovaBootTestSuite.image_ref,
                user_data=NovaBootTestSuite.user_data,
                poll=True,
                name=rand_name("auto"),
                yroleArgs=yroleArgs,
                cwd=None,
                env=NovaBootTestSuite.env).execute()
            self.assertEqual(resp['retCode'], 0, "Nova boot exited with a non-zero return value \n"
                                                 + str(resp['stdErr']) + '\n' + str(resp['stdOut']))

            novaBootBO = opParser.NovaBoot(resp['stdOut']).get()
            novaBootBoList.append(novaBootBO)

            servClient = servers_client.ServersClientJSON(config.CliConfig(),
                                                          NovaBootTestSuite.username,
                                                          NovaBootTestSuite.password,
                                                          NovaBootTestSuite.identity_auth_url,
                                                          NovaBootTestSuite.tenant_name)
            resp, server = servClient.get_server(novaBootBO.id)
            logger.info(server)

            #Read the VM hostname from 'nova show'
            resp = novaCommands.NovaShow(
                username=NovaBootTestSuite.username,
                password=NovaBootTestSuite.password,
                tenant_name=NovaBootTestSuite.tenant_name,
                os_auth_url=NovaBootTestSuite.auth_url,
                name=novaBootBO.name,
            ).execute()
            novaShowBO = opParser.NovaShow(resp['stdOut']).get()

            #Get a linux client, to remote SSH into the VM
            linux_client = RemoteClient(server,
                                        NovaBootTestSuite.yahoo_ssh_user,
                                        look_for_keys=True,
                                        key_filename=NovaBootTestSuite.key_filename)

            #Make sure that the linux client can authenticate
            self.assertTrue(linux_client.can_authenticate())

            #Validate
            validations.append(valHdlr.Validator(linux_client=linux_client,
                                                 customHostName=None,
                                                 flavorRef=NovaBootTestSuite.flavor_ref,
                                                 opsDbProperty=None,
                                                 novaBootBO=novaBootBO,
                                                 roles_to_validate=yroleArgs
            ))
            validations[count].validate()

        for count in range(0, 2):
            #NOVA DELETE
            resp = novaCommands.NovaDelete(
                username=NovaBootTestSuite.username,
                password=NovaBootTestSuite.password,
                tenant_name=NovaBootTestSuite.tenant_name,
                os_auth_url=NovaBootTestSuite.auth_url,
                ids=[novaBootBoList[count].id],
                cwd=None,
                env=NovaBootTestSuite.env
            ).execute()
            self.assertEqual(resp['retCode'], 0)

            #Validate
            #Give it a few seconds before checking deletion from ROLESDB
            time.sleep(15)
            validations[count].validateAfterDelete(checkRolesDeletion=True)

    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT', problem='TRUE')
    #@unittest.skip("Temporary")
    def test_nova_boot_multi_vms_in_single_yrole(self):
        """[Test] test_nova_boot_multi_vms_in_single_yrole """
        logger.info("[Test]test_nova_boot_multi_vms_in_single_yrole ")
        yroleArgs = "example.boot_multi_vms_in_me"
        novaBootBoList = []
        validations = []
        for count in range(0, 2):
            #NOVA BOOT
            resp = novaCommands.NovaBoot(
                username=NovaBootTestSuite.username,
                password=NovaBootTestSuite.password,
                tenant_name=NovaBootTestSuite.tenant_name,
                os_auth_url=NovaBootTestSuite.auth_url,
                flavor=NovaBootTestSuite.flavor_ref,
                image=NovaBootTestSuite.image_ref,
                user_data=NovaBootTestSuite.user_data,
                poll=True,
                name=rand_name("auto"),
                yroleArgs=yroleArgs,
                cwd=None,
                env=NovaBootTestSuite.env).execute()
            self.assertEqual(resp['retCode'], 0, "Nova boot exited with a non-zero return value \n"
                                                 + str(resp['stdErr']) + '\n' + str(resp['stdOut']))

            novaBootBO = opParser.NovaBoot(resp['stdOut']).get()
            novaBootBoList.append(novaBootBO)

            servClient = servers_client.ServersClientJSON(config.CliConfig(),
                                                          NovaBootTestSuite.username,
                                                          NovaBootTestSuite.password,
                                                          NovaBootTestSuite.identity_auth_url,
                                                          NovaBootTestSuite.tenant_name)
            resp, server = servClient.get_server(novaBootBO.id)
            logger.info(server)

            #Read the VM hostname from 'nova show'
            resp = novaCommands.NovaShow(
                username=NovaBootTestSuite.username,
                password=NovaBootTestSuite.password,
                tenant_name=NovaBootTestSuite.tenant_name,
                os_auth_url=NovaBootTestSuite.auth_url,
                name=novaBootBO.name,
            ).execute()
            novaShowBO = opParser.NovaShow(resp['stdOut']).get()

            #Get a linux client, to remote SSH into the VM
            linux_client = RemoteClient(server,
                                        NovaBootTestSuite.yahoo_ssh_user,
                                        look_for_keys=True,
                                        key_filename=NovaBootTestSuite.key_filename)

            #Make sure that the linux client can authenticate
            self.assertTrue(linux_client.can_authenticate())

            #Validate
            validations.append(valHdlr.Validator(linux_client=linux_client,
                                                 customHostName=None,
                                                 flavorRef=NovaBootTestSuite.flavor_ref,
                                                 opsDbProperty=None,
                                                 novaBootBO=novaBootBO,
                                                 roles_to_validate=yroleArgs
            ))
            validations[count].validate()

        for count in range(0, 2):
            #NOVA DELETE
            resp = novaCommands.NovaDelete(
                username=NovaBootTestSuite.username,
                password=NovaBootTestSuite.password,
                tenant_name=NovaBootTestSuite.tenant_name,
                os_auth_url=NovaBootTestSuite.auth_url,
                ids=[novaBootBoList[count].id],
                cwd=None,
                env=NovaBootTestSuite.env
            ).execute()
            self.assertEqual(resp['retCode'], 0)

            #Validate
            #Give it a few seconds before checking deletion from ROLESDB
            time.sleep(15)
            validations[count].validateAfterDelete(checkRolesDeletion=True)

    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT')
    #@unittest.skip("Skip until Defect: 6140109 is fixed")
    def test_nova_boot_multi_vms_in_multiple_yrole(self):
        """[Test] test_nova_boot_multi_vms_in_multiple_yrole """
        logger.info("[Test]test_nova_boot_multi_vms_in_multiple_yrole ")
        #Boot 2 VMs under example.A and one under example.B
        yroleArgsList = ["example.aa", "example.aa", "example.bb"]
        novaBootBoList = []
        validations = []
        for count in range(0, 3):
            #NOVA BOOT
            resp = novaCommands.NovaBoot(
                username=NovaBootTestSuite.username,
                password=NovaBootTestSuite.password,
                tenant_name=NovaBootTestSuite.tenant_name,
                os_auth_url=NovaBootTestSuite.auth_url,
                flavor=NovaBootTestSuite.flavor_ref,
                image=NovaBootTestSuite.image_ref,
                user_data=NovaBootTestSuite.user_data,
                poll=True,
                name=rand_name("auto"),
                yroleArgs=yroleArgsList[count],
                cwd=None,
                env=NovaBootTestSuite.env).execute()
            self.assertEqual(resp['retCode'], 0, "Nova boot exited with a non-zero return value \n"
                                                 + str(resp['stdErr']) + '\n' + str(resp['stdOut']))

            novaBootBO = opParser.NovaBoot(resp['stdOut']).get()
            novaBootBoList.append(novaBootBO)

            servClient = servers_client.ServersClientJSON(config.CliConfig(),
                                                          NovaBootTestSuite.username,
                                                          NovaBootTestSuite.password,
                                                          NovaBootTestSuite.identity_auth_url,
                                                          NovaBootTestSuite.tenant_name)
            resp, server = servClient.get_server(novaBootBO.id)
            logger.info(server)

            #Read the VM hostname from 'nova show'
            resp = novaCommands.NovaShow(
                username=NovaBootTestSuite.username,
                password=NovaBootTestSuite.password,
                tenant_name=NovaBootTestSuite.tenant_name,
                os_auth_url=NovaBootTestSuite.auth_url,
                name=novaBootBO.name,
            ).execute()
            novaShowBO = opParser.NovaShow(resp['stdOut']).get()

            #Get a linux client, to remote SSH into the VM
            linux_client = RemoteClient(server,
                                        NovaBootTestSuite.yahoo_ssh_user,
                                        look_for_keys=True,
                                        key_filename=NovaBootTestSuite.key_filename)

            #Make sure that the linux client can authenticate
            self.assertTrue(linux_client.can_authenticate())

            #Validate
            validations.append(valHdlr.Validator(linux_client=linux_client,
                                                 customHostName=None,
                                                 flavorRef=NovaBootTestSuite.flavor_ref,
                                                 opsDbProperty=None,
                                                 novaBootBO=novaBootBO,
                                                 roles_to_validate=yroleArgsList[count]
            ))
            validations[count].validate()

        #NOVA DELETE 'em, one shot
        resp = novaCommands.NovaDelete(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            ids=[novaBootBO.id for novaBootBO in novaBootBoList],
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0)

        #Give it a few seconds before checking deletion from ROLESDB
        time.sleep(15)
        for count in range(0, 3):
            #Validate
            validations[count].validateAfterDelete(checkRolesDeletion=True)

    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT')
    def test_nova_boot_custom_hostname_with_yrole(self):
        """[Test] test_nova_boot_custom_hostname_with_yrole """
        logger.info("[Test]test_nova_boot_custom_hostname_with_yrole ")
        yroleArgs = "example.custom_host_with_yrole"
        custom_hostname = "%s.%s" % (rand_name("yrole"), NovaBootTestSuite.custom_hostname)
        #NOVA BOOT
        resp = novaCommands.NovaBoot(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            flavor=NovaBootTestSuite.flavor_ref,
            image=NovaBootTestSuite.image_ref,
            user_data=NovaBootTestSuite.user_data,
            poll=True,
            hostname=custom_hostname,
            name=rand_name("auto"),
            yroleArgs=yroleArgs,
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0, "Nova boot exited with a non-zero return value \n"
                                             + str(resp['stdErr']) + '\n' + str(resp['stdOut']))

        novaBootBO = opParser.NovaBoot(resp['stdOut']).get()

        servClient = servers_client.ServersClientJSON(config.CliConfig(),
                                                      NovaBootTestSuite.username,
                                                      NovaBootTestSuite.password,
                                                      NovaBootTestSuite.identity_auth_url,
                                                      NovaBootTestSuite.tenant_name)
        logger.info(novaBootBO.id)
        resp, server = servClient.get_server(novaBootBO.id)
        logger.info(server)

        #Get a linux client, to remote SSH into the VM
        linux_client = RemoteClient(server,
                                    self.config.compute.yahoo_ssh_user,
                                    look_for_keys=True,
                                    key_filename=self.config.compute.key_filename)

        #Make sure that the linux client can authenticate
        self.assertTrue(linux_client.can_authenticate())

        #Validate
        validations = valHdlr.Validator(linux_client=linux_client,
                                        customHostName=custom_hostname,
                                        flavorRef=NovaBootTestSuite.flavor_ref,
                                        opsDbProperty=None,
                                        novaBootBO=novaBootBO,
                                        roles_to_validate=yroleArgs,
                                        createYroot=False)

        validations.validate()

        #NOVA DELETE
        resp = novaCommands.NovaDelete(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            ids=[novaBootBO.id],
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0)

        time.sleep(15)
        #Validate
        #Note: we are not checking for cleanups from rolesdb, because of BZ 6066333
        #http://bug.corp.yahoo.com/show_bug.cgi?id=6066333&mark=1#c1
        validations.validateAfterDelete(checkRolesDeletion=False)

    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-DELETE')
    def test_delete_non_existent_vm(self):
        """[Test] test_delete_non_existent_vm """
        logger.info("[Test]test_delete_non_existent_vm ")

        #NOVA DELETE A NON-EXISTING VM
        resp = novaCommands.NovaDelete(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            ids=['cab1111f-11dd-1f1f-1d10-bc1e1d11cf11'],
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 1,
                         "Nova single Delete didn't existed with 0 return code instead " +
                         str(resp['retCode']) + " with response stdErr" + str(
                             resp['stdErr']) + " & StdOut " +
                         str(resp['stdOut']))
        self.assertTrue("No server with a name or ID of" in resp['stdErr'])

    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT')
    def test_nova_boot_against_non_existent_flavor(self):
        """[Test] test_nova_boot_against_non_existent_flavor """
        logger.info("[Test]test_nova_boot_against_non_existent_flavor ")
        #NOVA BOOT (NON-EXISTENT FLAVOR)
        resp = novaCommands.NovaBoot(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            flavor="NON-EXISTENT-FLAVOR",
            image=NovaBootTestSuite.image_ref,
            user_data=NovaBootTestSuite.user_data,
            poll=True,
            name=rand_name("auto"),
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertNotEqual(resp['retCode'], 0)
        self.assertTrue("ERROR: No flavor with a name or ID of" in resp['stdErr'])

    @unittest.skip("Skipping due to new data-driven approach applied to this test")
    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT', allImage='TRUE')
    def test_nova_boot_all_flavor_and_images(self):
        """[Test] test_nova_boot_all_images_with_all_flavors  \n .. \n"""

        # Get all the images from the nova
        resp = novaCommands.NovaImageList().execute()
        novaImageListBO = opParser.NovaImageList(data=resp['stdOut']).get()
        # Get all the flavor
        resp = novaCommands.NovaFlavorList().execute()
        flavListBO = opParser.NovaFlavorList(data=resp['stdOut']).get()
        responseList = []
        print "\n"  # Empty print to add new line on console for pretty printing
        with self.multiple_assertions():
            for imageItem in novaImageListBO:
                # filter out *-initrd and *-vmlinuz images (may change in the future)
                if ((imageItem.name.find("-initrd") >= 0) or (imageItem.name.find("-vmlinuz") >= 0) or (
                            imageItem.name.find("ylinux") < 0) ):
                    logger.debug(
                        "Skipping the image %s because it has image name *-initrd or *-vmlinuz or not a ylinux image" % imageItem.name)
                    continue

                if (imageItem.status.find("ACTIVE") < 0):
                    logger.debug("Skipping the image as state is not ACTIVE instead " + str(imageItem.status))
                    continue;

                logger.debug("test_nova_boot_all_images: " + imageItem.name + " ...")
                VMsToDelete = []
                for aFlav in flavListBO:
                    #NOVA BOOT
                    resp = novaCommands.NovaBoot(flavor=aFlav.id,
                                                 image=imageItem.name,
                                                 name=rand_name("auto") + "-" + imageItem.name + "-" + aFlav.name,
                                                 #poll=True,
                    ).execute()

                    if resp['retCode'] != 0 or resp['stdOut'] is None:
                        self.assertEqual(resp['retCode'], 0, "Nova boot failed having " + imageItem.name
                                        + " with non-zero return code \n" + str(resp['stdErr']) + '\n' + str(resp['stdOut']))
                        print "[FAIL] Booting VM with Image = " + imageItem.name + " with Flavor = " + aFlav.name + str(
                            resp['stdErr']) + "  ...."
                        continue

                    responseList.append(resp['stdOut'])

            for response in responseList:
                novaBootBO = opParser.NovaBoot(response).get()

                VMsToDelete.append(novaBootBO.id)
                logger.debug("VM ID = " + novaBootBO.id)
                logger.debug("VM Ip address = " + str(novaBootBO.default_network))

                servClient = servers_client.ServersClientJSON(config.CliConfig(),
                                                              NovaBootTestSuite.username,
                                                              NovaBootTestSuite.password,
                                                              NovaBootTestSuite.identity_auth_url,
                                                              NovaBootTestSuite.tenant_name)
                resp, server = servClient.get_server(novaBootBO.id)
                logger.info(server)

                try:
                    #Get a linux client, to remote SSH into the VM
                    linux_client = RemoteClient(server,
                                                NovaBootTestSuite.yahoo_ssh_user,
                                                look_for_keys=True,
                                                key_filename=NovaBootTestSuite.key_filename)
                    #Validate
                    validations = valHdlr.Validator(linux_client=linux_client,
                                                    flavorRef=(novaBootBO.flavor.split(" "))[0],
                                                    novaBootBO=novaBootBO,
                                                    createYroot=False)
                    validations.validate()
                    print "[PASS] Image = " + novaBootBO.image + " with Flavor = " + novaBootBO.flavor + " ...."
                except:
                    type, value, tb = sys.exc_info()
                    print "[FAIL] Validation on Image = ", novaBootBO.image, " with Flavor = ", novaBootBO.flavor, " ....",  \
                                    ''. join( traceback.format_exception(type, value, tb)).strip("\n")
                    self.assertEqual(1, 0,
                                     "Exception happen during ssh / validation phase on Image = " + novaBootBO.image + \
                                     " with Flavor = " + novaBootBO.flavor + ''.join(
                                         traceback.format_exception(type, value, tb)).strip("\n"))


            #NOVA DELETE
            resp = novaCommands.NovaDelete(ids=VMsToDelete).execute()
            self.assertEqual(resp['retCode'], 0,
                             "Nova delete failed with non-zero return code having image name %s" % imageItem.name)
            
    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT')
    def test_nova_boot_incorrect_user_password(self):
        vm_name = rand_name('auto_boot')
        ERROR_MESSAGE = 'ERROR: Invalid bouncer credentials.'

        #This is a workaround for a defect. As a result of previous tests
        #user's token is saved in keyring file and this token is used
        #regardless of any given password to nova command.
        CommandLineToolsUtils().cmd('rm -rf %s/.local/share/python_keyring' %
                                    expanduser("~"), '')

        test_vm = VirtualMachine(password="incorrect", fail_ok=True)
        result = test_vm.boot(vm_name)
        self.assertIn(ERROR_MESSAGE, result,
                         'Incorrect error message during the VM creation')

    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT')
    def test_nova_boot_incorrect_user_name(self):
        vm_name = rand_name('auto_boot')
        ERROR_MESSAGE = 'ERROR: Invalid bouncer credentials.'

        test_vm = VirtualMachine(username="qwerty", fail_ok=True)
        result = test_vm.boot(vm_name)
        self.assertIn(ERROR_MESSAGE, result,
                      'Incorrect error message during the VM creation')

@classmethod
def tearDownClass(cls):
    logger.info("Finished executing NovaBootTestSuite")
    pass
    @attr(interface='OS-NATIVE', group='POST-INSTALL', genre='NOVA-BOOT', allImage='TRUE')
    @data(generate_list_of_images_and_flavors_new())
    @ddt_list
    def test_nova_boot_all_flavor_and_images_ddt(self, *args, **kwargs):

        imageItem = kwargs.values()[0][0]
        aFlav = kwargs.values()[0][1]

        logger.debug("test_nova_boot_all_images: " + imageItem.name + " ...")
        VMsToDelete = []

        #NOVA BOOT
        resp = novaCommands.NovaBoot(flavor=aFlav.id,
                                     image=imageItem.name,
                                     user_data=NovaBootTestSuite.user_data,
                                     name=rand_name("auto") + "-" + imageItem.name + "-" + aFlav.name,
                                     poll=True,
                                     cwd=None,
                                     env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0, "Nova boot failed having " + imageItem.name
                       + " with non-zero return code \n" + str(resp['stdErr']) + '\n' + str(resp['stdOut']))

        novaBootBO = opParser.NovaBoot(resp['stdOut']).get()
        VMsToDelete.append(novaBootBO.id)
        logger.debug("VM ID = " + novaBootBO.id)
        logger.debug("VM Ip address = " + str(novaBootBO.default_network))

        servClient = servers_client.ServersClientJSON(config.CliConfig(),
                                                      NovaBootTestSuite.username,
                                                      NovaBootTestSuite.password,
                                                      NovaBootTestSuite.identity_auth_url,
                                                      NovaBootTestSuite.tenant_name)
        resp, server = servClient.get_server(novaBootBO.id)
        logger.info(server)

        #Get a linux client, to remote SSH into the VM
        linux_client = RemoteClient(server,
                                    NovaBootTestSuite.yahoo_ssh_user,
                                    look_for_keys=True,
                                    key_filename=NovaBootTestSuite.key_filename)

        #Validate
        validations = valHdlr.Validator(linux_client=linux_client,
                                        flavorRef=aFlav.id,
                                        novaBootBO=novaBootBO,
                                        createYroot=False)
        validations.validate()

        #NOVA DELETE
        resp = novaCommands.NovaDelete(
            username=NovaBootTestSuite.username,
            password=NovaBootTestSuite.password,
            tenant_name=NovaBootTestSuite.tenant_name,
            os_auth_url=NovaBootTestSuite.auth_url,
            ids=VMsToDelete,
            cwd=None,
            env=NovaBootTestSuite.env
        ).execute()
        self.assertEqual(resp['retCode'], 0, "Nova delete failed with non-zero return code")

    @classmethod
    def tearDownClass(cls):
        logger.info("Finished executing NovaBootTestSuite")
        pass
