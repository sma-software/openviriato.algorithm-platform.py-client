import unittest
from unittest import mock

import AIDMClasses.AIDM_Algorithm_classes
import AlgorithmInterface_test.test_helper.SessionMockFactory as APISessionMock
from AIDMClasses import AIDM_classes
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import \
    get_api_url, SessionMockTestBase


class TestGetVehicleType(unittest.TestCase):
    class GetVehicleTypeTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            json__string = ("{\n"
                            "  \"ID\": 1828,\n"
                            "  \"DebugString\": \"vehicle isEngine: True, model: ICN, series: 1, velMax: 200\",\n"
                            "  \"IsEngine\": true\n"
                            "}")
            return APISessionMock.create_response_mock(json__string, 200)

    @mock.patch('requests.Session', side_effect=GetVehicleTypeTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetVehicleTypeTestSessionMock)
    def test_get_vehicle_type_request(self, mocked_get_obj):
        vehicle_type_id = 1828

        self.interface_to_viriato.get_vehicle_type(vehicle_type_id=vehicle_type_id)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetVehicleTypeTestSessionMock__last_request, get_api_url() +
                         "/vehicles/types/1828")
        self.assertDictEqual(session_obj._GetVehicleTypeTestSessionMock__last_body, {})

    @mock.patch('requests.Session', side_effect=GetVehicleTypeTestSessionMock)
    def test_get_vehicle_type_response(self, mocked_get_obj):
        vehicle_type_id = 1828

        test_algorithm_vehicle_type = self.interface_to_viriato.get_vehicle_type(vehicle_type_id)

        self.assertIsInstance(test_algorithm_vehicle_type, AIDMClasses.AIDM_Algorithm_classes.AlgorithmVehicleType)
        self.assertEqual(test_algorithm_vehicle_type.DebugString,
                         "vehicle isEngine: True, model: ICN, series: 1, velMax: 200")
        self.assertEqual(test_algorithm_vehicle_type.IsEngine, True)
        self.assertEqual(test_algorithm_vehicle_type.ID, 1828)

    @mock.patch('requests.Session', side_effect=GetVehicleTypeTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
