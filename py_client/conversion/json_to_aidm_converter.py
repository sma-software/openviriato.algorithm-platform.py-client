from typing import Type, List
from py_client.conversion.json_to_aidm_processors import AidmWithPrimitivesOrListOfPrimitivesProcessor, JsonToAidmProcessor
from py_client.communication.response_processing import AlgorithmPlatformConversionError
from py_client.aidm.aidm_base_classes import _HasID

class JsonToAidmConverter:

    def process_json_to_aidm(self, attribute_dict: dict, aidm_class: Type[object]) -> _HasID:
        try:
            return AidmWithPrimitivesOrListOfPrimitivesProcessor().process_attribute_dict(attribute_dict, aidm_class)
        except TypeError as e:
            raise AlgorithmPlatformConversionError(
                "Could not populate AIDM object, AIDM class {} is unknown.".format(aidm_class),
                e)