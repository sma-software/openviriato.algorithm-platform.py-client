import datetime
import unittest
from unittest import mock
from py_client.aidm import TimeWindow, AlgorithmTrain, AlgorithmTrainPathNode, StopStatus
from py_client.algorithm_interface import algorithm_interface_factory
import algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetTrains(unittest.TestCase):
    class GetTrainsTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = ("[\n"
                           "  {\n"
                           "    \"ID\": 3516,\n"
                           "    \"TrainPathNodes\": [\n"
                           "      {\n"
                           "        \"ID\": 2424,\n"
                           "        \"SectionTrackID\": null,\n"
                           "        \"node_id\": 7,\n"
                           "        \"node_track_id\": 8,\n"
                           "        \"FormationID\": 1187,\n"
                           "        \"ArrivalTime\": \"2003-05-01T00:10:00\",\n"
                           "        \"DepartureTime\": \"2003-05-01T00:10:00\",\n"
                           "        \"MinimumRunTime\": null,\n"
                           "        \"MinimumStopTime\": \"P0D\",\n"
                           "        \"StopStatus\": \"commercialStop\",\n"
                           "        \"SequenceNumber\": 0\n"
                           "      },\n"
                           "      {\n"
                           "        \"ID\": 2788,\n"
                           "        \"SectionTrackID\": 1175,\n"
                           "        \"node_id\": 15,\n"
                           "        \"node_track_id\": 16,\n"
                           "        \"FormationID\": 1187,\n"
                           "        \"ArrivalTime\": \"2003-05-01T00:14:00\",\n"
                           "        \"DepartureTime\": \"2003-05-01T00:14:00\",\n"
                           "        \"MinimumRunTime\": \"PT4M\",\n"
                           "        \"MinimumStopTime\": \"P0D\",\n"
                           "        \"StopStatus\": \"passing\",\n"
                           "        \"SequenceNumber\": 1\n"
                           "      },\n"
                           "      {\n"
                           "        \"ID\": 3152,\n"
                           "        \"SectionTrackID\": 1174,\n"
                           "        \"node_id\": 10,\n"
                           "        \"node_track_id\": 12,\n"
                           "        \"FormationID\": null,\n"
                           "        \"ArrivalTime\": \"2003-05-01T00:19:00\",\n"
                           "        \"DepartureTime\": \"2003-05-01T00:19:00\",\n"
                           "        \"MinimumRunTime\": \"PT5M\",\n"
                           "        \"MinimumStopTime\": \"P0D\",\n"
                           "        \"StopStatus\": \"commercialStop\",\n"
                           "        \"SequenceNumber\": 2\n"
                           "      }\n"
                           "    ],\n"
                           "    \"DebugString\": \"RVZH_3_1_J03 tt_(S)\"\n"
                           "  },\n"
                           "  {\n"
                           "    \"ID\": 2060,\n"
                           "    \"TrainPathNodes\": [\n"
                           "      {\n"
                           "        \"ID\": 1332,\n"
                           "        \"SectionTrackID\": null,\n"
                           "        \"node_id\": 18,\n"
                           "        \"node_track_id\": null,\n"
                           "        \"FormationID\": 1187,\n"
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
                             dict(FromTime="2000-01-01T01:01:00",
                                  ToTime="2004-01-01T00:00:00"))

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
