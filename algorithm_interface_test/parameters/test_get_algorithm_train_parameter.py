import unittest
from unittest import mock

import py_client.aidm.aidm_algorithm_classes
import algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.aidm import aidm_train_path_node_classes
from py_client.algorithm_interface import algorithm_interface_factory
from algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, SessionMockTestBase


class TestGetAlgorithmTrainParameter(unittest.TestCase):
    class GetAlgorithmTrainParameterTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            json__string = ("{\n"
                            "   \"Key\": \"templateTrainParameter\",\n"
                            "   \"Value\": {\n"
                            "       \"ID\": 2060,\n"
                            "       \"TrainPathNodes\": [\n"
                            "           {\n"
                            "                \"ID\": 1332,\n"
                            "                \"SectionTrackID\": null,\n"
                            "                \"node_id\": 18,\n"
                            "                \"node_track_id\": null,\n"
                            "                \"FormationID\": 1187,\n"
                            "                \"ArrivalTime\": \"2003-05-01T00:04:00\",\n"
                            "                \"DepartureTime\": \"2003-05-01T00:05:30\",\n"
                            "                \"MinimumRunTime\": null,\n"
                            "                \"MinimumStopTime\": \"P0D\",\n"
                            "                \"StopStatus\": \"operationalStop\",\n"
                            "                \"SequenceNumber\": 0\n"
                            "           },\n"
                            "           {\n"
                            "                \"ID\": 1696,\n"
                            "                \"SectionTrackID\": 1172,\n"
                            "                \"node_id\": 10,\n"
                            "                \"node_track_id\": null,\n"
                            "                \"FormationID\": null,\n"
                            "                \"ArrivalTime\": \"2003-05-01T00:10:30\",\n"
                            "                \"DepartureTime\": \"2003-05-01T00:10:30\",\n"
                            "                \"MinimumRunTime\": \"PT5M\",\n"
                            "                \"MinimumStopTime\": \"P0D\",\n"
                            "                \"StopStatus\": \"commercialStop\",\n"
                            "                \"SequenceNumber\": 1\n"
                            "           }\n"
                            "       ],\n"
                            "       \"DebugString\": \"RVZH_1_1_J03 tt_(G)\"\n"
                            "   }\n"
                            " }")
            return APISessionMock.create_response_mock(json__string, 200)

    @mock.patch('requests.Session', side_effect=GetAlgorithmTrainParameterTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetAlgorithmTrainParameterTestSessionMock)
    def test_get_algorithm_train_parameter_request(self, mocked_get_obj):
        key = "somTestTrainParameterKey"

        self.interface_to_viriato.get_algorithm_train_parameter(key)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetAlgorithmTrainParameterTestSessionMock__last_request, get_api_url() +
                         '/parameters/somTestTrainParameterKey')
        self.assertDictEqual(session_obj._GetAlgorithmTrainParameterTestSessionMock__last_body, {})

    @mock.patch('requests.Session', side_effect=GetAlgorithmTrainParameterTestSessionMock)
    def test_get_algorithm_train_parameter_response(self, mocked_get_obj):
        key = "somTestTrainParameterKey"

        test_algorithm_train = self.interface_to_viriato.get_algorithm_train_parameter(key)

        self.assertIsInstance(test_algorithm_train, py_client.aidm.aidm_algorithm_classes.AlgorithmTrain)
        self.assertEqual(test_algorithm_train.debug_string, "RVZH_1_1_J03 tt_(G)")
        self.assertEqual(test_algorithm_train.id, 2060)
        self.assertIsInstance(
            test_algorithm_train.train_path_nodes[0],
            aidm_train_path_node_classes.AlgorithmTrainPathNode)
        self.assertEqual(test_algorithm_train.train_path_nodes[0].id, 1332)

    @mock.patch('requests.Session', side_effect=GetAlgorithmTrainParameterTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
