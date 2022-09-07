import datetime
import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.aidm import StopStatus, StationEntryOrExit
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetSeparationTimeInStationForEntryOrExit(unittest.TestCase):
    class GetSeparationTimeInStationForEntryOrExitTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = """{ "separationTime": "P0D"}"""

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=GetSeparationTimeInStationForEntryOrExitTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetSeparationTimeInStationForEntryOrExitTestMockSession)
    def test_get_separation_time_in_station_for_planned_train_paths_request_no_stop_status(self, mocked_get_obj):
        node_id = 123
        preceding_train_path_node_id = 80
        preceding_train_stop_status = None
        preceding_station_entry_or_exit = StationEntryOrExit("exit")
        succeeding_train_path_node_id = 123
        succeeding_train_stop_status = None
        succeeding_station_entry_or_exit = StationEntryOrExit("entry")

        self.interface_to_viriato.get_separation_time_in_station_for_planned_train_paths(
            node_id,
            preceding_train_path_node_id,
            preceding_train_stop_status,
            preceding_station_entry_or_exit,
            succeeding_train_path_node_id,
            succeeding_train_stop_status,
            succeeding_station_entry_or_exit,
        )

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetSeparationTimeInStationForEntryOrExitTestMockSession__last_request, get_api_url() + "/nodes/123/separation-times")
        expected_query_parameters = dict(precedingTrainPathNodeId=80, precedingEntryOrExit="exit", succeedingTrainPathNodeId=123, succeedingEntryOrExit="entry")

        self.assertDictEqual(session_obj._GetSeparationTimeInStationForEntryOrExitTestMockSession__last_body, expected_query_parameters)

    @mock.patch("requests.Session", side_effect=GetSeparationTimeInStationForEntryOrExitTestMockSession)
    def test_get_separation_time_in_station_for_planned_train_paths_request_one_stop_status(self, mocked_get_obj):
        node_id = 123
        preceding_train_path_node_id = 80
        preceding_train_stop_status = StopStatus("passing")
        preceding_station_entry_or_exit = StationEntryOrExit("exit")
        succeeding_train_path_node_id = 123
        succeeding_train_stop_status = None
        succeeding_station_entry_or_exit = StationEntryOrExit("entry")

        self.interface_to_viriato.get_separation_time_in_station_for_planned_train_paths(
            node_id,
            preceding_train_path_node_id,
            preceding_train_stop_status,
            preceding_station_entry_or_exit,
            succeeding_train_path_node_id,
            succeeding_train_stop_status,
            succeeding_station_entry_or_exit,
        )

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetSeparationTimeInStationForEntryOrExitTestMockSession__last_request, get_api_url() + "/nodes/123/separation-times")
        expected_query_parameters = dict(
            precedingTrainPathNodeId=80,
            precedingStopStatus="passing",
            precedingEntryOrExit="exit",
            succeedingTrainPathNodeId=123,
            succeedingEntryOrExit="entry",
        )
        self.assertDictEqual(session_obj._GetSeparationTimeInStationForEntryOrExitTestMockSession__last_body, expected_query_parameters)

    @mock.patch("requests.Session", side_effect=GetSeparationTimeInStationForEntryOrExitTestMockSession)
    def test_get_separation_time_in_station_for_planned_train_paths_request_both_stop_status(self, mocked_get_obj):
        node_id = 123
        preceding_train_path_node_id = 80
        preceding_train_stop_status = StopStatus("commercialStop")
        preceding_station_entry_or_exit = StationEntryOrExit("exit")
        succeeding_train_path_node_id = 123
        succeeding_train_stop_status = StopStatus("passing")
        succeeding_station_entry_or_exit = StationEntryOrExit("entry")

        self.interface_to_viriato.get_separation_time_in_station_for_planned_train_paths(
            node_id,
            preceding_train_path_node_id,
            preceding_train_stop_status,
            preceding_station_entry_or_exit,
            succeeding_train_path_node_id,
            succeeding_train_stop_status,
            succeeding_station_entry_or_exit,
        )

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetSeparationTimeInStationForEntryOrExitTestMockSession__last_request, get_api_url() + "/nodes/123/separation-times")
        expected_query_parameters = dict(
            precedingTrainPathNodeId=80,
            precedingStopStatus="commercialStop",
            precedingEntryOrExit="exit",
            succeedingTrainPathNodeId=123,
            succeedingEntryOrExit="entry",
            succeedingStopStatus="passing",
        )

        self.assertDictEqual(session_obj._GetSeparationTimeInStationForEntryOrExitTestMockSession__last_body, expected_query_parameters)

    @mock.patch("requests.Session", side_effect=GetSeparationTimeInStationForEntryOrExitTestMockSession)
    def test_get_separation_time_in_station_for_planned_train_paths_response(self, mocked_get_obj):
        node_id = 123
        preceding_train_path_node_id = 80
        preceding_train_stop_status = StopStatus("passing")
        preceding_station_entry_or_exit = StationEntryOrExit("exit")
        succeeding_train_path_node_id = 123
        succeeding_train_stop_status = StopStatus("commercialStop")
        succeeding_station_entry_or_exit = StationEntryOrExit("entry")

        separation_time = self.interface_to_viriato.get_separation_time_in_station_for_planned_train_paths(
            node_id,
            preceding_train_path_node_id,
            preceding_train_stop_status,
            preceding_station_entry_or_exit,
            succeeding_train_path_node_id,
            succeeding_train_stop_status,
            succeeding_station_entry_or_exit,
        )

        self.assertIsInstance(separation_time, datetime.timedelta)
        self.assertEqual(separation_time, datetime.timedelta(seconds=0))

    @mock.patch("requests.Session", side_effect=GetSeparationTimeInStationForEntryOrExitTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
