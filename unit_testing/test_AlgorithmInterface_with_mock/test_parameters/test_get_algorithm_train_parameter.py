import unittest
from unittest import mock

import unit_testing.test_AlgorithmInterface_with_mock.unit_testing_requisites.SessionMockFactory as APISessionMock
from AlgorithmInterface import AlgorithmInterfaceFactory
from unit_testing.test_AlgorithmInterface_with_mock.unit_testing_requisites.unit_testing_with_mock_helpers import \
    get_api_url, SessionMockTestBase
from AIDMClasses import AIDM_classes


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
                            "                \"NodeID\": 18,\n"
                            "                \"NodeTrackID\": null,\n"
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
                            "                \"NodeID\": 10,\n"
                            "                \"NodeTrackID\": null,\n"
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
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetAlgorithmTrainParameterTestSessionMock)
    def test_get_algorithm_train_parameter_request(self, mocked_get_obj):
        key = "somTestTrainParameterKey"

        self.interface_to_viriato.get_algorithm_train_parameter(key)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetAlgorithmTrainParameterTestSessionMock__last_request, get_api_url() +
                         '/parameters/somTestTrainParameterKey')
        self.assertDictEqual(session_obj._GetAlgorithmTrainParameterTestSessionMock__last_body, {})

    @mock.patch('requests.Session', side_effect=GetAlgorithmTrainParameterTestSessionMock)
    def test_get_algorithm_train_parameter_response(self, mocked_get_obj):
        key = "somTestTrainParameterKey"

        test_algorithm_train = self.interface_to_viriato.get_algorithm_train_parameter(key)

        self.assertIsInstance(test_algorithm_train, AIDM_classes.AlgorithmTrain)
        self.assertEqual(test_algorithm_train.DebugString, "RVZH_1_1_J03 tt_(G)")
        self.assertEqual(test_algorithm_train.ID, 2060)
        self.assertIsInstance(test_algorithm_train.TrainPathNodes[0], AIDM_classes.TrainPathNode)
        self.assertEqual(test_algorithm_train.TrainPathNodes[0].ID, 1332)

    @mock.patch('requests.Session', side_effect=GetAlgorithmTrainParameterTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()