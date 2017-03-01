import subprocess
import unittest

import mock

from kayobe import utils


class TestCase(unittest.TestCase):

    @mock.patch.object(utils, "run_command")
    def test_yum_install(self, mock_run):
        utils.yum_install(["package1", "package2"])
        mock_run.assert_called_once_with(["sudo", "yum", "-y", "install",
                                          "package1", "package2"])

    @mock.patch.object(utils, "run_command")
    def test_yum_install_failure(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, "command")
        self.assertRaises(SystemExit,
                          utils.yum_install, ["package1", "package2"])

    @mock.patch.object(utils, "run_command")
    def test_galaxy_install(self, mock_run):
        utils.galaxy_install("/path/to/role/file", "/path/to/roles")
        mock_run.assert_called_once_with(["ansible-galaxy", "install",
                                          "--roles-path", "/path/to/roles",
                                          "--role-file", "/path/to/role/file"])

    @mock.patch.object(utils, "run_command")
    def test_galaxy_install_failure(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, "command")
        self.assertRaises(SystemExit,
                          utils.galaxy_install, "/path/to/role/file",
                          "/path/to/roles")

    @mock.patch.object(utils, "read_file")
    def test_read_yaml_file(self, mock_read):
        mock_read.return_value = """---
key1: value1
key2: value2
"""
        result = utils.read_yaml_file("/path/to/file")
        self.assertEqual(result, {"key1": "value1", "key2": "value2"})
        mock_read.assert_called_once_with("/path/to/file")

    @mock.patch.object(utils, "read_file")
    def test_read_yaml_file_open_failure(self, mock_read):
        mock_read.side_effect = IOError
        self.assertRaises(SystemExit, utils.read_yaml_file, "/path/to/file")

    @mock.patch.object(utils, "read_file")
    def test_read_yaml_file_not_yaml(self, mock_read):
        mock_read.return_value = "[1{!"
        self.assertRaises(SystemExit, utils.read_yaml_file, "/path/to/file")

    @mock.patch.object(subprocess, "check_call")
    def test_run_command(self, mock_call):
        utils.run_command(["command", "to", "run"])
        mock_call.assert_called_once_with(["command", "to", "run"])

    @mock.patch.object(subprocess, "check_call")
    def test_run_command_quiet(self, mock_call):
        utils.run_command(["command", "to", "run"], quiet=True)
        mock_call.assert_called_once_with(["command", "to", "run"],
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)

    @mock.patch.object(subprocess, "check_call")
    def test_run_command_failure(self, mock_call):
        mock_call.side_effect = subprocess.CalledProcessError(1, "command")
        self.assertRaises(subprocess.CalledProcessError, utils.run_command,
                          ["command", "to", "run"])
