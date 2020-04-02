import unittest
from unittest import mock

import AIDMClasses.AIDM_Algorithm_classes
import AlgorithmInterface_test.test_helper.SessionMockFactory as APISessionMock
from AIDMClasses import AIDM_TrainPathNode_classes, AIDM_enum_classes
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import \
    get_api_url, SessionMockTestBase


class TestGetAssignableStationTracksInAlgorithmNode(unittest.TestCase):
    class GetAssignableStationTracksInAlgorithmNodeTestSessionMock(SessionMockTestBase):
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

    @mock.patch('requests.Session', side_effect=GetAssignableStationTracksInAlgorithmNodeTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetAssignableStationTracksInAlgorithmNodeTestSessionMock)
    def test_get_assignable_station_tracks_in_algorithm_node_request(self, mocked_get_obj):
        node_id = 1
        train_path_node_id = 1
        test_stop_status = AIDM_enum_classes.StopStatus['commercialStop']

        self.interface_to_viriato.get_assignable_station_tracks_in_algorithm_node(nodeID=node_id,
                                                                                  trainPathNodeId=train_path_node_id,
                                                                                  stopStatus=test_stop_status)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetAssignableStationTracksInAlgorithmNodeTestSessionMock__last_request,
                         get_api_url() + '/assignable-station-tracks-in-algorithm-node')
        self.assertDictEqual(session_obj._GetAssignableStationTracksInAlgorithmNodeTestSessionMock__last_body,
                             dict(NodeID=1, TrainPathNodeID=1, StopStatus="commercialStop"))

    @mock.patch('requests.Session', side_effect=GetAssignableStationTracksInAlgorithmNodeTestSessionMock)
    def test_get_assignable_station_tracks_in_algorithm_node_response(self, mocked_get_obj):
        node_id = 1
        train_path_node_id = 1
        test_stop_status = AIDM_enum_classes.StopStatus['commercialStop']

        test_list = self.interface_to_viriato.get_assignable_station_tracks_in_algorithm_node(nodeID=node_id,
                                                                                              trainPathNodeId=train_path_node_id,
                                                                                              stopStatus=test_stop_status)

        self.assertIsInstance(test_list, list)
        self.assertIsInstance(test_list[0], AIDMClasses.AIDM_Algorithm_classes.AlgorithmNodeTrack)
        self.assertEqual(test_list[0].DebugString, "stationtrack:85AR_{StationTrack SID = 34140}")

    @mock.patch('requests.Session', side_effect=GetAssignableStationTracksInAlgorithmNodeTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
