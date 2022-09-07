import unittest
from enum import Enum
from unittest import mock

import py_client.algorithm_interface_test.test_helper.SessionMockFactory as APISessionMock
from py_client.algorithm_interface import algorithm_interface_factory
from py_client.algorithm_interface_test.test_helper.SessionMockTestBase import get_api_url, SessionMockTestBase


class TestRequestEnum(Enum):
    optionValue1 = "optionValue1"
    optionValue2 = "optionValue2"
    optionValue3 = "optionValue3"


class TestGetEnumPointAlgorithmParameter(unittest.TestCase):
    class GetEnumAlgorithmParameterTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self._last_request = request
            self._last_body = params

            if "noneEnumParameter" in self._last_request:
                json__string = "{\n" '  "value": null,\n' '  "key": "noneEnumParameter"\n' "}"
            else:
                json__string = "{\n" '  "value": "optionValue3",\n' '  "key": "enumParameter"\n' "}"

            return APISessionMock.create_response_mock(json__string, 200)

    @mock.patch("requests.Session", side_effect=GetEnumAlgorithmParameterTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = algorithm_interface_factory.create(get_api_url())

    @mock.patch("requests.Session", side_effect=GetEnumAlgorithmParameterTestSessionMock)
    def test_get_enum_algorithm_parameter_request(self, mocked_get_obj):
        key = "enumParameter"

        self.interface_to_viriato.get_enum_algorithm_parameter(TestRequestEnum, key)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj.last_request, get_api_url() + "/parameters/enumParameter")
        self.assertDictEqual(session_obj.last_body, {})

    @mock.patch("requests.Session", side_effect=GetEnumAlgorithmParameterTestSessionMock)
    def test_get_enum_algorithm_parameter_response_with_value(self, mocked_get_obj):
        key = "enumParameter"

        value_with_populated_enum = self.interface_to_viriato.get_enum_algorithm_parameter(TestRequestEnum, key)

        self.assertIsInstance(value_with_populated_enum, TestRequestEnum)
        self.assertEqual(value_with_populated_enum, TestRequestEnum.optionValue3)

    @mock.patch("requests.Session", side_effect=GetEnumAlgorithmParameterTestSessionMock)
    def test_get_enum_algorithm_parameter_response_with_none(self, mocked_get_obj):
        key = "noneEnumParameter"

        value_with_none = self.interface_to_viriato.get_enum_algorithm_parameter(TestRequestEnum, key)

        self.assertEqual(value_with_none, None)

    @mock.patch("requests.Session", side_effect=GetEnumAlgorithmParameterTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == "__main__":
    unittest.main()
