import unittest
from unittest import mock

import unit_testing.test_AlgorithmInterface_with_mock.unit_testing_requisites.SessionMockFactory as APISessionMock
from AlgorithmInterface import AlgorithmInterfaceFactory
from unit_testing.test_AlgorithmInterface_with_mock.unit_testing_requisites.unit_testing_with_mock_helpers import \
    get_api_url, SessionMockTestBase
from AIDMClasses import AIDM_classes, AIDM_enum_classes


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
        NodeID = 1
        TrainPathNodeID = 1
        TestStopStatus = AIDM_enum_classes.StopStatus['commercialStop']

        self.interface_to_viriato.get_assignable_station_tracks_in_algorithm_node(nodeID=NodeID,
                                                                                  trainPathNodeId=TrainPathNodeID,
                                                                                  stopStatus=TestStopStatus)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetAssignableStationTracksInAlgorithmNodeTestSessionMock__last_request,
                         get_api_url() + '/parameters/somTestTrainParameterKey')
        self.assertDictEqual(session_obj._GetAssignableStationTracksInAlgorithmNodeTestSessionMock__last_body, {})

    @mock.patch('requests.Session', side_effect=GetAssignableStationTracksInAlgorithmNodeTestSessionMock)
    def test_get_assignable_station_tracks_in_algorithm_node_response(self, mocked_get_obj):
        key = "somTestTrainParameterKey"

        test_algorithm_train = self.interface_to_viriato.get_assignable_station_tracks_in_algorithm_node(key)

        self.assertIsInstance(test_algorithm_train, AIDM_classes.AlgorithmTrain)
        self.assertEqual(test_algorithm_train.DebugString, "RVZH_1_1_J03 tt_(G)")
        self.assertEqual(test_algorithm_train.ID, 2060)
        self.assertIsInstance(test_algorithm_train.TrainPathNodes[0], AIDM_classes.TrainPathNode)
        self.assertEqual(test_algorithm_train.TrainPathNodes[0].ID, 1332)

    @mock.patch('requests.Session', side_effect=GetAssignableStationTracksInAlgorithmNodeTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
