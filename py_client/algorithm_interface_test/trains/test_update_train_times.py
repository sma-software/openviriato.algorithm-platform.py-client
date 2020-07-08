import datetime
import unittest
from unittest import mock

import py_client.aidm.aidm_algorithm_classes
import py_client.aidm.aidm_train_path_node_classes as AIDM_classes
import py_client.aidm.aidm_update_classes
from py_client import algorithm_interface
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, SessionMockTestBase


class TestUpdateTrainTimes(unittest.TestCase):
    class UpdateTrainTimesTestMockSession(SessionMockTestBase):
        # to replace session.get:
        def put(self, request, json):
            self.__last_body = json
            self.__last_request = request
            json_string = ("{\n"
                           "                \"ID\": 2060,\n"
                           "                \"TrainPathNodes\": [\n"
                           "                    {\n"
                           "                        \"ID\": 1332,\n"
                           "                        \"SectionTrackID\": null,\n"
                           "                        \"node_id\": 18,\n"
                           "                        \"node_track_id\": null,\n"
                           "                        \"FormationID\": 1187,\n"
                           "                        \"ArrivalTime\": \"2003-05-01T00:04:00\",\n"
                           "                        \"DepartureTime\": \"2003-05-01T00:05:00\",\n"
                           "                        \"MinimumRunTime\": null,\n"
                           "                        \"MinimumStopTime\": \"P0D\",\n"
                           "                        \"StopStatus\": \"commercialStop\",\n"
                           "                        \"SequenceNumber\": 0\n"
                           "                    },\n"
                           "                    {\n"
                           "                        \"ID\": 1696,\n"
                           "                        \"SectionTrackID\": 1172,\n"
                           "                        \"node_id\": 10,\n"
                           "                        \"node_track_id\": null,\n"
                           "                        \"FormationID\": null,\n"
                           "                        \"ArrivalTime\": \"2003-05-01T00:10:00\",\n"
                           "                        \"DepartureTime\": \"2003-05-01T00:10:00\",\n"
                           "                        \"MinimumRunTime\": \"PT5M\",\n"
                           "                        \"MinimumStopTime\": \"P0D\",\n"
                           "                        \"StopStatus\": \"commercialStop\",\n"
                           "                        \"SequenceNumber\": 1\n"
                           "                    }\n"
                           "                ],\n"
                           "                \"DebugString\": \"Mocked RVZH_1_1_J03 tt_(G)\"\n"
                           "            }")

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: py_client.algorithm_interface.algorithm_interface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=UpdateTrainTimesTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=UpdateTrainTimesTestMockSession)
    def test_update_train_times_request(self, mocked_get_obj):
        train_id = 2060
        update_train_time_nodes = [py_client.aidm.aidm_update_classes.UpdateTrainTimesNode(train_path_node_id=1332,
                                                                                           arrival_time=datetime.datetime(2003, 5, 1, 0, 4),
                                                                                           departure_time=datetime.datetime(2003, 5, 1, 0, 5))]

        self.interface_to_viriato.update_train_times(train_id, update_train_time_nodes)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._UpdateTrainTimesTestMockSession__last_request,
                         get_api_url() + '/trains/2060/train-path-nodes:update-times')
        self.assertListEqual(session_obj._UpdateTrainTimesTestMockSession__last_body, [{"TrainPathNodeID": 1332,
                                                                                        "ArrivalTime":
                                                                                            "2003-05-01T00:04:00",
                                                                                        "DepartureTime":
                                                                                            "2003-05-01T00:05:00",
                                                                                        'MinimumRunTime': None,
                                                                                        'MinimumStopTime': None,
                                                                                        'StopStatus': None}])

    @mock.patch('requests.Session', side_effect=UpdateTrainTimesTestMockSession)
    def test_update_train_times_response(self, mocked_get_obj):
        train_id = 2060
        update_train_time_nodes = [py_client.aidm.aidm_update_classes.UpdateTrainTimesNode(train_path_node_id=1332,
                                                                                           arrival_time=datetime.datetime(2003, 5, 1, 0, 4),
                                                                                           departure_time=datetime.datetime(2003, 5, 1, 0, 5))]

        updated_algorithm_train = self.interface_to_viriato.update_train_times(train_id, update_train_time_nodes)

        self.assertIsInstance(updated_algorithm_train, py_client.aidm.aidm_algorithm_classes.AlgorithmTrain)
        self.assertEqual(updated_algorithm_train.debug_string, 'Mocked RVZH_1_1_J03 tt_(G)')
        self.assertEqual(updated_algorithm_train.id, 2060)
        self.assertIsInstance(updated_algorithm_train.train_path_nodes , list)
        self.assertIsInstance(updated_algorithm_train.train_path_nodes[0], AIDM_classes.AlgorithmTrainPathNode)

    @mock.patch('requests.Session', side_effect=UpdateTrainTimesTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
