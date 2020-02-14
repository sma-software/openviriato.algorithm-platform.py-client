import unittest

import AlgorithmPlatformPyClient


# test which dont need a mock
class TestObjectInitialisation(unittest.TestCase):
    # test for the object creation:
    def test_initialisation_in_with(self):
        url_str = 'http://localhost:8080'
        with AlgorithmPlatformPyClient.AlgorithmicPlatformInterface(url_str) as interface_to_viriato:
            self.assertEqual(interface_to_viriato.base_url, url_str)

    # fails on purpose:
    def test_if_initialisation_with_int_fails(self):
        url_nr = 952022
        with self.assertRaises(AssertionError):
            with AlgorithmPlatformPyClient.AlgorithmicPlatformInterface(url_nr) as interface_to_viriato:
                raise NotImplementedError('there is an assertion not raised')


if __name__ == '__main__':
    unittest.main()
