import unittest

import requests
import responses

from py_client.communication import communication_layer


class TestCommunicationLayerToRaiseHTTPError(unittest.TestCase):

    def setUp(self):
        base_url = "http://viriato.rest.ch/api"
        self.CommunicationLayer = communication_layer.CommunicationLayer(base_url=base_url)

    @responses.activate
    def test_do_get_request_to_raise_HTTPError(self):
        responses.add(**dict(
            method=responses.GET,
            url='http://viriato.rest.ch/api/get_to_raise_HTTPError',
            body='',
            status=400,
        ))
        with self.assertRaises(requests.exceptions.HTTPError) as http_error:
            self.CommunicationLayer.do_get_request('get_to_raise_HTTPError')

        self.assertIsInstance(http_error.exception, requests.exceptions.HTTPError)
        self.assertEqual(http_error.exception.response.status_code, 400)
        self.assertEqual(http_error.exception.response.reason, "Bad Request")

    @responses.activate
    def test_do_post_request_to_raise_HTTPError(self):
        responses.add(**dict(
            method=responses.POST,
            url='http://viriato.rest.ch/api/post_to_raise_HTTPError',
            body='',
            status=400
        ))

        with self.assertRaises(requests.exceptions.HTTPError) as http_error:
            self.CommunicationLayer.do_post_request('post_to_raise_HTTPError')

        self.assertIsInstance(http_error.exception, requests.exceptions.HTTPError)
        self.assertEqual(http_error.exception.response.status_code, 400)
        self.assertEqual(http_error.exception.response.reason, "Bad Request")

    @responses.activate
    def test_do_put_request_to_raise_HTTPError(self):
        responses.add(**dict(
            method=responses.PUT,
            url='http://viriato.rest.ch/api/put_to_raise_HTTPError',
            body='',
            status=400
        ))

        with self.assertRaises(requests.exceptions.HTTPError) as http_error:
            self.CommunicationLayer.do_put_request('put_to_raise_HTTPError')

        self.assertIsInstance(http_error.exception, requests.exceptions.HTTPError)
        self.assertEqual(http_error.exception.response.status_code, 400)
        self.assertEqual(http_error.exception.response.reason, "Bad Request")

    def tearDown(self) -> None:
        self.CommunicationLayer.currentSession.close()
