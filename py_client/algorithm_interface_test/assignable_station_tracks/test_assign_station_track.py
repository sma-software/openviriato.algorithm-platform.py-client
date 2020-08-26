import unittest
from unittest import mock

import py_client.aidm.aidm_algorithm_classes
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.aidm import aidm_train_path_node_classes
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, SessionMockTestBase


class TestSetStationTracksNode(unittest.TestCase):
    class SetStationTracksNodeTestSessionMock(SessionMockTestBase):
        def post(self, request, json):
            self.__last_request = request
            self.__last_body = json

            json__string = ("{\n"
                            "  \"id\": 6430,\n"
                            "  \"trainPathNodes\": [\n"
                            "    {\n"
                            "      \"id\": 5338,\n"
                            "      \"SectionTrackId\": null,\n"
                            "      \"nodeId\": 321,\n"
                            "      \"nodeTrackId\": 322,\n"
                            "      \"formationId\": 4108,\n"
                            "      \"arrivalTime\": \"2003-05-01T06:00:00\",\n"
                            "      \"departureTime\": \"2003-05-01T06:00:00\",\n"
                            "      \"minimumRunTime\": null,\n"
                            "      \"minimumStopTime\": \"P0D\",\n"
                            "      \"stopStatus\": \"commercialStop\",\n"
                            "      \"sequenceNumber\": 0\n"
                            "    },\n"
                            "    {\n"
                            "      \"id\": 5702,\n"
                            "      \"sectionTrackId\": 888,\n"
                            "      \"nodeId\": 281,\n"
                            "      \"nodeTrackId\": null,\n"
                            "      \"formationID\": 4108,\n"
                            "      \"arrivalTime\": \"2003-05-01T06:02:42\",\n"
                            "      \"departureTime\": \"2003-05-01T06:02:42\",\n"
                            "      \"minimumRunTime\": \"PT2M42S\",\n"
                            "      \"minimumStopTime\": \"P0D\",\n"
                            "      \"stopStatus\": \"passing\",\n"
                            "      \"sequenceNumber\": 1\n"
                            "    },\n"
                            "    {\n"
                            "      \"id\": 6066,\n"
                            "      \"sectionTrackId\": 887,\n"
                            "      \"nodeId\": 161,\n"
                            "      \"nodeTrackId\": 162,\n"
                            "      \"formationId\": null,\n"
                            "      \"arrivalTime\": \"2003-05-01T06:03:54\",\n"
                            "      \"departureTime\": \"2003-05-01T06:03:54\",\n"
                            "      \"minimumRunTime\": \"PT1M12S\",\n"
                            "      \"minimumStopTime\": \"P0D\",\n"
                            "      \"stopStatus\": \"commercialStop\",\n"
                            "      \"sequenceNumber\": 2\n"
                            "    }\n"
                            "  ],\n"
                            "  \"debugString\": \"FV_9_J03 tt_(SZ)\"\n"
                            "}")

            return APISessionMock.create_response_mock(json__string, 200)

    @mock.patch('requests.Session', side_effect=SetStationTracksNodeTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=SetStationTracksNodeTestSessionMock)
    def test_assign_station_track_request(self, mocked_get_obj):
        train_path_node_id = 50
        station_track_id = 162

        self.interface_to_viriato.assign_station_track(train_path_node_id=train_path_node_id,
                                                       station_track_id_or_none=station_track_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._SetStationTracksNodeTestSessionMock__last_request,
                         get_api_url() + '/assign-station-track')
        self.assertDictEqual(
            session_obj._SetStationTracksNodeTestSessionMock__last_body,
            dict(trainPathNodeId=50, nodeTrackId="162"))

    @mock.patch('requests.Session', side_effect=SetStationTracksNodeTestSessionMock)
    def test_assign_station_track_response(self, mocked_get_obj):
        train_path_node_id = 1

        test_train = self.interface_to_viriato.assign_station_track(train_path_node_id=train_path_node_id)

        self.assertIsInstance(test_train, py_client.aidm.aidm_algorithm_classes.AlgorithmTrain)
        self.assertIsInstance(test_train.train_path_nodes[0], aidm_train_path_node_classes.AlgorithmTrainPathNode)
        self.assertEqual(test_train.debug_string, "FV_9_J03 tt_(SZ)")

    @mock.patch('requests.Session', side_effect=SetStationTracksNodeTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
