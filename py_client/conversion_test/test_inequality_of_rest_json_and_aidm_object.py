import unittest
from py_client.aidm import AlgorithmNodeTrack
from py_client.conversion.algorithm_platform_json_to_aidm_converter import convert, convert_json_to_algorithm_node


class TestEqualityOfRESTJsonAndAIDMObjectValidated(unittest.TestCase):

    def test_convert_with_aidm_class_missing_attribute_raises_exception(self):
        node_track_as_dict_with_missing_code_attribute = dict(ID=1, DebugString="CodeIsMissing")

        with self.assertRaises(TypeError, msg="__init__() missing 1 required positional argument: 'Code'"):
            convert(AlgorithmNodeTrack, node_track_as_dict_with_missing_code_attribute)

    def test_convert_with_aidm_class_unexpected_attribute_raises_exception(self):
        node_track_as_dict_with_additional_attribute = dict(ID=1, Code='2', DebugString='3')
        node_track_as_dict_with_additional_attribute['ThisIs___AWrongName'] = 'unexpectedAttribute'

        with self.assertRaises(TypeError, msg="__init__() got an unexpected keyword argument 'ThisIs___AWrongName'"):
            convert(AlgorithmNodeTrack, node_track_as_dict_with_additional_attribute)

    def test_convert_with_aidm_factory_missing_attribute_raises_exception(self):
        algorithm_node_with_missing_code_attribute = dict(ID=15, DebugString='test123', NodeTracks=[])

        with self.assertRaises(TypeError, msg="__init__() missing 1 required positional argument: 'Code'"):
            convert(convert_json_to_algorithm_node, algorithm_node_with_missing_code_attribute)

    def test_convert_with_aidm_factory_unexpected_attribute_raises_exception(self):
        algorithm_node_with_additional_attribute = dict(ID=15, Code='A', DebugString='test123', NodeTracks=[])
        algorithm_node_with_additional_attribute['__A__WrongName'] = 'unexpectedAttribute'

        with self.assertRaises(TypeError, msg="__init__() got an unexpected keyword argument '__A__WrongName'"):
            convert(convert_json_to_algorithm_node, algorithm_node_with_additional_attribute)
