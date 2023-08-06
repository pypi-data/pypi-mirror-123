import os
import unittest
from dnastack import PublisherClient
from .. import *


def assert_has_property(self, obj, attribute):
    self.assertTrue(
        attribute in obj,
        msg="obj lacking an attribute. obj: %s, intendedAttribute: %s"
        % (obj, attribute),
    )


class TestClientLibraryDataConnectTablesCommand(unittest.TestCase):
    def setUp(self):
        self.publisher_client = PublisherClient(dataconnect_url=TEST_DATA_CONNECT_URI)

    def test_tables_list(self):
        result = self.publisher_client.dataconnect.list_tables()

        self.assertIsNotNone(result)

        for item in result:
            assert_has_property(self, item, "name")
            assert_has_property(self, item, "data_model")
            assert_has_property(self, item["data_model"], "$ref")

    def test_tables_get_table(self):
        list_tables_result = self.publisher_client.dataconnect.list_tables()
        table_name = list_tables_result[len(list_tables_result) - 1]["name"]
        get_table_result = self.publisher_client.dataconnect.get_table(table_name)

        self.assertIsNotNone(get_table_result)

        assert_has_property(self, get_table_result, "name")
        assert_has_property(self, get_table_result, "description")
        assert_has_property(self, get_table_result, "data_model")
        assert_has_property(self, get_table_result["data_model"], "$id")
        assert_has_property(self, get_table_result["data_model"], "$schema")
        assert_has_property(self, get_table_result["data_model"], "description")

        for property in get_table_result["data_model"]["properties"]:
            assert_has_property(
                self, get_table_result["data_model"]["properties"][property], "format"
            )
            assert_has_property(
                self, get_table_result["data_model"]["properties"][property], "type"
            )
            assert_has_property(
                self,
                get_table_result["data_model"]["properties"][property],
                "$comment",
            )

    def test_tables_get_table_does_not_exist(self):
        with self.assertRaises(Exception) as cm:
            self.publisher_client.dataconnect.get_table("some table name")
