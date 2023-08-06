import os
import unittest
import pathlib
from dnastack import PublisherClient
from .. import *
import json


class TestCliWesCommand(unittest.TestCase):
    def setUp(self):
        self.publisher_client = PublisherClient(
            wes_url=TEST_WES_URI, auth_params=TEST_AUTH_PARAMS["wes"]
        )
        self.wes_url = TEST_WES_URI
        self.publisher_client.auth.oauth_token["scope"] = TEST_AUTH_SCOPES["wes"]
        self.publisher_client.auth.set_refresh_token(TEST_WALLET_REFRESH_TOKEN["wes"])
        self.publisher_client.auth.refresh_token()

    def test_wes_info_with_auth(self):
        result = self.publisher_client.wes.info()

        self.assertIsNotNone(result)

        self.assertIn("workflow_type_versions", result.keys())
        self.assertIn("supported_wes_versions", result.keys())
        self.assertIn("supported_filesystem_protocols", result.keys())
        self.assertIn("workflow_engine_versions", result.keys())
        self.assertIn("system_state_counts", result.keys())
