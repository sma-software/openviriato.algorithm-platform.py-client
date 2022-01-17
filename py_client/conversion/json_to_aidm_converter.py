from typing import Type, List
from py_client.conversion.json_to_aidm_processor import SectionTrackProcessor, JsonToAidmProcessor
from py_client.communication.response_processing import AlgorithmPlatformConversionError

class JsonToAidmConverter:
    __processors: List[JsonToAidmProcessor]

    def __init__(self):
        self.__processors = [SectionTrackProcessor()]

    def process_json_to_aidm(self, attribute_dict: dict, aidm_class: Type[object]) -> object:
        for processor in self.__processors:
            if processor.is_applicable(aidm_class):
                try:
                    return processor.process_attribute_dict(aidm_class, attribute_dict)
                except TypeError as error_instance:
                    raise AlgorithmPlatformConversionError(
                        "Could not populate AIDM object, client AIDM class deviates from server AIDM class",
                        error_instance)
        raise AlgorithmPlatformConversionError(
                        "Could not populate AIDM object, AIDM class {} is unknown.".format(aidm_class), None)