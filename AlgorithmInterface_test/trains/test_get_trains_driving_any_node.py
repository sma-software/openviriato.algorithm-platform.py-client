import datetime
import unittest
from unittest import mock
from AIDMClasses import TimeWindow, AlgorithmTrain, AlgorithmTrainPathNode, StopStatus
from AlgorithmInterface.AlgorithmInterface import AlgorithmInterface
import AlgorithmInterface_test.test_helper.SessionMockFactory as SessionMockFactory
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetTrainsDrivingAnyNode(unittest.TestCase):
    class GetTrainsDrivingAnyNodeTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = (
                "[\n"
                "  {\n"
                "    \"ID\": 2060,\n"
                "    \"TrainPathNodes\": [\n"
                "      {\n"
                "        \"ID\": 1332,\n"
                "        \"SectionTrackID\": null,\n"
                "        \"NodeID\": 18,\n"
                "        \"NodeTrackID\": null,\n"
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
                "        \"NodeID\": 10,\n"
                "        \"NodeTrackID\": null,\n"
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

    interface_to_viriato: AlgorithmInterface

    @mock.patch('requests.Session', side_effect=GetTrainsDrivingAnyNodeTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetTrainsDrivingAnyNodeTestMockSession)
    def test_get_trains_driving_any_node_request(self, mocked_get_obj):
        time_window = TimeWindow(FromTime=datetime.datetime(2000, 1, 1, 1, 1),
                                 ToTime=datetime.datetime(2004, 1, 1, 0, 0))
        node_ids = [10]

        self.interface_to_viriato.get_trains_driving_any_node(time_window, nodeIDs=node_ids)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetTrainsDrivingAnyNodeTestMockSession__last_request, get_api_url() + '/trains')
        self.assertDictEqual(session_obj._GetTrainsDrivingAnyNodeTestMockSession__last_body,
                             dict(FromTime="2000-01-01T01:01:00",
                                  ToTime="2004-01-01T00:00:00",
                                  NodeFilter=[10]))

    @mock.patch('requests.Session', side_effect=GetTrainsDrivingAnyNodeTestMockSession)
    def test_get_trains_driving_any_node_response(self, mocked_get_obj):
        time_window = TimeWindow(FromTime=datetime.datetime(2000, 1, 1, 1, 1),
                                 ToTime=datetime.datetime(2004, 1, 1, 0, 0))
        node_ids = [10]

        listed_algorithm_trains = self.interface_to_viriato.get_trains_driving_any_node(time_window, nodeIDs=node_ids)

        self.assertIsInstance(listed_algorithm_trains, list)
        self.assertEqual(listed_algorithm_trains.__len__(), 1)

        self.assertIsInstance(listed_algorithm_trains[0], AlgorithmTrain)
        self.assertEqual(listed_algorithm_trains[0].ID, 2060)
        self.assertEqual(listed_algorithm_trains[0].DebugString, 'RVZH_1_1_J03 tt_(G)')
        self.assertIsInstance(listed_algorithm_trains[0].TrainPathNodes, list)
        self.assertEqual(listed_algorithm_trains[0].TrainPathNodes.__len__(), 2)

        self.assertIsInstance(listed_algorithm_trains[0].TrainPathNodes[0], AlgorithmTrainPathNode)
        self.assertEqual(listed_algorithm_trains[0].TrainPathNodes[0].ID, 1332)
        self.assertEqual(listed_algorithm_trains[0].TrainPathNodes[0].SectionTrackID, None)
        self.assertEqual(listed_algorithm_trains[0].TrainPathNodes[0].NodeID, 18)
        self.assertEqual(listed_algorithm_trains[0].TrainPathNodes[0].NodeTrackID, None)
        self.assertEqual(listed_algorithm_trains[0].TrainPathNodes[0].FormationID, 1187)
        self.assertEqual(listed_algorithm_trains[0].TrainPathNodes[0].ArrivalTime,
                         datetime.datetime(2003, 5, 1, 0, 5))
        self.assertEqual(listed_algorithm_trains[0].TrainPathNodes[0].DepartureTime,
                         datetime.datetime(2003, 5, 1, 0, 5))
        self.assertEqual(listed_algorithm_trains[0].TrainPathNodes[0].MinimumRunTime, None)
        self.assertEqual(listed_algorithm_trains[0].TrainPathNodes[0].MinimumStopTime, datetime.timedelta(0))
        self.assertEqual(listed_algorithm_trains[0].TrainPathNodes[0].StopStatus, StopStatus['commercialStop'])
        self.assertEqual(listed_algorithm_trains[0].TrainPathNodes[0].SequenceNumber, 0)

    @mock.patch('requests.Session', side_effect=GetTrainsDrivingAnyNodeTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
