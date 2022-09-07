import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.aidm import TableDefinition, TableColumnDefinition, TableCellDataType
from py_client.aidm.aidm_table_cell_classes import TableTextCell
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestCreateTable(unittest.TestCase):
    class TestCreateTableTestSessionMock(SessionMockTestBase):
        def post(self, request: str, json: dict):
            self._last_request = request
            self._last_body = json

            return APISessionMock.create_response_mock("""{ "tableId": 11041 }""", 200)

    @mock.patch("requests.Session", side_effect=TestCreateTableTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=TestCreateTableTestSessionMock)
    def test_create_table_request(self, _):
        header_1 = TableTextCell("keyOfColumn1", "Caption of Column With String Header and String Data")
        definition_of_table_column_1 = TableColumnDefinition(header_1.column_key, header_1, TableCellDataType.string, TableCellDataType.string)

        header_2 = TableTextCell("keyOfColumn2", "Column With Integer Entries")
        definition_of_table_column_2 = TableColumnDefinition(header_2.column_key, header_2, TableCellDataType.string, TableCellDataType.integer)

        header_3 = TableTextCell("keyOfColumn3", "Column With DateTime Entries")
        definition_of_table_column_3 = TableColumnDefinition(header_3.column_key, header_3, TableCellDataType.string, TableCellDataType.local_date_time)

        header_4 = TableTextCell("keyOfColumn4", "Column With Duration Entries")
        definition_of_table_column_4 = TableColumnDefinition(header_4.column_key, header_4, TableCellDataType.string, TableCellDataType.duration)

        header_5 = TableTextCell("keyOfColumn5", "Column With Algorithm Node Entries")
        definition_of_table_column_5 = TableColumnDefinition(header_5.column_key, header_5, TableCellDataType.string, TableCellDataType.algorithm_node)

        header_6 = TableTextCell("keyOfColumn6", "Column With Algorithm Train Entries")
        definition_of_table_column_6 = TableColumnDefinition(header_6.column_key, header_6, TableCellDataType.string, TableCellDataType.algorithm_train)

        all_column_definitions = [
            definition_of_table_column_1,
            definition_of_table_column_2,
            definition_of_table_column_3,
            definition_of_table_column_4,
            definition_of_table_column_5,
            definition_of_table_column_6,
        ]

        table_definition = TableDefinition("TableName", columns=all_column_definitions)

        self.interface_to_viriato.create_table(table_definition)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj.last_request, get_api_url() + "/user-outputs/tables")

        self.assertIsInstance(session_obj.last_body, dict)
        self.assertSetEqual(set(session_obj.last_body.keys()), {"name", "columns"})
        self.assertEqual(session_obj.last_body["name"], "TableName")
        self.assertIsInstance(session_obj.last_body["columns"], list)
        self.assertEqual(len(session_obj.last_body["columns"]), 6)

        columns_in_body = session_obj.last_body["columns"]

        self.assertIsInstance(columns_in_body[0], dict)
        self.assertSetEqual(set(columns_in_body[0].keys()), {"key", "header", "headerDataType", "columnDataType"})
        self.assertEqual(columns_in_body[0]["key"], "keyOfColumn1")
        self.assertEqual(columns_in_body[0]["header"], "Caption of Column With String Header and String Data")
        self.assertEqual(columns_in_body[0]["headerDataType"], "string")
        self.assertEqual(columns_in_body[0]["columnDataType"], "string")

        self.assertIsInstance(columns_in_body[1], dict)
        self.assertSetEqual(set(columns_in_body[1].keys()), {"key", "header", "headerDataType", "columnDataType"})
        self.assertEqual(columns_in_body[1]["key"], "keyOfColumn2")
        self.assertEqual(columns_in_body[1]["header"], "Column With Integer Entries")
        self.assertEqual(columns_in_body[1]["headerDataType"], "string")
        self.assertEqual(columns_in_body[1]["columnDataType"], "integer")

        self.assertIsInstance(columns_in_body[2], dict)
        self.assertSetEqual(set(columns_in_body[2].keys()), {"key", "header", "headerDataType", "columnDataType"})
        self.assertEqual(columns_in_body[2]["key"], "keyOfColumn3")
        self.assertEqual(columns_in_body[2]["header"], "Column With DateTime Entries")
        self.assertEqual(columns_in_body[2]["headerDataType"], "string")
        self.assertEqual(columns_in_body[2]["columnDataType"], "localDateTime")

        self.assertIsInstance(columns_in_body[3], dict)
        self.assertSetEqual(set(columns_in_body[3].keys()), {"key", "header", "headerDataType", "columnDataType"})
        self.assertEqual(columns_in_body[3]["key"], "keyOfColumn4")
        self.assertEqual(columns_in_body[3]["header"], "Column With Duration Entries")
        self.assertEqual(columns_in_body[3]["headerDataType"], "string")
        self.assertEqual(columns_in_body[3]["columnDataType"], "duration")

        self.assertIsInstance(columns_in_body[4], dict)
        self.assertSetEqual(set(columns_in_body[4].keys()), {"key", "header", "headerDataType", "columnDataType"})
        self.assertEqual(columns_in_body[4]["key"], "keyOfColumn5")
        self.assertEqual(columns_in_body[4]["header"], "Column With Algorithm Node Entries")
        self.assertEqual(columns_in_body[4]["headerDataType"], "string")
        self.assertEqual(columns_in_body[4]["columnDataType"], "algorithmNode")

        self.assertIsInstance(columns_in_body[5], dict)
        self.assertSetEqual(set(columns_in_body[5].keys()), {"key", "header", "headerDataType", "columnDataType"})
        self.assertEqual(columns_in_body[5]["key"], "keyOfColumn6")
        self.assertEqual(columns_in_body[5]["header"], "Column With Algorithm Train Entries")
        self.assertEqual(columns_in_body[5]["headerDataType"], "string")
        self.assertEqual(columns_in_body[5]["columnDataType"], "algorithmTrain")

    @mock.patch("requests.Session", side_effect=TestCreateTableTestSessionMock)
    def test_create_table_response(self, _):
        header_1 = TableTextCell("keyOfColumn1", "Caption of Column With String Header and String Data")
        definition_of_table_column_1 = TableColumnDefinition(header_1.column_key, header_1, TableCellDataType.string, TableCellDataType.string)

        header_2 = TableTextCell("keyOfColumn2", "Column With Integer Entries")
        definition_of_table_column_2 = TableColumnDefinition(header_2.column_key, header_2, TableCellDataType.string, TableCellDataType.integer)

        header_3 = TableTextCell("keyOfColumn3", "Column With DateTime Entries")
        definition_of_table_column_3 = TableColumnDefinition(header_3.column_key, header_3, TableCellDataType.string, TableCellDataType.local_date_time)

        header_4 = TableTextCell("keyOfColumn4", "Column With Duration Entries")
        definition_of_table_column_4 = TableColumnDefinition(header_4.column_key, header_4, TableCellDataType.string, TableCellDataType.duration)

        header_5 = TableTextCell("keyOfColumn5", "Column With Algorithm Node Entries")
        definition_of_table_column_5 = TableColumnDefinition(header_5.column_key, header_5, TableCellDataType.string, TableCellDataType.algorithm_node)

        header_6 = TableTextCell("keyOfColumn6", "Column With Algorithm Train Entries")
        definition_of_table_column_6 = TableColumnDefinition(header_6.column_key, header_6, TableCellDataType.string, TableCellDataType.algorithm_train)

        all_column_definitions = [
            definition_of_table_column_1,
            definition_of_table_column_2,
            definition_of_table_column_3,
            definition_of_table_column_4,
            definition_of_table_column_5,
            definition_of_table_column_6,
        ]

        table_definition = TableDefinition("TableName", columns=all_column_definitions)

        table_id = self.interface_to_viriato.create_table(table_definition)

        self.assertIsInstance(table_id, int)
        self.assertEqual(table_id, 11041)

    @mock.patch("requests.Session", side_effect=TestCreateTableTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
