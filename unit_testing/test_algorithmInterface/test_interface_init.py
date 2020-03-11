import unittest

from AlgorithmInterface import AlgorithmInterfaceFactory


# test which dont need a mock
class TestObjectInitialisation(unittest.TestCase):
    # test for the object creation:
    def test_initialisation_in_with(self):
        url_str = 'http://localhost:8080'
        with AlgorithmInterfaceFactory.AlgorithmicPlatformInterface(url_str) as interface_to_viriato:
            self.assertEqual(interface_to_viriato.base_url, url_str)


if __name__ == '__main__':
    unittest.main()
