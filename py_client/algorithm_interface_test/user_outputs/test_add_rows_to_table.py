import unittest
from datetime import datetime, timedelta
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.aidm import AlgorithmNode, AlgorithmTrain, TableRow
from py_client.aidm.aidm_table_cell_classes import (
    TableTextCell,
    TableIntegerCell,
    TableDurationCell,
    TableLocalDateTimeCell,
    TableAlgorithmNodeCell,
    TableAlgorithmTrainCell,
)
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestAddRowsToTable(unittest.TestCase):
    class AddRowsToTableTestSessionMock(SessionMockTestBase):
        def post(self, request: str, json: dict):
            self._last_request = request
            self._last_body = json

            return APISessionMock.create_response_mock("", 200)

    @mock.patch("requests.Session", side_effect=AddRowsToTableTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=AddRowsToTableTestSessionMock)
    def test_add_rows_to_table_request(self, mocked_session_object):
        table_id = 11041
        cell_1 = TableTextCell("keyOfColumn1", "some_contents")
        cell_2 = TableIntegerCell("keyOfColumn2", 9)
        cell_4 = TableDurationCell("keyOfColumn4", timedelta(seconds=5))
        cell_5 = TableAlgorithmNodeCell("keyOfColumn5", AlgorithmNode(1, "code", "debug_string", node_tracks=[]).id)
        cell_3 = TableLocalDateTimeCell("keyOfColumn3", datetime(year=2003, month=5, day=21, hour=18, minute=4, second=59))
        cell_6 = TableAlgorithmTrainCell("keyOfColumn6", AlgorithmTrain(id=0, debug_string="dummy_train", train_path_nodes=[], code="test_train").id)
        table_row = TableRow([cell_1, cell_2, cell_3, cell_4, cell_5, cell_6])

        self.interface_to_viriato.add_rows_to_table(table_id, [table_row])

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj.last_request, get_api_url() + "/user-outputs/tables/11041/rows")

        self.assertIsInstance(session_obj.last_body, list)
        self.assertEqual(len(session_obj.last_body), 1)
        self.assertIsInstance(session_obj.last_body[0], dict)
        self.assertEqual(session_obj.last_body[0].keys(), {"row"})
        self.assertIsInstance(session_obj.last_body[0]["row"], list)
        self.assertEqual(len(session_obj.last_body[0]["row"]), 6)

        self.assertIsInstance(session_obj.last_body[0]["row"][0], dict)
        self.assertEqual(session_obj.last_body[0]["row"][0]["columnKey"], "keyOfColumn1")
        self.assertEqual(session_obj.last_body[0]["row"][0]["value"], "some_contents")

        self.assertIsInstance(session_obj.last_body[0]["row"][1], dict)
        self.assertEqual(session_obj.last_body[0]["row"][1]["columnKey"], "keyOfColumn2")
        self.assertEqual(session_obj.last_body[0]["row"][1]["value"], 9)

        self.assertIsInstance(session_obj.last_body[0]["row"][2], dict)
        self.assertEqual(session_obj.last_body[0]["row"][2]["columnKey"], "keyOfColumn3")
        self.assertEqual(session_obj.last_body[0]["row"][2]["value"], "2003-05-21T18:04:59")

        self.assertIsInstance(session_obj.last_body[0]["row"][3], dict)
        self.assertEqual(session_obj.last_body[0]["row"][3]["columnKey"], "keyOfColumn4")
        self.assertEqual(session_obj.last_body[0]["row"][3]["value"], "PT5S")

        self.assertIsInstance(session_obj.last_body[0]["row"][4], dict)
        self.assertEqual(session_obj.last_body[0]["row"][4]["columnKey"], "keyOfColumn5")
        self.assertEqual(session_obj.last_body[0]["row"][4]["nodeId"], 1)

        self.assertIsInstance(session_obj.last_body[0]["row"][5], dict)
        self.assertEqual(session_obj.last_body[0]["row"][5]["columnKey"], "keyOfColumn6")
        self.assertEqual(session_obj.last_body[0]["row"][5]["trainId"], 0)

    @mock.patch("requests.Session", side_effect=AddRowsToTableTestSessionMock)
    def test_add_rows_to_table_one_row_response(self, _):
        table_id = 11041
        cell_1 = TableTextCell("keyOfColumn1", "some_contents")
        cell_2 = TableIntegerCell("keyOfColumn2", 9)
        cell_4 = TableDurationCell("keyOfColumn4", timedelta(seconds=5))
        cell_5 = TableAlgorithmNodeCell("keyOfColumn5", AlgorithmNode(1, "code", "debug_string", node_tracks=[]).id)
        cell_3 = TableLocalDateTimeCell("keyOfColumn3", datetime(year=2003, month=5, day=21, hour=18, minute=4, second=59))
        cell_6 = TableAlgorithmTrainCell("keyOfColumn6", AlgorithmTrain(id=0, debug_string="dummy_train", train_path_nodes=[], code="dummy_train").id)
        table_row = TableRow([cell_1, cell_2, cell_3, cell_4, cell_5, cell_6])

        none_response = self.interface_to_viriato.add_rows_to_table(table_id, [table_row])

        self.assertIsNone(none_response)

    @mock.patch("requests.Session", side_effect=AddRowsToTableTestSessionMock)
    def test_add_empty_list_of_rows_to_table_response(self, _):
        table_id = 1231

        none_response = self.interface_to_viriato.add_rows_to_table(table_id, [])

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj.last_request, get_api_url() + "/user-outputs/tables/1231/rows")

        self.assertIsInstance(session_obj.last_body, list)
        self.assertEqual(len(session_obj.last_body), 0)

        self.assertIsNone(none_response)

    @mock.patch("requests.Session", side_effect=AddRowsToTableTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
