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
                            "  \"ID\": 6430,\n"
                            "  \"TrainPathNodes\": [\n"
                            "    {\n"
                            "      \"ID\": 5338,\n"
                            "      \"SectionTrackID\": null,\n"
                            "      \"node_id\": 321,\n"
                            "      \"node_track_id\": 322,\n"
                            "      \"FormationID\": 4108,\n"
                            "      \"ArrivalTime\": \"2003-05-01T06:00:00\",\n"
                            "      \"DepartureTime\": \"2003-05-01T06:00:00\",\n"
                            "      \"MinimumRunTime\": null,\n"
                            "      \"MinimumStopTime\": \"P0D\",\n"
                            "      \"StopStatus\": \"commercialStop\",\n"
                            "      \"SequenceNumber\": 0\n"
                            "    },\n"
                            "    {\n"
                            "      \"ID\": 5702,\n"
                            "      \"SectionTrackID\": 888,\n"
                            "      \"node_id\": 281,\n"
                            "      \"node_track_id\": null,\n"
                            "      \"FormationID\": 4108,\n"
                            "      \"ArrivalTime\": \"2003-05-01T06:02:42\",\n"
                            "      \"DepartureTime\": \"2003-05-01T06:02:42\",\n"
                            "      \"MinimumRunTime\": \"PT2M42S\",\n"
                            "      \"MinimumStopTime\": \"P0D\",\n"
                            "      \"StopStatus\": \"passing\",\n"
                            "      \"SequenceNumber\": 1\n"
                            "    },\n"
                            "    {\n"
                            "      \"ID\": 6066,\n"
                            "      \"SectionTrackID\": 887,\n"
                            "      \"node_id\": 161,\n"
                            "      \"node_track_id\": 162,\n"
                            "      \"FormationID\": null,\n"
                            "      \"ArrivalTime\": \"2003-05-01T06:03:54\",\n"
                            "      \"DepartureTime\": \"2003-05-01T06:03:54\",\n"
                            "      \"MinimumRunTime\": \"PT1M12S\",\n"
                            "      \"MinimumStopTime\": \"P0D\",\n"
                            "      \"StopStatus\": \"commercialStop\",\n"
                            "      \"SequenceNumber\": 2\n"
                            "    }\n"
                            "  ],\n"
                            "  \"DebugString\": \"FV_9_J03 tt_(SZ)\"\n"
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
        self.assertDictEqual(session_obj._SetStationTracksNodeTestSessionMock__last_body, dict(TrainPathNodeID=50,
                                                                                               NodeTrackID="162"))

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
