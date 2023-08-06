import os
import unittest
from click.testing import CliRunner
import json
from dnastack import __main__ as dnastack_cli

from .utils import clear_config
from .. import *


class TestCliConfigCommand(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.data_connect_url = TEST_DATA_CONNECT_URI
        self.wes_url = TEST_WES_URI
        self.refresh_token = TEST_WALLET_REFRESH_TOKEN["publisher"]
        clear_config()

    def test_cli_config_set_get(self):
        result = self.runner.invoke(
            dnastack_cli.dnastack,
            ["config", "set", "data-connect-url", self.data_connect_url],
        )

        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(
            dnastack_cli.dnastack, ["config", "get", "data-connect-url"]
        )

        self.assertEqual(result.exit_code, 0)

        self.assertEqual(result.output.strip(), self.data_connect_url)

    def test_cli_config_set_get_nested(self):
        result = self.runner.invoke(
            dnastack_cli.dnastack,
            ["config", "set", "oauth_token.refresh_token", self.refresh_token],
        )

        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(
            dnastack_cli.dnastack, ["config", "get", "oauth_token.refresh_token"]
        )

        self.assertEqual(result.exit_code, 0)

        self.assertEqual(result.output.strip(), self.refresh_token)

    def test_cli_config_get_bad_key(self):
        result = self.runner.invoke(dnastack_cli.dnastack, ["config", "get", "testKey"])

        self.assertEqual(result.exit_code, 1)
        self.assertIn("not an accepted configuration key", result.output)
        self.assertIn("accepted configuration keys", result.output.lower())

    def test_cli_config_set_bad_key(self):
        result = self.runner.invoke(
            dnastack_cli.dnastack, ["config", "set", "testKey", "testValue"]
        )

        self.assertEqual(result.exit_code, 1)
        self.assertIn("not an accepted configuration key", result.output)
        self.assertIn("accepted configuration keys", result.output.lower())

    def test_cli_config_list(self):

        self.runner.invoke(
            dnastack_cli.dnastack,
            [
                "config",
                "set",
                "data-connect-url",
                self.data_connect_url,
            ],
        )

        self.runner.invoke(
            dnastack_cli.dnastack,
            [
                "config",
                "set",
                "wes-url",
                self.wes_url,
            ],
        )

        self.runner.invoke(
            dnastack_cli.dnastack,
            [
                "config",
                "set",
                "oauth_token.refresh_token",
                self.refresh_token,
            ],
        )

        # test config list
        result = self.runner.invoke(dnastack_cli.dnastack, ["config", "list"])

        result_object = json.loads(result.output)

        self.assertEqual(result_object["data-connect-url"], self.data_connect_url)
        self.assertEqual(result_object["wes-url"], self.wes_url)
        self.assertEqual(
            result_object["oauth_token"]["refresh_token"], self.refresh_token
        )
