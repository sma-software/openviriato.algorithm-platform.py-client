import datetime
import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.aidm import TimeWindow, AlgorithmTrain, AlgorithmTrainPathNode, StopStatus
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetTrains(unittest.TestCase):
    class GetTrainsTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = ("[\n"
                           "  {\n"
                           "    \"id\": 3516,\n"
                           "    \"code\": \"3516\",\n"
                           "    \"trainPathNodes\": [\n"
                           "      {\n"
                           "        \"id\": 2424,\n"
                           "        \"sectionTrackId\": null,\n"
                           "        \"nodeId\": 7,\n"
                           "        \"nodeTrackId\": 8,\n"
                           "        \"formationId\": 1187,\n"
                           "        \"movementTypeId\": null,\n"
                           "        \"arrivalTime\": \"2003-05-01T00:10:00\",\n"
                           "        \"departureTime\": \"2003-05-01T00:10:00\",\n"
                           "        \"minimumRunTime\": null,\n"
                           "        \"minimumStopTime\": \"P0D\",\n"
                           "        \"stopStatus\": \"commercialStop\",\n"
                           "        \"sequenceNumber\": 0\n"
                           "      },\n"
                           "      {\n"
                           "        \"id\": 2788,\n"
                           "        \"sectionTrackId\": 1175,\n"
                           "        \"nodeId\": 15,\n"
                           "        \"nodeTrackId\": 16,\n"
                           "        \"formationID\": 1187,\n"
                           "        \"movementTypeId\": null,\n"
                           "        \"arrivalTime\": \"2003-05-01T00:14:00\",\n"
                           "        \"departureTime\": \"2003-05-01T00:14:00\",\n"
                           "        \"minimumRunTime\": \"PT4M\",\n"
                           "        \"minimumStopTime\": \"P0D\",\n"
                           "        \"stopStatus\": \"passing\",\n"
                           "        \"sequenceNumber\": 1\n"
                           "      },\n"
                           "      {\n"
                           "        \"id\": 3152,\n"
                           "        \"sectionTrackId\": 1174,\n"
                           "        \"nodeId\": 10,\n"
                           "        \"nodeTrackId\": 12,\n"
                           "        \"formationID\": null,\n"
                           "        \"movementTypeId\": null,\n"
                           "        \"arrivalTime\": \"2003-05-01T00:19:00\",\n"
                           "        \"departureTime\": \"2003-05-01T00:19:00\",\n"
                           "        \"minimumRunTime\": \"PT5M\",\n"
                           "        \"minimumStopTime\": \"P0D\",\n"
                           "        \"stopStatus\": \"commercialStop\",\n"
                           "        \"sequenceNumber\": 2\n"
                           "      }\n"
                           "    ],\n"
                           "    \"debugString\": \"RVZH_3_1_J03 tt_(S)\"\n"
                           "  },\n"
                           "  {\n"
                           "    \"id\": 2060,\n"
                           "    \"code\": \"213\",\n"
                           "    \"trainPathNodes\": [\n"
                           "      {\n"
                           "        \"id\": 1332,\n"      
                           "        \"sectionTrackId\": null,\n"
                           "        \"nodeId\": 18,\n"
                           "        \"nodeTrackId\": null,\n"
                           "        \"formationID\": 1187,\n"
                           "        \"movementTypeId\": null,\n"
                           "        \"arrivalTime\": \"2003-05-01T00:05:00\",\n"
                           "        \"departureTime\": \"2003-05-01T00:05:00\",\n"
                           "        \"minimumRunTime\": null,\n"
                           "        \"minimumStopTime\": \"P0D\",\n"
                           "        \"stopStatus\": \"commercialStop\",\n"
                           "        \"sequenceNumber\": 0\n"
                           "      },\n"
                           "      {\n"
                           "        \"id\": 1696,\n"
                           "        \"sectionTrackId\": 1171,\n"
                           "        \"nodeId\": 10,\n"
                           "        \"nodeTrackId\": null,\n"
                           "        \"formationID\": null,\n"
                           "        \"movementTypeId\": null,\n"
                           "        \"arrivalTime\": \"2003-05-01T00:10:00\",\n"
                           "        \"departureTime\": \"2003-05-01T00:10:00\",\n"
                           "        \"minimumRunTime\": \"PT5M\",\n"
                           "        \"minimumStopTime\": \"P0D\",\n"
                           "        \"stopStatus\": \"commercialStop\",\n"
                           "        \"sequenceNumber\": 1\n"
                           "      }\n"
                           "    ],\n"
                           "    \"debugString\": \"RVZH_1_1_J03 tt_(G)\"\n"
                           "  }\n"
                           "]")

            return SessionMockFactory.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetTrainsTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetTrainsTestMockSession)
    def test_get_trains_request(self, mocked_get_obj):
        time_window = TimeWindow(from_time=datetime.datetime(2000, 1, 1, 1, 1),
                                 to_time=datetime.datetime(2004, 1, 1, 0, 0))

        self.interface_to_viriato.get_trains(time_window)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetTrainsTestMockSession__last_request, get_api_url() + '/trains')
        self.assertDictEqual(session_obj._GetTrainsTestMockSession__last_body,
                             dict(fromTime="2000-01-01T01:01:00",
                                  toTime="2004-01-01T00:00:00"))

    @mock.patch('requests.Session', side_effect=GetTrainsTestMockSession)
    def test_get_trains_response(self, mocked_get_obj):
        time_window = TimeWindow(from_time=datetime.datetime(2000, 1, 1, 1, 1),
                                 to_time=datetime.datetime(2004, 1, 1, 0, 0))

        listed_algorithm_trains = self.interface_to_viriato.get_trains(time_window)

        self.assertIsInstance(listed_algorithm_trains, list)
        self.assertEqual(listed_algorithm_trains.__len__(), 2)

        self.assertIsInstance(listed_algorithm_trains[0], AlgorithmTrain)
        self.assertEqual(listed_algorithm_trains[0].id, 3516)
        self.assertEqual(listed_algorithm_trains[0].debug_string, 'RVZH_3_1_J03 tt_(S)')
        self.assertEqual(listed_algorithm_trains[0].code, "3516")
        self.assertIsInstance(listed_algorithm_trains[0].train_path_nodes, list)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes.__len__(), 3)

        self.assertIsInstance(listed_algorithm_trains[0].train_path_nodes[0], AlgorithmTrainPathNode)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].id, 2424)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].section_track_id, None)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].node_id, 7)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].node_track_id, 8)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].formation_id, 1187)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].arrival_time,
                         datetime.datetime(2003, 5, 1, 0, 10))
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].departure_time,
                         datetime.datetime(2003, 5, 1, 0, 10))
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].minimum_run_time, None)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].minimum_stop_time, datetime.timedelta(0))
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].stop_status, StopStatus.commercial_stop)
        self.assertEqual(listed_algorithm_trains[0].train_path_nodes[0].sequence_number, 0)

    @mock.patch('requests.Session', side_effect=GetTrainsTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
