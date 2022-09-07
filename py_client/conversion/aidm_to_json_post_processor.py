from abc import ABC, abstractmethod
from typing import Type, Tuple

from py_client.aidm import (
    IncomingRoutingEdge,
    OutgoingRoutingEdge,
    IncomingNodeTrackRoutingEdge,
    CrossingRoutingEdge,
    OutgoingNodeTrackRoutingEdge,
    AlgorithmRosterLinkDefinition,
    LinkType,
    AlgorithmAwaitArrivalLink,
    AlgorithmConnectionLink,
    AlgorithmRosterLink,
)
from py_client.conversion.converter_helpers import RoutingEdgeType


class ABCAIDMToJSONPostProcessor(ABC):
    __aidm_class: object

    @classmethod
    @abstractmethod
    def is_applicable(cls, aidm_class: Type[object]) -> bool:
        pass

    @classmethod
    @abstractmethod
    def process_attribute_dict(cls, aidm_class: Type[object], attribute_dictionary: dict) -> None:
        pass


class RoutingEdgeProcessor(ABCAIDMToJSONPostProcessor):
    @staticmethod
    def __get_routing_edge_types():
        return (
            IncomingRoutingEdge,
            IncomingNodeTrackRoutingEdge,
            OutgoingRoutingEdge,
            OutgoingNodeTrackRoutingEdge,
            CrossingRoutingEdge,
        )

    @classmethod
    def is_applicable(cls, aidm_class: Type[object]) -> bool:
        return isinstance(aidm_class, cls.__get_routing_edge_types())

    @classmethod
    def process_attribute_dict(cls, aidm_class: Type[object], attribute_dictionary: dict) -> None:
        if isinstance(aidm_class, IncomingRoutingEdge):
            attribute_dictionary["type"] = RoutingEdgeType.incoming.value
        elif isinstance(aidm_class, IncomingNodeTrackRoutingEdge):
            attribute_dictionary["type"] = RoutingEdgeType.incoming_node_track.value
        elif isinstance(aidm_class, OutgoingRoutingEdge):
            attribute_dictionary["type"] = RoutingEdgeType.outgoing.value
        elif isinstance(aidm_class, OutgoingNodeTrackRoutingEdge):
            attribute_dictionary["type"] = RoutingEdgeType.outgoing_node_track.value
        elif isinstance(aidm_class, CrossingRoutingEdge):
            attribute_dictionary["type"] = RoutingEdgeType.crossing.value
        else:
            raise NotImplementedError(f"RoutingEdge {aidm_class} can not be converted to json")


class AlgorithmRosterLinkDefinitionPostProcessor(ABCAIDMToJSONPostProcessor):
    @classmethod
    def is_applicable(cls, aidm_class: Type[object]) -> bool:
        return isinstance(aidm_class, AlgorithmRosterLinkDefinition)

    @classmethod
    def process_attribute_dict(cls, _: Type[object], attribute_dictionary: dict) -> None:
        attribute_dictionary["type"] = LinkType.roster.value


class AlgorithmAwaitArrivalLinkPostProcessor(ABCAIDMToJSONPostProcessor):
    # Only required for End-To-End-Test, placed here for convenience.
    @classmethod
    def is_applicable(cls, aidm_class: Type[object]) -> bool:
        return isinstance(aidm_class, AlgorithmAwaitArrivalLink)

    @classmethod
    def process_attribute_dict(cls, _: Type[object], attribute_dictionary: dict) -> None:
        attribute_dictionary["type"] = LinkType.await_arrival.value


class AlgorithmConnectionLinkPostProcessor(ABCAIDMToJSONPostProcessor):
    # Only required for End-To-End-Test, placed here for convenience.
    @classmethod
    def is_applicable(cls, aidm_class: Type[object]) -> bool:
        return isinstance(aidm_class, AlgorithmConnectionLink)

    @classmethod
    def process_attribute_dict(cls, _: Type[object], attribute_dictionary: dict) -> None:
        attribute_dictionary["type"] = LinkType.connection.value


class AlgorithmRosterLinkPostProcessor(ABCAIDMToJSONPostProcessor):
    # Only required for End-To-End-Test, placed here for convenience.
    @classmethod
    def is_applicable(cls, aidm_class: Type[object]) -> bool:
        return isinstance(aidm_class, AlgorithmRosterLink)

    @classmethod
    def process_attribute_dict(cls, _: Type[object], attribute_dictionary: dict) -> None:
        attribute_dictionary["type"] = LinkType.roster.value


class AIDMToJSONPostProcessorChain:
    __processors: Tuple[ABCAIDMToJSONPostProcessor, ...] = (
        RoutingEdgeProcessor,
        AlgorithmRosterLinkDefinitionPostProcessor,
        AlgorithmAwaitArrivalLinkPostProcessor,
        AlgorithmConnectionLinkPostProcessor,
        AlgorithmRosterLinkPostProcessor,
    )

    @classmethod
    def post_process_aidm_as_json(cls, attribute_dict: dict, aidm_class: Type[object]) -> dict:
        for processor in cls.__processors:
            if processor.is_applicable(aidm_class):
                processor.process_attribute_dict(aidm_class, attribute_dict)
                return attribute_dict
        return attribute_dict
