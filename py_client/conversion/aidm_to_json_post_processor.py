from abc import ABC
from typing import Type, Tuple

from py_client.aidm import IncomingRoutingEdge, CrossingRoutingEdge, OutgoingRoutingEdge, RoutingEdgeType
from py_client.aidm.aidm_base_classes import _RoutingEdge


class ABCAIDMToJSONPostProcessor(ABC):
    __aidm_class: object

    @classmethod
    def is_applicable(cls, aidm_class: Type[object]) -> bool:
        pass

    @classmethod
    def process(cls, aidm_class: Type[object], attribute_dictionary: dict) -> dict:
        pass


class RoutingEdgeProcessor(ABCAIDMToJSONPostProcessor):
    __aidm_class = _RoutingEdge

    @classmethod
    def is_applicable(cls, aidm_class: Type[object]) -> bool:
        return isinstance(aidm_class, _RoutingEdge)

    @classmethod
    def process(cls, aidm_class: Type[object], attribute_dictionary: dict) -> dict:
        if isinstance(aidm_class, IncomingRoutingEdge):
            attribute_dictionary["type"] = RoutingEdgeType.incoming.value
            return attribute_dictionary
        elif isinstance(aidm_class, OutgoingRoutingEdge):
            attribute_dictionary["type"] = RoutingEdgeType.outgoing.value
            return attribute_dictionary
        elif isinstance(aidm_class, CrossingRoutingEdge):
            attribute_dictionary["type"] = RoutingEdgeType.crossing.value
            return attribute_dictionary
        else:
            raise NotImplementedError(f"RoutingEdge {aidm_class} can not be converted to json")


class AIDMToJSONPostProcessorChain:
    __processors: Tuple[ABCAIDMToJSONPostProcessor, ...] = (
        RoutingEdgeProcessor,)

    @classmethod
    def post_process_aidm_as_json(cls, attribute_dict: dict, aidm_class: Type[object]) -> dict:
        for processor in cls.__processors:
            if processor.is_applicable(aidm_class):
                return processor.process(aidm_class, attribute_dict)
        return attribute_dict
