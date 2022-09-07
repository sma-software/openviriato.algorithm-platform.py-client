import unittest
from unittest import mock

import py_client.aidm.aidm_algorithm_classes
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestGetOrCreateFormation(unittest.TestCase):
    class GetOrCreateFormationTestSessionMock(SessionMockTestBase):
        def put(self, request, json):
            self._last_request = request
            self._last_body = json

            json__string = (
                "{\n"
                '        "id": 4108,\n'
                '        "vehicleTypeIds": [\n'
                "             688,\n"
                "             688,\n"
                "             688,\n"
                "             688\n"
                "        ],\n"
                '        "placesFirstClass": 125,\n'
                '        "placesSecondClass": 326,\n'
                '        "debugString": "formation generated by user, vehicles: 688, 688, 688, 688"'
                "}"
            )
            return APISessionMock.create_response_mock(json__string, 200)

    @mock.patch("requests.Session", side_effect=GetOrCreateFormationTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetOrCreateFormationTestSessionMock)
    def test_get_or_create_formation_request(self, mocked_get_obj):
        vehicle_type_ids = [688, 688, 688, 688]

        self.interface_to_viriato.get_or_create_formation(vehicle_type_ids=vehicle_type_ids)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + "/vehicles/formations")
        self.assertDictEqual(session_obj.last_body, {"vehicleTypeIDs": [688, 688, 688, 688]})

    @mock.patch("requests.Session", side_effect=GetOrCreateFormationTestSessionMock)
    def test_get_or_create_formation_response(self, mocked_get_obj):
        vehicle_type_ids = [688, 688, 688, 688]

        generated_formation = self.interface_to_viriato.get_or_create_formation(vehicle_type_ids)

        self.assertIsInstance(generated_formation, py_client.aidm.aidm_algorithm_classes.AlgorithmFormation)
        self.assertEqual(generated_formation.debug_string, "formation generated by user, vehicles: 688, 688, 688, 688")
        self.assertEqual(generated_formation.id, 4108)
        self.assertIsInstance(generated_formation.vehicle_type_ids[0], int)
        self.assertEqual(generated_formation.vehicle_type_ids, [688, 688, 688, 688])
        self.assertEqual(generated_formation.places_first_class, 125)
        self.assertEqual(generated_formation.places_second_class, 326)

    @mock.patch("requests.Session", side_effect=GetOrCreateFormationTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == "__main__":
    unittest.main()
