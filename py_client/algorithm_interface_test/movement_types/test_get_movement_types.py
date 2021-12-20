import unittest
from unittest import mock

from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
from py_client.algorithm_interface import algorithm_interface_factory
import py_client.algorithm_interface_test.test_helper.SessionMockFactory as SessionMockFactory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase
from py_client.aidm import AlgorithmMovementType

class TestMovementTypes(unittest.TestCase):
    class MovementTypes(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request

            json_string = ( "[{ \n"
                            "   \"id\": 1220, \n"
                            "   \"name\": \"empty\", \n"
                            "   \"description\": \"Empty Run\", \n"
                            "   \"isEmptyTrain\": true \n"
                            "}, \n"
                            "{ \n"
                            "   \"id\": 1221, \n"
                            "   \"name\": \"extra\", \n"
                            "   \"description\": \"Extra Train Run\", \n"
                            "   \"isEmptyTrain\": false \n"
                            "}]")

            return SessionMockFactory.create_response_mock(json_string, 200)

        interface_to_viriato: AlgorithmInterface

    @mock.patch('requests.Session', side_effect=MovementTypes)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=MovementTypes)
    def test_get_movement_types(self, mocked_get_obj):
        self.interface_to_viriato.get_movement_types()

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession

        self.assertEqual(session_obj._MovementTypes__last_request,
                         get_api_url() + "/movement-types")

        self.assertDictEqual(session_obj._MovementTypes__last_body,
                             dict())


    @mock.patch('requests.Session', side_effect=MovementTypes)
    def test_get_movement_types_response(self, mocked_get_obj):
        list_of_movement_types = self.interface_to_viriato.get_movement_types()

        self.assertIsInstance(
            list_of_movement_types,
            list)
        self.assertIsInstance(
            list_of_movement_types[0],
            AlgorithmMovementType)
        self.assertIsInstance(
            list_of_movement_types[0].id,
            int)
        self.assertEqual(
            list_of_movement_types[0].id,
            1220
            )
        self.assertIsInstance(
            list_of_movement_types[0].description,
            str
        )
        self.assertEqual(
            list_of_movement_types[0].description,
            "Empty Run"
        )
        self.assertIsInstance(
            list_of_movement_types[0].is_empty_train,
            bool
        )
        self.assertEqual(
            list_of_movement_types[0].is_empty_train,
            True
        )
        self.assertIsInstance(
            list_of_movement_types[0].name,
            str
        )
        self.assertEqual(
            list_of_movement_types[0].name,
            "empty"
        )
        self.assertIsInstance(
            list_of_movement_types[1],
            AlgorithmMovementType)
        self.assertIsInstance(
            list_of_movement_types[1].id,
            int)
        self.assertEqual(
            list_of_movement_types[1].id,
            1221
        )
        self.assertIsInstance(
            list_of_movement_types[1].description,
            str
        )
        self.assertEqual(
            list_of_movement_types[1].description,
            "Extra Train Run"
        )
        self.assertIsInstance(
            list_of_movement_types[1].is_empty_train,
            bool
        )
        self.assertEqual(
            list_of_movement_types[1].is_empty_train,
            False
        )
        self.assertIsInstance(
            list_of_movement_types[1].name,
            str
        )
        self.assertEqual(
            list_of_movement_types[1].name,
            "extra"
        )

    @mock.patch('requests.Session', side_effect=MovementTypes)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)

class TestMovementTypesEmpty(unittest.TestCase):
    class MovementTypesEmpty(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request

            json_string = "[]"

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface

    @mock.patch('requests.Session', side_effect=MovementTypesEmpty)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=MovementTypesEmpty)
    def test_get_movement_types_response_empty(self, mocked_get_obj):
        list_of_movement_types = self.interface_to_viriato.get_movement_types()

        self.assertIsInstance(
            list_of_movement_types,
            list)

        self.assertEqual(list_of_movement_types.__len__(), 0)

    @mock.patch('requests.Session', side_effect=MovementTypesEmpty)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)