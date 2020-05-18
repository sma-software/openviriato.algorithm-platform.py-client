import unittest
from unittest import mock

import AIDMClasses.AIDM_Algorithm_classes
import AlgorithmInterface_test.test_helper.SessionMockFactory as APISessionMock
from AIDMClasses import AIDM_TrainPathNode_classes
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import \
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
                            "      \"NodeID\": 321,\n"
                            "      \"NodeTrackID\": 322,\n"
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
                            "      \"NodeID\": 281,\n"
                            "      \"NodeTrackID\": null,\n"
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
                            "      \"NodeID\": 161,\n"
                            "      \"NodeTrackID\": 162,\n"
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
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=SetStationTracksNodeTestSessionMock)
    def test_assign_station_track_request(self, mocked_get_obj):
        train_path_node_id = 50
        station_track_id = "162"

        self.interface_to_viriato.assign_station_track(trainPathNodeId=train_path_node_id,
                                                       stationTrackIDOrNone=station_track_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._SetStationTracksNodeTestSessionMock__last_request,
                         get_api_url() + '/assign-station-track')
        self.assertDictEqual(session_obj._SetStationTracksNodeTestSessionMock__last_body, dict(TrainPathNodeID=50,
                                                                                               NodeTrackID="162"))

    @mock.patch('requests.Session', side_effect=SetStationTracksNodeTestSessionMock)
    def test_assign_station_track_response(self, mocked_get_obj):
        train_path_node_id = 1

        test_train = self.interface_to_viriato.assign_station_track(trainPathNodeId=train_path_node_id)

        self.assertIsInstance(test_train, AIDMClasses.AIDM_Algorithm_classes.AlgorithmTrain)
        self.assertIsInstance(test_train.TrainPathNodes[0], AIDM_TrainPathNode_classes.TrainPathNode)
        self.assertEqual(test_train.DebugString, "FV_9_J03 tt_(SZ)")

    @mock.patch('requests.Session', side_effect=SetStationTracksNodeTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
