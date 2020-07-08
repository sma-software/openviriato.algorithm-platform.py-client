import unittest
from py_client.aidm import AlgorithmNodeTrack
import py_client.Conversion.algorithm_platform_json_to_AIDM_converter as algorithm_platform_json_to_AIDM_converter


class TestEqualityOfRESTJsonAndAIDMObjectValidated(unittest.TestCase):

    def test_convert_with_AIDM_class_missing_attribute_raises_exception(self):
        node_track_as_dict_with_missing_code_attribute  = dict(ID=1, DebugString= "CodeIsMissing")

        with self.assertRaises(TypeError, msg="__init__() missing 1 required positional argument: 'Code'"):
            algorithm_platform_json_to_AIDM_converter.convert(
                AlgorithmNodeTrack,
                node_track_as_dict_with_missing_code_attribute)

    def test_convert_with_AIDM_class_unexpected_attribute_raises_exception(self):
        node_track_as_dict_with_additional_attribute = dict(ID=1, Code='2', DebugString='3')
        node_track_as_dict_with_additional_attribute['ThisIs___AWrongName'] = 'unexpectedAttribute'

        with self.assertRaises(TypeError, msg="__init__() got an unexpected keyword argument 'ThisIs___AWrongName'"):
            algorithm_platform_json_to_AIDM_converter.convert(
                AlgorithmNodeTrack,
                node_track_as_dict_with_additional_attribute)

    def test_convert_with_AIDM_factory_missing_attribute_raises_exception(self):
        algorithm_node_with_missing_code_attribute = dict(ID=15, DebugString='test123', NodeTracks=[])

        with self.assertRaises(TypeError, msg="__init__() missing 1 required positional argument: 'Code'"):
            algorithm_platform_json_to_AIDM_converter.convert(
                algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmNode,
                algorithm_node_with_missing_code_attribute)

    def test_convert_with_AIDM_factory_unexpected_attribute_raises_exception(self):
        algorithm_node_with_additional_attribute = dict(ID=15, Code='A', DebugString='test123', NodeTracks=[])
        algorithm_node_with_additional_attribute['__A__WrongName'] = 'unexpectedAttribute'

        with self.assertRaises(TypeError, msg="__init__() got an unexpected keyword argument '__A__WrongName'"):
            algorithm_platform_json_to_AIDM_converter.convert(
                algorithm_platform_json_to_AIDM_converter.convert_json_to_AlgorithmNode,
                algorithm_node_with_additional_attribute)
