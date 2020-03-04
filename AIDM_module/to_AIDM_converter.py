"""
class AlgorithmSectionTrack(hasID, hasCode, hasDebugString):
    __Weight: int
    __SectionCode: str

    def __init__(self, ID: int, Code: str, DebugString: str, Weight: int, SectionCode: str):
        hasID.__init__(self, ID)
        hasCode.__init__(self, Code)
        hasDebugString.__init__(self, DebugString)
        self.__Weight = Weight
        self.__SectionCode = SectionCode

    @classmethod
    def convert_dict_to_AIDM(cls, json_dict: dict):
        return cls(**json_dict)
"""
import AIDM_module.AIDM_classes


def convert_dict_to_AIDM(AIDM_class, attribute_dict: dict):
    return AIDM_class(**attribute_dict)


def from_list_of_dict_to_list_of_AIDM(AIDM_class, list_of_dict: list):
    return [convert_dict_to_AIDM(AIDM_class, dict_from_list) for dict_from_list in list_of_dict]


def convert_dict_to_AlgorithmNode(attribute_dict: dict) -> AIDM_module.AIDM_classes.AlgorithmNode:
    attribute_dict['NodeTracks'] = from_list_of_dict_to_list_of_AIDM(AIDM_module.AIDM_classes.AlgorithmNodeTrack, attribute_dict['NodeTracks'])
    return convert_dict_to_AIDM(AIDM_module.AIDM_classes.AlgorithmNode, attribute_dict)


def from_list_of_dict_to_AlgorithmNode(attribute_dict: dict) -> list:
    return [convert_dict_to_AIDM(AIDM_class, dict_from_list) for dict_from_list in list_of_dict]
    attribute_dict['NodeTracks'] = from_list_of_dict_to_list_of_AIDM(AIDM_module.AIDM_classes.AlgorithmNodeTrack, attribute_dict['NodeTracks'])
    return convert_dict_to_AIDM(AIDM_module.AIDM_classes.AlgorithmNode, attribute_dict)