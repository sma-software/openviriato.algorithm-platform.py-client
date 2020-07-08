import unittest
from unittest import mock

import aidm.aidm_algorithm_classes
import algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from algorithm_interface import algorithm_interface_factory
from algorithm_interface_test.test_helper.SessionMockTestBase import \
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
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetVehicleTypeTestSessionMock)
    def test_get_vehicle_type_request(self, mocked_get_obj):
        vehicle_type_id = 1828

        self.interface_to_viriato.get_vehicle_type(vehicle_type_id=vehicle_type_id)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetVehicleTypeTestSessionMock__last_request, get_api_url() +
                         "/vehicles/types/1828")
        self.assertDictEqual(session_obj._GetVehicleTypeTestSessionMock__last_body, {})

    @mock.patch('requests.Session', side_effect=GetVehicleTypeTestSessionMock)
    def test_get_vehicle_type_response(self, mocked_get_obj):
        vehicle_type_id = 1828

        test_algorithm_vehicle_type = self.interface_to_viriato.get_vehicle_type(vehicle_type_id)

        self.assertIsInstance(test_algorithm_vehicle_type, aidm.aidm_algorithm_classes.AlgorithmVehicleType)
        self.assertEqual(test_algorithm_vehicle_type.debug_string,
                         "vehicle isEngine: True, model: ICN, series: 1, velMax: 200")
        self.assertEqual(test_algorithm_vehicle_type.is_engine, True)
        self.assertEqual(test_algorithm_vehicle_type.id, 1828)

    @mock.patch('requests.Session', side_effect=GetVehicleTypeTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
