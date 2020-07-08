import unittest
from unittest import mock

import aidm.aidm_algorithm_classes
import algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from aidm import aidm_train_path_node_classes
from algorithm_interface import algorithm_interface_factory
from algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, SessionMockTestBase


class TestGetAlgorithmTrainsParameter(unittest.TestCase):
    class GetAlgorithmTrainsParameterTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            json__string = ("{\n"
                            "  \"Key\": \"templateTrainsFromScenarioParameter\",\n"
                            "  \"Value\": [\n"
                            "    {\n"
                            "      \"ID\": 1190,\n"
                            "      \"TrainPathNodes\": [\n"
                            "        {\n"
                            "          \"ID\": 1186,\n"
                            "          \"SectionTrackID\": null,\n"
                            "          \"node_id\": 526,\n"
                            "          \"node_track_id\": null,\n"
                            "          \"FormationID\": 1187,\n"
                            "          \"ArrivalTime\": \"2005-05-01T04:00:00\",\n"
                            "          \"DepartureTime\": \"2005-05-01T04:00:00\",\n"
                            "          \"MinimumRunTime\": null,\n"
                            "          \"MinimumStopTime\": \"P0D\",\n"
                            "          \"StopStatus\": \"commercialStop\",\n"
                            "          \"SequenceNumber\": 0\n"
                            "        },\n"
                            "        {\n"
                            "          \"ID\": 1188,\n"
                            "          \"SectionTrackID\": 688,\n"
                            "          \"node_id\": 351,\n"
                            "          \"node_track_id\": null,\n"
                            "          \"FormationID\": 1187,\n"
                            "          \"ArrivalTime\": \"2005-05-01T04:04:00\",\n"
                            "          \"DepartureTime\": \"2005-05-01T04:04:00\",\n"
                            "          \"MinimumRunTime\": \"PT4M\",\n"
                            "          \"MinimumStopTime\": \"P0D\",\n"
                            "          \"StopStatus\": \"passing\",\n"
                            "          \"SequenceNumber\": 1\n"
                            "        },\n"
                            "        {\n"
                            "          \"ID\": 1189,\n"
                            "          \"SectionTrackID\": 690,\n"
                            "          \"node_id\": 296,\n"
                            "          \"node_track_id\": null,\n"
                            "          \"FormationID\": null,\n"
                            "          \"ArrivalTime\": \"2005-05-01T04:07:00\",\n"
                            "          \"DepartureTime\": \"2005-05-01T04:07:00\",\n"
                            "          \"MinimumRunTime\": \"PT3M\",\n"
                            "          \"MinimumStopTime\": \"P0D\",\n"
                            "          \"StopStatus\": \"commercialStop\",\n"
                            "          \"SequenceNumber\": 2\n"
                            "        }\n"
                            "      ],\n"
                            "      \"DebugString\": \"GV_9_J05 tt_()\"\n"
                            "    },\n"
                            "    {\n"
                            "      \"ID\": 1194,\n"
                            "      \"TrainPathNodes\": [\n"
                            "        {\n"
                            "          \"ID\": 1191,\n"
                            "          \"SectionTrackID\": null,\n"
                            "          \"node_id\": 296,\n"
                            "          \"node_track_id\": null,\n"
                            "          \"FormationID\": 1187,\n"
                            "          \"ArrivalTime\": \"2005-05-01T05:00:00\",\n"
                            "          \"DepartureTime\": \"2005-05-01T05:00:00\",\n"
                            "          \"MinimumRunTime\": null,\n"
                            "          \"MinimumStopTime\": \"P0D\",\n"
                            "          \"StopStatus\": \"commercialStop\",\n"
                            "          \"SequenceNumber\": 0\n"
                            "        },\n"
                            "        {\n"
                            "          \"ID\": 1192,\n"
                            "          \"SectionTrackID\": 691,\n"
                            "          \"node_id\": 351,\n"
                            "          \"node_track_id\": null,\n"
                            "          \"FormationID\": 1187,\n"
                            "          \"ArrivalTime\": \"2005-05-01T05:07:00\",\n"
                            "          \"DepartureTime\": \"2005-05-01T05:07:00\",\n"
                            "          \"MinimumRunTime\": \"PT3M\",\n"
                            "          \"MinimumStopTime\": \"P0D\",\n"
                            "          \"StopStatus\": \"passing\",\n"
                            "          \"SequenceNumber\": 1\n"
                            "        },\n"
                            "        {\n"
                            "          \"ID\": 1193,\n"
                            "          \"SectionTrackID\": 689,\n"
                            "          \"node_id\": 526,\n"
                            "          \"node_track_id\": null,\n"
                            "          \"FormationID\": null,\n"
                            "          \"ArrivalTime\": \"2005-05-01T05:11:00\",\n"
                            "          \"DepartureTime\": \"2005-05-01T05:11:00\",\n"
                            "          \"MinimumRunTime\": \"PT4M\",\n"
                            "          \"MinimumStopTime\": \"P0D\",\n"
                            "          \"StopStatus\": \"commercialStop\",\n"
                            "          \"SequenceNumber\": 2\n"
                            "        }\n"
                            "      ],\n"
                            "      \"DebugString\": \"GV_10_J05 tt_()\"\n"
                            "    }\n"
                            "  ]\n"
                            "}")

            return APISessionMock.create_response_mock(json__string, 200)

    @mock.patch('requests.Session', side_effect=GetAlgorithmTrainsParameterTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetAlgorithmTrainsParameterTestSessionMock)
    def test_get_algorithm_trains_parameter_request(self, mocked_get_obj):
        key = "somTestTrainsParameterKey"

        self.interface_to_viriato.get_algorithm_trains_parameter(key)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetAlgorithmTrainsParameterTestSessionMock__last_request, get_api_url() +
                         '/parameters/somTestTrainsParameterKey')
        self.assertDictEqual(session_obj._GetAlgorithmTrainsParameterTestSessionMock__last_body, {})

    @mock.patch('requests.Session', side_effect=GetAlgorithmTrainsParameterTestSessionMock)
    def test_get_algorithm_trains_parameter_response(self, mocked_get_obj):
        key = "somTestTrainsParameterKey"

        test_algorithm_trains = self.interface_to_viriato.get_algorithm_trains_parameter(key)

        self.assertIsInstance(test_algorithm_trains, list)
        self.assertIsInstance(test_algorithm_trains[0], aidm.aidm_algorithm_classes.AlgorithmTrain)
        self.assertEqual(test_algorithm_trains[0].debug_string, "GV_9_J05 tt_()")
        self.assertEqual(test_algorithm_trains[0].id, 1190)
        self.assertIsInstance(
            test_algorithm_trains[0].train_path_nodes[0],
            aidm_train_path_node_classes.AlgorithmTrainPathNode)
        self.assertEqual(test_algorithm_trains[0].train_path_nodes[0].id, 1186)

    @mock.patch('requests.Session', side_effect=GetAlgorithmTrainsParameterTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
