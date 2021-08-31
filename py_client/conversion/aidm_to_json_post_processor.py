from abc import ABC, abstractmethod
from typing import Type, Tuple

from py_client.aidm import IncomingRoutingEdge, OutgoingRoutingEdge, ABCRoutingEdge, IncomingNodeTrackRoutingEdge, \
    CrossingRoutingEdge, OutgoingNodeTrackRoutingEdge, AlgorithmRosterLinkDefinition, LinkType, AlgorithmLink, \
    AlgorithmAwaitArrivalLink, AlgorithmConnectionLink, AlgorithmRosterLink
from py_client.conversion.converter_helpers import RoutingEdgeType


class ABCAIDMToJSONPostProcessor(ABC):
    __aidm_class: object

    @classmethod
    @abstractmethod
    def is_applicable(cls, aidm_class: Type[object]) -> bool:
        pass

    @classmethod
    @abstractmethod
    def process(cls, aidm_class: Type[object], attribute_dictionary: dict) -> dict:
        pass


class RoutingEdgeProcessor(ABCAIDMToJSONPostProcessor):
    __aidm_class = ABCRoutingEdge

    @classmethod
    def is_applicable(cls, aidm_class: Type[object]) -> bool:
        return isinstance(aidm_class, ABCRoutingEdge)

    @classmethod
    def process(cls, aidm_class: Type[object], attribute_dictionary: dict) -> dict:
        if isinstance(aidm_class, IncomingRoutingEdge):
            attribute_dictionary["type"] = RoutingEdgeType.incoming.value
            return attribute_dictionary
        elif isinstance(aidm_class, IncomingNodeTrackRoutingEdge):
            attribute_dictionary["type"] = RoutingEdgeType.incoming_node_track.value
            return attribute_dictionary
        elif isinstance(aidm_class, OutgoingRoutingEdge):
            attribute_dictionary["type"] = RoutingEdgeType.outgoing.value
            return attribute_dictionary
        elif isinstance(aidm_class, OutgoingNodeTrackRoutingEdge):
            attribute_dictionary["type"] = RoutingEdgeType.outgoing_node_track.value
            return attribute_dictionary
        elif isinstance(aidm_class, CrossingRoutingEdge):
            attribute_dictionary["type"] = RoutingEdgeType.crossing.value
            return attribute_dictionary
        else:
            raise NotImplementedError(f"RoutingEdge {aidm_class} can not be converted to json")


class AlgorithmRosterLinkDefinitionPostProcessor(ABCAIDMToJSONPostProcessor):
    @classmethod
    def is_applicable(cls, aidm_class: Type[object]) -> bool:
        return isinstance(aidm_class, AlgorithmRosterLinkDefinition)

    @classmethod
    def process(cls, _: Type[object], attribute_dictionary: dict) -> dict:
        attribute_dictionary["type"] = LinkType.roster.value
        return attribute_dictionary


class AlgorithmLinkPostProcessor(ABCAIDMToJSONPostProcessor):
    # Only required for End-To-End-Test, placed here for convenience.
    @classmethod
    def is_applicable(cls, aidm_class: Type[object]) -> bool:
        return isinstance(aidm_class, AlgorithmLink)

    @classmethod
    def process(cls, aidm_class: Type[object], attribute_dictionary: dict) -> dict:
        if isinstance(aidm_class, AlgorithmAwaitArrivalLink):
            attribute_dictionary["type"] = LinkType.await_arrival.value
            return attribute_dictionary
        elif isinstance(aidm_class, AlgorithmConnectionLink):
            attribute_dictionary["type"] = LinkType.connection.value
            return attribute_dictionary
        elif isinstance(aidm_class, AlgorithmRosterLink):
            attribute_dictionary["type"] = LinkType.roster.value
            return attribute_dictionary
        else:
            raise NotImplementedError(f"RoutingEdge {aidm_class} can not be converted to json")


class AIDMToJSONPostProcessorChain:
    __processors: Tuple[ABCAIDMToJSONPostProcessor, ...] = (
        RoutingEdgeProcessor, AlgorithmRosterLinkDefinitionPostProcessor, AlgorithmLinkPostProcessor,
    )

    @classmethod
    def post_process_aidm_as_json(cls, attribute_dict: dict, aidm_class: Type[object]) -> dict:
        for processor in cls.__processors:
            if processor.is_applicable(aidm_class):
                return processor.process(aidm_class, attribute_dict)
        return attribute_dict
