import datetime
import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.aidm import TimeWindow, AlgorithmTrain, AlgorithmTrainPathNode, StopStatus
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetTrainsDrivingAnyNode(unittest.TestCase):
    class GetTrainsDrivingAnyNodeTestMockSession(SessionMockTestBase):
        def get(self, request, params, json):
            self.__last_body = json
            self.__last_params = params
            self.__last_request = request
            json_string = (
                "[\n"
                "  {\n"
                '    "id": 2060,\n'
                '    "code": "TestGetTrainsDrivingAnyNode",\n'
                '    "trainPathNodes": [\n'
                "      {\n"
                '        "id": 1332,\n'
                '        "SectionTrackID": null,\n'
                '        "nodeId": 18,\n'
                '        "nodeTrackId": null,\n'
                '        "formationId": 1187,\n'
                '        "movementTypeId": null,\n'
                '        "arrivalTime": "2003-05-01T00:05:00",\n'
                '        "departureTime": "2003-05-01T00:05:00",\n'
                '        "minimumRunTime": null,\n'
                '        "minimumStopTime": "P0D",\n'
                '        "stopStatus": "commercialStop",\n'
                '        "sequenceNumber": 0\n'
                "      },\n"
                "      {\n"
                '        "id": 1696,\n'
                '        "sectionTrackId": 1171,\n'
                '        "nodeId": 10,\n'
                '        "nodeTrackId": null,\n'
                '        "formationId": null,\n'
                '        "movementTypeId": null,\n'
                '        "arrivalTime": "2003-05-01T00:10:00",\n'
                '        "departureTime": "2003-05-01T00:10:00",\n'
                '        "minimumRunTime": "PT5M",\n'
                '        "minimumStopTime": "P0D",\n'
                '        "stopStatus": "commercialStop",\n'
                '        "sequenceNumber": 1\n'
                "      }\n"
                "    ],\n"
                '    "debugString": "RVZH_1_1_J03 tt_(G)"\n'
                "  }\n"
                "]"
            )

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch("requests.Session", side_effect=GetTrainsDrivingAnyNodeTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetTrainsDrivingAnyNodeTestMockSession)
    def test_get_trains_driving_any_node_request(self, mocked_get_obj):
        time_window = TimeWindow(from_time=datetime.datetime(2000, 1, 1, 1, 1), to_time=datetime.datetime(2004, 1, 1, 0, 0))
        node_ids = [10]

        self.interface_to_viriato.get_trains_driving_any_node(time_window, node_ids=node_ids)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetTrainsDrivingAnyNodeTestMockSession__last_request, get_api_url() + "/trains")
        self.assertDictEqual(
            session_obj._GetTrainsDrivingAnyNodeTestMockSession__last_params, dict(fromTime="2000-01-01T01:01:00", toTime="2004-01-01T00:00:00")
        )

        self.assertDictEqual(session_obj._GetTrainsDrivingAnyNodeTestMockSession__last_body, dict(filterNodeIds=[10]))

    @mock.patch("requests.Session", side_effect=GetTrainsDrivingAnyNodeTestMockSession)
    def test_get_trains_driving_any_node_response(self, mocked_get_obj):
        time_window = TimeWindow(from_time=datetime.datetime(2000, 1, 1, 1, 1), to_time=datetime.datetime(2004, 1, 1, 0, 0))
        node_ids = [10]

        listed_algorithm_trains = self.interface_to_viriato.get_trains_driving_any_node(time_window, node_ids=node_ids)

        self.assertIsInstance(listed_algorithm_trains, list)
        self.assertEqual(listed_algorithm_trains.__len__(), 1)

        self.assertIsInstance(listed_algorithm_trains[0], AlgorithmTrain)
        self.assertEqual(listed_algorithm_trains[0].id, 2060)
        self.assertEqual(listed_algorithm_trains[0].debug_string, "RVZH_1_1_J03 tt_(G)")
        self.assertEqual(listed_algorithm_trains[0].code, "TestGetTrainsDrivingAnyNode")
        self.assertIsInstance(listed_algorithm_trains[0].train_path_nodes, list)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes.__len__(), 2)

        self.assertIsInstance(listed_algorithm_trains[0].train_path_nodes[0], AlgorithmTrainPathNode)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].id, 1332)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].section_track_id, None)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].node_id, 18)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].node_track_id, None)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].formation_id, 1187)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].arrival_time, datetime.datetime(2003, 5, 1, 0, 5))
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].departure_time, datetime.datetime(2003, 5, 1, 0, 5))
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].minimum_run_time, None)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].minimum_stop_time, datetime.timedelta(0))
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].stop_status, StopStatus.commercial_stop)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].sequence_number, 0)

    @mock.patch("requests.Session", side_effect=GetTrainsDrivingAnyNodeTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
