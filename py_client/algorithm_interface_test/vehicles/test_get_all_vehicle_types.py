import unittest
from unittest import mock

import py_client.aidm.aidm_algorithm_classes
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import \
    get_api_url, SessionMockTestBase


class TestGetAllVehicleTypes(unittest.TestCase):
    class GetAllVehicleTypesTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self._last_body = params
            self._last_request = request

            json_string = (
                "[\n"
                "  {\n"
                "    \"id\": 686,\n"
                "    \"debugString\": \"vehicle isEngine: True, model: 401, series: 301, velMax: 280, seats: 144 681\",\n"
                "    \"isEngine\": true,\n"
                "    \"placesFirstClass\": 144,\n"
                "    \"placesSecondClass\": 681\n"
                "  },\n"
                "  {\n"
                "    \"id\": 687,\n"
                "    \"debugString\": \"vehicle isEngine: True, model: ETR470, series: 0, velMax: 200, seats: 156 324\",\n"
                "    \"isEngine\": true,\n"
                "    \"placesFirstClass\": 156,\n"
                "    \"placesSecondClass\": 324\n"
                "  },\n"
                "  {\n"
                "    \"id\": 688,\n"
                "    \"debugString\": \"vehicle isEngine: True, model: ICN, series: 1, velMax: 200, seats: 125 326\",\n"
                "    \"isEngine\": true,\n"
                "    \"placesFirstClass\": 125,\n"
                "    \"placesSecondClass\": 326\n"
                "  }\n"
                "]")
            return APISessionMock.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetAllVehicleTypesTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetAllVehicleTypesTestSessionMock)
    def test_get_vehicle_type_request(self, mocked_get_obj):
        self.interface_to_viriato.get_all_vehicle_types()

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + "/vehicles/types")
        self.assertDictEqual(session_obj.last_body, {})

    @mock.patch('requests.Session', side_effect=GetAllVehicleTypesTestSessionMock)
    def test_get_vehicle_type_response(self, mocked_get_obj):
        test_algorithm_vehicle_types = self.interface_to_viriato.get_all_vehicle_types()

        self.assertIsInstance(test_algorithm_vehicle_types, list)
        self.assertEqual(len(test_algorithm_vehicle_types), 3)

        self.assertIsInstance(
            test_algorithm_vehicle_types[2],
            py_client.aidm.aidm_algorithm_classes.AlgorithmVehicleType)
        self.assertEqual(
            test_algorithm_vehicle_types[2].debug_string,
            "vehicle isEngine: True, model: ICN, series: 1, velMax: 200, seats: 125 326")
        self.assertEqual(test_algorithm_vehicle_types[2].is_engine, True)
        self.assertEqual(test_algorithm_vehicle_types[2].id, 688)
        self.assertEqual(test_algorithm_vehicle_types[2].places_first_class, 125)
        self.assertEqual(test_algorithm_vehicle_types[2].places_second_class, 326)

    @mock.patch('requests.Session', side_effect=GetAllVehicleTypesTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
