import unittest

import ConverterLayer.from_AIDM_converter
from AIDMClasses import AIDM_classes


class TestFromAIDMConverter(unittest.TestCase):

    def test_convert_to_json_conform_dict(self):
        test_section = AIDM_classes.AlgorithmSectionTrack(ID=12, Code='ATest', DebugString='str', Weight=8,
                                                        SectionCode='TestSection')

        test_section_as_dict = ConverterLayer.from_AIDM_converter.convert_to_json_conform_dict(test_section)

        self.assertIsInstance(test_section_as_dict, dict)
        self.assertEqual(test_section_as_dict['ID'], 12)
        self.assertEqual(test_section_as_dict['Code'], 'ATest')
        self.assertEqual(test_section_as_dict['DebugString'], 'str')
        self.assertEqual(test_section_as_dict['Weight'], 8)
        self.assertEqual(test_section_as_dict['SectionCode'], 'TestSection')

    def test_convert_to_list_of_dict_emtpy(self):
        test_list_of_dict = []

        test_section_list = ConverterLayer.from_AIDM_converter.convert_to_list_of_dict(test_list_of_dict)

        self.assertIsInstance(test_section_list, list)
        self.assertListEqual(test_section_list, [])

    def test_convert_to_list_of_dict(self):
        algorithm_section_track = AIDM_classes.AlgorithmSectionTrack(ID=12, Code='ATest', DebugString='str', Weight=8,
                                                          SectionCode='TestSection')
        test_list_of_algorithm_section_track = [algorithm_section_track, algorithm_section_track,
                                                algorithm_section_track]

        test_section_list_of_dict = ConverterLayer.from_AIDM_converter.convert_to_list_of_dict(
            test_list_of_algorithm_section_track)

        self.assertIsInstance(test_section_list_of_dict, list)
        self.assertIsInstance(test_section_list_of_dict[0], dict)
        self.assertEqual(test_section_list_of_dict[0]['DebugString'], 'str')
