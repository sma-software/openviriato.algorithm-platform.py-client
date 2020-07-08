import unittest
from unittest import mock

import py_client.aidm.aidm_algorithm_classes
import algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.algorithm_interface import algorithm_interface_factory
from algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, SessionMockTestBase


class TestGetAssignableStationTracksOnTrainPathNode(unittest.TestCase):
    class GetAssignableStationTracksOnTrainPathNodeTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            json__string = ("[\n"
                            "  {\n"
                            "    \"ID\": 163,\n"
                            "    \"Code\": \"2\",\n"
                            "    \"DebugString\": \"stationtrack:85AR_{StationTrack SID = 34140}\"\n"
                            "  }\n"
                            "]")

            return APISessionMock.create_response_mock(json__string, 200)

    @mock.patch('requests.Session', side_effect=GetAssignableStationTracksOnTrainPathNodeTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetAssignableStationTracksOnTrainPathNodeTestSessionMock)
    def test_get_assignable_station_tracks_on_train_path_node_request(self, mocked_get_obj):
        train_path_node_id = 1

        self.interface_to_viriato.get_assignable_station_tracks_on_train_path_node(trainPathNodeId=train_path_node_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetAssignableStationTracksOnTrainPathNodeTestSessionMock__last_request,
                         get_api_url() + '/assignable-station-tracks-on-train-path-node')
        self.assertDictEqual(session_obj._GetAssignableStationTracksOnTrainPathNodeTestSessionMock__last_body,
                             dict(TrainPathNodeID=1))

    @mock.patch('requests.Session', side_effect=GetAssignableStationTracksOnTrainPathNodeTestSessionMock)
    def test_get_assignable_station_tracks_on_train_path_node_response(self, mocked_get_obj):
        train_path_node_id = 1

        test_list = self.interface_to_viriato.get_assignable_station_tracks_on_train_path_node(trainPathNodeId=
                                                                                               train_path_node_id)

        self.assertIsInstance(test_list, list)
        self.assertIsInstance(test_list[0], py_client.aidm.aidm_algorithm_classes.AlgorithmNodeTrack)
        self.assertEqual(test_list[0].debug_string, "stationtrack:85AR_{StationTrack SID = 34140}")

    @mock.patch('requests.Session', side_effect=GetAssignableStationTracksOnTrainPathNodeTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
