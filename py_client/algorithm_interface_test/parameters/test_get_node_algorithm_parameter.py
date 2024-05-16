import unittest
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase
from py_client.aidm.aidm_algorithm_classes import AlgorithmNode
from py_client.aidm.aidm_algorithm_classes import AlgorithmNodeTrack


class TestGetNodeAlgorithmParameter(unittest.TestCase):
    class GetNodeAlgorithmParameterTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            json__string = (
                '{"value":{"id":644,"code":"85ZOER","nodeTracks":[{"id":645,"code":"6",'
                '"debugString":"stationtrack:85ZOER_{StationTrack SID = 206}"},{"id":646,'
                '"code":"5","debugString":"stationtrack:85ZOER_{StationTrack SID = 205}"},'
                '{"id":647,"code":"4","debugString":"stationtrack:85ZOER_{StationTrack SID = '
                '203}"},{"id":648,"code":"3","debugString":"stationtrack:85ZOER_{StationTrack '
                'SID = 202}"},{"id":649,"code":"2","debugString":"stationtrack:85ZOER_{'
                'StationTrack SID = 200}"},{"id":650,"code":"1",'
                '"debugString":"stationtrack:85ZOER_{StationTrack SID = 199}"}],'
                '"debugString":"station:85ZOER"},"key":"algorithmNode"}'
            )

            return APISessionMock.create_response_mock(json__string, 200)

    @mock.patch("requests.Session", side_effect=GetNodeAlgorithmParameterTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetNodeAlgorithmParameterTestSessionMock)
    def test_get_node_algorithm_parameter_request(self, mocked_get_obj):
        key = "someNodeParameterKey"

        self.interface_to_viriato.get_algorithm_node_parameter(key)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetNodeAlgorithmParameterTestSessionMock__last_request, get_api_url() + "/parameters/someNodeParameterKey")
        (self.assertDictEqual(session_obj._GetNodeAlgorithmParameterTestSessionMock__last_body, {}))

    @mock.patch("requests.Session", side_effect=GetNodeAlgorithmParameterTestSessionMock)
    def test_get_node_algorithm_parameter_response(self, mocked_get_obj):
        key = "someNodeParameterKey"

        node_param = self.interface_to_viriato.get_algorithm_node_parameter(key)

        self.assertIsInstance(node_param, AlgorithmNode)
        self.assertEqual(node_param.id, 644)
        self.assertEqual(node_param.code, "85ZOER")
        self.assertEqual(len(node_param.node_tracks), 6)
        self.assertIsInstance(node_param.node_tracks[0], AlgorithmNodeTrack)

    @mock.patch("requests.Session", side_effect=GetNodeAlgorithmParameterTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == "__main__":
    unittest.main()
