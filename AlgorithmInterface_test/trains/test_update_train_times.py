import datetime
import unittest
from unittest import mock

import AIDMClasses.AIDM_Algorithm_classes
import AIDMClasses.AIDM_Update_classes
import AIDMClasses.AIDM_TrainPathNode_classes as AIDM_classes
import AlgorithmInterface.AlgorithmInterface
import AlgorithmInterface_test.test_helper.SessionMockFactory as SessionMockFactory
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import \
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
                           "                        \"NodeID\": 18,\n"
                           "                        \"NodeTrackID\": null,\n"
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
                           "                        \"NodeID\": 10,\n"
                           "                        \"NodeTrackID\": null,\n"
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

    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=UpdateTrainTimesTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=UpdateTrainTimesTestMockSession)
    def test_update_train_times_request(self, mocked_get_obj):
        train_id = 2060
        update_train_time_nodes = [AIDMClasses.AIDM_Update_classes.UpdateTrainTimesNode(TrainPathNodeID=1332,
                                                                                        ArrivalTime=datetime.datetime(2003, 5, 1, 0, 4),
                                                                                        DepartureTime=datetime.datetime(2003, 5, 1, 0, 5))]

        self.interface_to_viriato.update_train_times(train_id, update_train_time_nodes)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._UpdateTrainTimesTestMockSession__last_request,
                         get_api_url() + '/trains/2060/train-path-nodes')
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
        update_train_time_nodes = [AIDMClasses.AIDM_Update_classes.UpdateTrainTimesNode(TrainPathNodeID=1332,
                                                                                        ArrivalTime=datetime.datetime(2003, 5, 1, 0, 4),
                                                                                        DepartureTime=datetime.datetime(2003, 5, 1, 0, 5))]

        updated_algorithm_train = self.interface_to_viriato.update_train_times(train_id, update_train_time_nodes)

        self.assertIsInstance(updated_algorithm_train, AIDMClasses.AIDM_Algorithm_classes.AlgorithmTrain)
        self.assertEqual(updated_algorithm_train.DebugString, 'Mocked RVZH_1_1_J03 tt_(G)')
        self.assertEqual(updated_algorithm_train.ID, 2060)
        self.assertIsInstance(updated_algorithm_train.TrainPathNodes, list)
        self.assertIsInstance(updated_algorithm_train.TrainPathNodes[0], AIDM_classes.TrainPathNode)

    @mock.patch('requests.Session', side_effect=UpdateTrainTimesTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
