# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 OpenStack, LLC
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import time
import socket
import warnings
import select

from yopenstackqe_tests import exceptions
from yopenstackqe_tests.common.utils import yLogger

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import paramiko

logger = yLogger.setup_custom_logger('SSH')

##########################################################################
#    Wrapper for Paramiko interface used to SSH into VMs/API-Nodes
##########################################################################
class Client(object):

    def __init__(self, host, username, password=None, timeout=3,
                 channel_timeout=600, look_for_keys=False, key_filename=None):
        logger.debug("Getting a client to host=" + str(host));
        self.host = host
        self.username = username
        self.password = password
        self.look_for_keys = look_for_keys
        self.key_filename = key_filename
        self.timeout = int(timeout)
        self.channel_timeout = float(channel_timeout)
        self.buf_size = 1024

    def _get_ssh_connection(self):
        """Returns an ssh connection to the specified host"""
        _timeout = True
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())
        _start_time = time.time()

        while not self._is_timed_out(self.timeout, _start_time):
            try:
                logger.debug("Trying to connect to the server as " + self.username + "@"  + self.host)
                time.sleep(2)
                ssh.connect(self.host, username=self.username,
                            password=self.password,
                            look_for_keys=self.look_for_keys,
                            key_filename=self.key_filename,
                            timeout=self.timeout)
                _timeout = False
                break
            except socket.error:
                continue
            except paramiko.AuthenticationException:
                time.sleep(5)
                continue
        if _timeout:
            logger.error("Timeout reached while trying to connect to server : " + self.host)
            raise exceptions.SSHTimeout(host=self.host,
                                        user=self.username,
                                        password=self.password)
        logger.debug("Connected to server ..." + self.host)            
        return ssh

    def _is_timed_out(self, timeout, start_time):
        return (time.time() - timeout) > start_time

    def connect_until_closed(self):
        """Connect to the server and wait until connection is lost"""
        try:
            ssh = self._get_ssh_connection()
            _transport = ssh.get_transport()
            _start_time = time.time()
            _timed_out = self._is_timed_out(self.timeout, _start_time)
            while _transport.is_active() and not _timed_out:
                time.sleep(5)
                _timed_out = self._is_timed_out(self.timeout, _start_time)
            ssh.close()
        except (EOFError, paramiko.AuthenticationException, socket.error):
            return

    def exec_command(self, cmd):
        """
        Execute the specified command on the server.

        Note that this method is reading whole command outputs to memory, thus
        shouldn't be used for large outputs.

        :returns: data read from standard output of the command.
        :raises: SSHExecCommandFailed if command returns nonzero
                 status. The exception contains command status stderr content.
        """
        logger.info("Executing command[" + cmd + "] on host [" + self.host +"]")
        ssh = self._get_ssh_connection()
        transport = ssh.get_transport()
        channel = transport.open_session()
        channel.exec_command(cmd)
        channel.shutdown_write()
        out_data = []
        err_data = []

        select_params = [channel], [], [], self.channel_timeout
        while True:
            ready = select.select(*select_params)
            if not any(ready):
                raise exceptions.TimeoutException(
                        "Command: '{0}' executed on host '{1}'.".format(
                            cmd, self.host))
            if not ready[0]:        # If there is nothing to read.
                continue
            out_chunk = err_chunk = None
            if channel.recv_ready():
                out_chunk = channel.recv(self.buf_size)
                out_data += out_chunk,
            if channel.recv_stderr_ready():
                err_chunk = channel.recv_stderr(self.buf_size)
                err_data += err_chunk,
            if channel.closed and not err_chunk and not out_chunk:
                break
        exit_status = channel.recv_exit_status()
        if 0 != exit_status:
            raise exceptions.SSHExecCommandFailed(
                    command=cmd, exit_status=exit_status,
                    strerror=''.join(err_data))
        logger.debug("Command output : " + str(out_data))
        return ''.join(out_data)

    def exec_command_on_nova_server(self, cmd, expect_response=True):
        """
        Execute the specified command on the server.

        Note that this method is reading whole command outputs to memory, thus
        shouldn't be used for large outputs.

        :returns: data read from standard output of the command.
        :raises: SSHExecCommandFailed if command returns nonzero
                 status. The exception contains command status stderr content.
        """
        resp = ''
        if "sudo" in cmd:
            logger.info(cmd + " it starts with sudo")
            ssh = self._get_ssh_connection()
            channel=ssh.invoke_shell()
            channel.send(cmd)
            time.sleep(2)
            resp = channel.recv(9999)
            resp = resp.strip()
            logger.info("Resp:" + resp)
            if resp.endswith("Password:"):
                logger.info("Got a Password prompt")
                if channel.send_ready():
                    logger.info("Channel is send ready now")
                    bytes = channel.send(self.password + '\n')
                    logger.info("Sent password size:" + str(bytes))
                    time.sleep(1)
                    #bytes = channel.send(self.password + '\n')
                    bytes = channel.send('\n')
                    logger.info("Sent password size:" + str(bytes))
                    channel.shutdown_write()
                else:
                    logger.info("Channel is not send ready now")
                if 'mysql_master_switchover' in cmd:
                    time.sleep(15)
                if channel.recv_ready():
                    resp = channel.recv(9999)
                #channel.shutdown_read()
                logger.info("Resp down password route: " + resp)
            ssh.close()
            logger.info("After SSH close")
        else:
            ssh = self._get_ssh_connection()
            transport = ssh.get_transport()
            channel = transport.open_session()
            channel.exec_command(cmd)
            logger.info(cmd + " does not start with sudo")
            channel.shutdown_write()
            logger.info("After shutdown_write")
        out_data = []
        err_data = []

        select_params = [channel], [], [], self.channel_timeout
        #logger.info(select_params)
        if expect_response:
            while True:
                if channel.recv_ready():
                    logger.info("Channel is Recv ready")
                else:
                    logger.info("Channel is Not Recv ready")
                if channel.recv_stderr(100):
                    logger.info("Channel is Stderr ready")
                else:
                    logger.info("Channel is Not Stderr ready")
                ready = select.select(*select_params)
                #logger.info("Ready:")
                #logger.info(ready)
                if not any(ready):
                    raise exceptions.TimeoutException(
                            "Command: '{0}' executed on host '{1}'.".format(
                                cmd, self.host))
                if not ready[0]:        # If there is nothing to read.
                    continue
                out_chunk = err_chunk = None
                if channel.recv_ready():
                    out_chunk = channel.recv(self.buf_size)
                    out_data += out_chunk,
                if channel.recv_stderr_ready():
                    err_chunk = channel.recv_stderr(self.buf_size)
                    err_data += err_chunk,
                if channel.closed and not err_chunk and not out_chunk:
                    break
            exit_status = channel.recv_exit_status()
            if 0 != exit_status:
                raise exceptions.SSHExecCommandFailed(
                        command=cmd, exit_status=exit_status,
                        strerror=''.join(err_data))
            return ''.join(out_data)
        else:
            # Return whatever we got
            return resp

    def test_connection_auth(self):
        """ Returns true if ssh can connect to server"""
        try:
            connection = self._get_ssh_connection()
            connection.close()
        except paramiko.AuthenticationException:
            return False

        return True
