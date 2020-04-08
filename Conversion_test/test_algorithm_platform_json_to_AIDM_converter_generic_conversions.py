import unittest

import AIDMClasses
from Conversion import algorithm_platform_json_to_AIDM_converter



class TestToAIDMConverterGenericConversions(unittest.TestCase):

    def test_convert_dict_to_AIDM(self):
        test_section_as_dict = dict(ID=12, Code='ATest', DebugString='str', Weight=8, SectionCode='TestSection')

        test_section = algorithm_platform_json_to_AIDM_converter.convert(
            AIDMClasses.AlgorithmSectionTrack, test_section_as_dict)

        self.assertIsInstance(test_section, AIDMClasses.AlgorithmSectionTrack)
        self.assertEqual(test_section.ID, 12)
        self.assertEqual(test_section.Code, 'ATest')
        self.assertEqual(test_section.DebugString, 'str')
        self.assertEqual(test_section.Weight, 8)
        self.assertEqual(test_section.SectionCode, 'TestSection')

    def test_convert_list_of_dict_to_list_of_AIDM(self):
        test_section_as_dict = dict(ID=12, Code='ATest', DebugString='str', Weight=8, SectionCode='TestSection')
        test_section_dict_in_list = [test_section_as_dict, test_section_as_dict, test_section_as_dict]

        test_section_list = algorithm_platform_json_to_AIDM_converter.convert_list(AIDMClasses.AlgorithmSectionTrack,
                                                                                   test_section_dict_in_list)

        self.assertIsInstance(test_section_list, list)
        self.assertIsInstance(test_section_list[0], AIDMClasses.AlgorithmSectionTrack)
        self.assertEqual(test_section_list[0].DebugString, 'str')