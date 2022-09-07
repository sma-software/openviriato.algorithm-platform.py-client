import unittest

from py_client.aidm import AlgorithmNodeTrack, AlgorithmNode
from py_client.communication.response_processing import AlgorithmPlatformConversionError
from py_client.conversion.json_to_aidm_converter import JsonToAidmConverter


class TestEqualityOfRESTJsonAndAIDMObjectValidated(unittest.TestCase):
    def test_convert_with_aidm_class_missing_attribute_raises_exception(self):
        node_track_as_dict_with_missing_code_attribute = dict(ID=1, DebugString="CodeIsMissing")

        with self.assertRaises(AlgorithmPlatformConversionError, msg="__init__() missing 1 required positional argument: 'Code'"):
            JsonToAidmConverter().process_json_to_aidm(node_track_as_dict_with_missing_code_attribute, AlgorithmNodeTrack)

    def test_convert_with_aidm_class_unexpected_attribute_raises_exception(self):
        node_track_as_dict_with_additional_attribute = dict(ID=1, Code="2", DebugString="3")
        node_track_as_dict_with_additional_attribute["ThisIs___AWrongName"] = "unexpectedAttribute"

        with self.assertRaises(AlgorithmPlatformConversionError, msg="__init__() got an unexpected keyword argument 'ThisIs___AWrongName'"):
            JsonToAidmConverter().process_json_to_aidm(node_track_as_dict_with_additional_attribute, AlgorithmNodeTrack)

    def test_convert_with_aidm_factory_missing_attribute_raises_exception(self):
        algorithm_node_with_missing_code_attribute = dict(ID=15, DebugString="test123", NodeTracks=[])

        with self.assertRaises(AlgorithmPlatformConversionError, msg="__init__() missing 1 required positional argument: 'Code'"):
            JsonToAidmConverter().process_json_to_aidm(algorithm_node_with_missing_code_attribute, AlgorithmNode)

    def test_convert_with_aidm_factory_unexpected_attribute_raises_exception(self):
        algorithm_node_with_additional_attribute = dict(ID=15, Code="A", DebugString="test123", NodeTracks=[])
        algorithm_node_with_additional_attribute["__A__WrongName"] = "unexpectedAttribute"

        with self.assertRaises(AlgorithmPlatformConversionError, msg="__init__() got an unexpected keyword argument '__A__WrongName'"):
            JsonToAidmConverter().process_json_to_aidm(algorithm_node_with_additional_attribute, AlgorithmNode)
