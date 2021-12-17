import datetime
import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.aidm import TimeWindow, AlgorithmTrain, AlgorithmTrainPathNode, StopStatus
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetTrainsCutToTimeRangeDrivingAnyNode(unittest.TestCase):
    class GetTrainsCutToTimeRangeDrivingAnyNodeTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = (
                "[\n"
                "  {\n"
                "    \"ID\": 2060,\n"
                "    \"code\": \"TestGetTrainsCutToTimeRangeDrivingAnyNode\",\n"
                "    \"train_path_nodes\": [\n"
                "      {\n"
                "        \"ID\": 1332,\n"
                "        \"SectionTrackID\": null,\n"
                "        \"node_id\": 18,\n"
                "        \"node_track_id\": null,\n"
                "        \"FormationID\": 1187,\n"
                "        \"MovementTypeId\": null,\n"
                "        \"ArrivalTime\": \"2003-05-01T00:05:00\",\n"
                "        \"DepartureTime\": \"2003-05-01T00:05:00\",\n"
                "        \"MinimumRunTime\": null,\n"
                "        \"MinimumStopTime\": \"P0D\",\n"
                "        \"StopStatus\": \"commercialStop\",\n"
                "        \"SequenceNumber\": 0\n"
                "      },\n"
                "      {\n"
                "        \"ID\": 1696,\n"
                "        \"SectionTrackID\": 1171,\n"
                "        \"node_id\": 10,\n"
                "        \"node_track_id\": null,\n"
                "        \"FormationID\": null,\n"
                "        \"MovementTypeId\": null,\n"
                "        \"ArrivalTime\": \"2003-05-01T00:10:00\",\n"
                "        \"DepartureTime\": \"2003-05-01T00:10:00\",\n"
                "        \"MinimumRunTime\": \"PT5M\",\n"
                "        \"MinimumStopTime\": \"P0D\",\n"
                "        \"StopStatus\": \"commercialStop\",\n"
                "        \"SequenceNumber\": 1\n"
                "      }\n"
                "    ],\n"
                "    \"DebugString\": \"RVZH_1_1_J03 tt_(G)\"\n"
                "  }\n"
                "]")

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetTrainsCutToTimeRangeDrivingAnyNodeTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetTrainsCutToTimeRangeDrivingAnyNodeTestMockSession)
    def test_get_trains_cut_to_time_range_driving_any_node_request(self, mocked_get_obj):
        time_window = TimeWindow(from_time=datetime.datetime(2000, 1, 1, 1, 1),
                                 to_time=datetime.datetime(2004, 1, 1, 0, 0))
        node_ids = [10, 11, 18]

        self.interface_to_viriato.get_trains_cut_to_time_range_driving_any_node(time_window, node_ids=node_ids)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetTrainsCutToTimeRangeDrivingAnyNodeTestMockSession__last_request,
                         get_api_url() + '/trains')
        self.assertDictEqual(session_obj._GetTrainsCutToTimeRangeDrivingAnyNodeTestMockSession__last_body,
                             dict(fromTime="2000-01-01T01:01:00",
                                  toTime="2004-01-01T00:00:00",
                                  cutTrain=True,
                                  nodeFilter=[10, 11, 18]))

    @mock.patch('requests.Session', side_effect=GetTrainsCutToTimeRangeDrivingAnyNodeTestMockSession)
    def test_get_trains_cut_to_time_range_driving_any_node_response(self, mocked_get_obj):
        time_window = TimeWindow(from_time=datetime.datetime(2000, 1, 1, 1, 1),
                                 to_time=datetime.datetime(2004, 1, 1, 0, 0))
        node_ids = [10]

        listed_algorithm_trains = self.interface_to_viriato.get_trains_cut_to_time_range_driving_any_node(
            time_window,
            node_ids=node_ids)

        self.assertIsInstance(listed_algorithm_trains, list)
        self.assertEqual(listed_algorithm_trains.__len__(), 1)

        self.assertIsInstance(listed_algorithm_trains[0], AlgorithmTrain)
        self.assertEqual(listed_algorithm_trains[0].id, 2060)
        self.assertEqual(listed_algorithm_trains[0].debug_string, 'RVZH_1_1_J03 tt_(G)')
        self.assertEqual(listed_algorithm_trains[0].code, "TestGetTrainsCutToTimeRangeDrivingAnyNode")
        self.assertIsInstance(listed_algorithm_trains[0].train_path_nodes, list)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes.__len__(), 2)

        self.assertIsInstance(listed_algorithm_trains[0].train_path_nodes[0], AlgorithmTrainPathNode)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].id, 1332)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].section_track_id, None)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].node_id, 18)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].node_track_id, None)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].formation_id, 1187)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].arrival_time,
                         datetime.datetime(2003, 5, 1, 0, 5))
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].departure_time,
                         datetime.datetime(2003, 5, 1, 0, 5))
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].minimum_run_time, None)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].minimum_stop_time, datetime.timedelta(0))
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].stop_status, StopStatus.commercial_stop)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].sequence_number, 0)

    @mock.patch('requests.Session', side_effect=GetTrainsCutToTimeRangeDrivingAnyNodeTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
