import unittest
from unittest import mock

import AlgorithmInterface_test.test_helper.SessionMockFactory as APISessionMock
from AIDMClasses import AIDM_classes
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import \
    get_api_url, SessionMockTestBase


class TestGetFormation(unittest.TestCase):
    class GetGetFormationTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            json__string = ("{\n"
                            "  \"ID\": 1828,\n"
                            "  \"VehicleTypeIDs\": [\n"
                            "    4107\n"
                            "  ],\n"
                            "  \"DebugString\": \"train configuration: \"\n"
                            "}")
            return APISessionMock.create_response_mock(json__string, 200)

    @mock.patch('requests.Session', side_effect=GetGetFormationTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetGetFormationTestSessionMock)
    def test_get_formation_request(self, mocked_get_obj):
        formation_id=1828

        self.interface_to_viriato.get_formation(formation_id=formation_id)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetGetFormationTestSessionMock__last_request, get_api_url() +
                         "/vehicles/formations/1828")
        self.assertDictEqual(session_obj._GetGetFormationTestSessionMock__last_body, {})

    @mock.patch('requests.Session', side_effect=GetGetFormationTestSessionMock)
    def test_get_formation_response(self, mocked_get_obj):
        key = 1828

        test_algorithm_formation = self.interface_to_viriato.get_formation(key)

        self.assertIsInstance(test_algorithm_formation, AIDM_classes.AlgorithmFormation)
        self.assertEqual(test_algorithm_formation.DebugString, "train configuration: ")
        self.assertEqual(test_algorithm_formation.ID, 1828)
        self.assertIsInstance(test_algorithm_formation.VehicleTypeIDs[0], int)
        self.assertEqual(test_algorithm_formation.VehicleTypeIDs[0], 4107)

    @mock.patch('requests.Session', side_effect=GetGetFormationTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
