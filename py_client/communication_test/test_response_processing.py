import unittest

import requests
import responses

from py_client.communication import response_processing


class TestResponseProcessing(unittest.TestCase):

    @responses.activate
    def test_extract_json_if_possible_to_raise_http_error(self):
        responses.add(**dict(
            method=responses.GET,
            url='http://notanurl/',
            status=404
        ))

        response = requests.get('http://notanurl/')

        with self.assertRaises(requests.HTTPError) as http_error:
            response_processing.extract_json_if_possible(response)

        self.assertIsInstance(http_error.exception, requests.exceptions.HTTPError)
        self.assertEqual(http_error.exception.response.status_code, 404)
        self.assertEqual(http_error.exception.response.reason, "Not Found")

    @responses.activate
    def test_extract_json_if_possible_to_raise_algorithm_platform_error(self):
        responses.add(**dict(
            method=responses.GET,
            url='http://notanurl/',
            body='{"statusCode": "404", "message": "test_reason_to_raise_AlgorithmPlatformError"}',
            status=400
        ))

        response = requests.get('http://notanurl/')
        with self.assertRaises(response_processing.AlgorithmPlatformHTTPError) as algorithm_platform_error:
            response_processing.extract_json_if_possible(response)

        self.assertIsInstance(algorithm_platform_error.exception, response_processing.AlgorithmPlatformHTTPError)
        self.assertEqual(algorithm_platform_error.exception.message, "test_reason_to_raise_AlgorithmPlatformError")

    @responses.activate
    def test_extract_json_if_possible_to_return_json(self):
        responses.add(**dict(
            method=responses.GET,
            url='http://notanurl/',
            body='{"key" : "Value"}',
            status=200
        ))

        response = requests.get('http://notanurl/')
        processed_response = response_processing.extract_json_if_possible(response)

        self.assertIsInstance(processed_response, dict)
        self.assertDictEqual(processed_response, dict(key="Value"))

    @responses.activate
    def test_extract_json_if_possible_to_return_none(self):
        responses.add(**dict(
            method=responses.GET,
            url='http://notanurl/',
            body='',
            status=200
        ))

        response = requests.get('http://notanurl/')
        processed_response = response_processing.extract_json_if_possible(response)

        self.assertIsNone(processed_response)
