import unittest
from unittest import mock

import py_client.aidm.aidm_algorithm_classes
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.aidm import aidm_train_path_node_classes
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, SessionMockTestBase


class TestGetAlgorithmTrainParameter(unittest.TestCase):
    class GetAlgorithmTrainParameterTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            json__string = ("{\n"
                            "   \"key\": \"templateTrainParameter\",\n"
                            "   \"value\": {\n"
                            "       \"id\": 2060,\n"
                            "       \"code\": \"templateTrain\",\n" 
                            "       \"trainPathNodes\": [\n"
                            "           {\n"
                            "                \"id\": 1332,\n"
                            "                \"sectionTrackId\": null,\n"
                            "                \"nodeId\": 18,\n"
                            "                \"nodeTrackId\": null,\n"
                            "                \"FormationId\": 1187,\n"
                            "                \"movementTypeId\": null,\n"
                            "                \"arrivalTime\": \"2003-05-01T00:04:00\",\n"
                            "                \"departureTime\": \"2003-05-01T00:05:30\",\n"
                            "                \"minimumRunTime\": null,\n"
                            "                \"minimumStopTime\": \"P0D\",\n"
                            "                \"stopStatus\": \"operationalStop\",\n"
                            "                \"sequenceNumber\": 0\n"
                            "           },\n"
                            "           {\n"
                            "                \"id\": 1696,\n"
                            "                \"sectionTrackId\": 1172,\n"
                            "                \"nodeId\": 10,\n"
                            "                \"nodeTrackId\": null,\n"
                            "                \"formationId\": null,\n"
                            "                \"movementTypeId\": null,\n"
                            "                \"arrivalTime\": \"2003-05-01T00:10:30\",\n"
                            "                \"departureTime\": \"2003-05-01T00:10:30\",\n"
                            "                \"minimumRunTime\": \"PT5M\",\n"
                            "                \"minimumStopTime\": \"P0D\",\n"
                            "                \"stopStatus\": \"commercialStop\",\n"
                            "                \"sequenceNumber\": 1\n"
                            "           }\n"
                            "       ],\n"
                            "       \"debugString\": \"RVZH_1_1_J03 tt_(G)\"\n"
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
        self.assertEqual(test_algorithm_train.code, "templateTrain")
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
