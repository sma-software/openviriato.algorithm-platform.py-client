import unittest
from unittest import mock

import py_client.aidm.aidm_algorithm_classes
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.aidm import aidm_train_path_node_classes
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetAlgorithmTrainsParameter(unittest.TestCase):
    class GetAlgorithmTrainsParameterTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            json__string = (
                "{\n"
                '  "key": "templateTrainsFromScenarioParameter",\n'
                '  "value": [\n'
                "    {\n"
                '      "id": 1190,\n'
                '      "code": "FirstTemplateTrain",\n'
                '      "trainPathNodes": [\n'
                "        {\n"
                '          "id": 1186,\n'
                '          "sectionTrackID": null,\n'
                '          "nodeId": 526,\n'
                '          "nodeTrackId": null,\n'
                '          "formationId": 1187,\n'
                '          "movementTypeId": null,\n'
                '          "arrivalTime": "2005-05-01T04:00:00",\n'
                '          "departureTime": "2005-05-01T04:00:00",\n'
                '          "minimumRunTime": null,\n'
                '          "minimumStopTime": "P0D",\n'
                '          "stopStatus": "commercialStop",\n'
                '          "sequenceNumber": 0\n'
                "        },\n"
                "        {\n"
                '          "id": 1188,\n'
                '          "sectionTrackID": 688,\n'
                '          "nodeId": 351,\n'
                '          "nodeTrackId": null,\n'
                '          "formationId": 1187,\n'
                '          "movementTypeId": null,\n'
                '          "arrivalTime": "2005-05-01T04:04:00",\n'
                '          "departureTime": "2005-05-01T04:04:00",\n'
                '          "minimumRunTime": "PT4M",\n'
                '          "minimumStopTime": "P0D",\n'
                '          "stopStatus": "passing",\n'
                '          "sequenceNumber": 1\n'
                "        },\n"
                "        {\n"
                '          "id": 1189,\n'
                '          "sectionTrackId": 690,\n'
                '          "nodeId": 296,\n'
                '          "nodeTrackId": null,\n'
                '          "FormationId": null,\n'
                '          "movementTypeId": null,\n'
                '          "arrivalTime": "2005-05-01T04:07:00",\n'
                '          "departureTime": "2005-05-01T04:07:00",\n'
                '          "minimumRunTime": "PT3M",\n'
                '          "minimumStopTime": "P0D",\n'
                '          "stopStatus": "commercialStop",\n'
                '          "sequenceNumber": 2\n'
                "        }\n"
                "      ],\n"
                '      "debugString": "GV_9_J05 tt_()"\n'
                "    },\n"
                "    {\n"
                '      "id": 1194,\n'
                '      "code": "SecondTemplateTrain",\n'
                '      "trainPathNodes": [\n'
                "        {\n"
                '          "id": 1191,\n'
                '          "sectionTrackId": null,\n'
                '          "nodeId": 296,\n'
                '          "nodeTrackId": null,\n'
                '          "formationID": 1187,\n'
                '          "movementTypeId": null,\n'
                '          "arrivalTime": "2005-05-01T05:00:00",\n'
                '          "departureTime": "2005-05-01T05:00:00",\n'
                '          "minimumRunTime": null,\n'
                '          "minimumStopTime": "P0D",\n'
                '          "stopStatus": "commercialStop",\n'
                '          "sequenceNumber": 0\n'
                "        },\n"
                "        {\n"
                '          "id": 1192,\n'
                '          "sectionTrackID": 691,\n'
                '          "nodeId": 351,\n'
                '          "nodeTrackId": null,\n'
                '          "formationId": 1187,\n'
                '          "movementTypeId": null,\n'
                '          "arrivalTime": "2005-05-01T05:07:00",\n'
                '          "departureTime": "2005-05-01T05:07:00",\n'
                '          "minimumRunTime": "PT3M",\n'
                '          "minimumStopTime": "P0D",\n'
                '          "stopStatus": "passing",\n'
                '          "sequenceNumber": 1\n'
                "        },\n"
                "        {\n"
                '          "id": 1193,\n'
                '          "sectionTrackID": 689,\n'
                '          "nodeId": 526,\n'
                '          "nodeTrackId": null,\n'
                '          "formationID": null,\n'
                '          "movementTypeId": null,\n'
                '          "arrivalTime": "2005-05-01T05:11:00",\n'
                '          "departureTime": "2005-05-01T05:11:00",\n'
                '          "minimumRunTime": "PT4M",\n'
                '          "minimumStopTime": "P0D",\n'
                '          "stopStatus": "commercialStop",\n'
                '          "sequenceNumber": 2\n'
                "        }\n"
                "      ],\n"
                '      "debugString": "GV_10_J05 tt_()"\n'
                "    }\n"
                "  ]\n"
                "}"
            )

            return APISessionMock.create_response_mock(json__string, 200)

    @mock.patch("requests.Session", side_effect=GetAlgorithmTrainsParameterTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetAlgorithmTrainsParameterTestSessionMock)
    def test_get_algorithm_trains_parameter_request(self, mocked_get_obj):
        key = "somTestTrainsParameterKey"

        self.interface_to_viriato.get_algorithm_trains_parameter(key)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetAlgorithmTrainsParameterTestSessionMock__last_request, get_api_url() + "/parameters/somTestTrainsParameterKey")
        self.assertDictEqual(session_obj._GetAlgorithmTrainsParameterTestSessionMock__last_body, {})

    @mock.patch("requests.Session", side_effect=GetAlgorithmTrainsParameterTestSessionMock)
    def test_get_algorithm_trains_parameter_response(self, mocked_get_obj):
        key = "somTestTrainsParameterKey"

        test_algorithm_trains = self.interface_to_viriato.get_algorithm_trains_parameter(key)

        self.assertIsInstance(test_algorithm_trains, list)
        self.assertIsInstance(test_algorithm_trains[0], py_client.aidm.aidm_algorithm_classes.AlgorithmTrain)
        self.assertEqual(test_algorithm_trains[0].debug_string, "GV_9_J05 tt_()")
        self.assertEqual(test_algorithm_trains[0].code, "FirstTemplateTrain")
        self.assertEqual(test_algorithm_trains[0].id, 1190)
        self.assertIsInstance(test_algorithm_trains[0].train_path_nodes[0], aidm_train_path_node_classes.AlgorithmTrainPathNode)
        self.assertEqual(test_algorithm_trains[0].train_path_nodes[0].id, 1186)
        self.assertEqual(test_algorithm_trains[1].code, "SecondTemplateTrain")

    @mock.patch("requests.Session", side_effect=GetAlgorithmTrainsParameterTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == "__main__":
    unittest.main()
