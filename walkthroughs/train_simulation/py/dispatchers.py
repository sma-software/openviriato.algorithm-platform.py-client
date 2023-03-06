from abc import abstractmethod
from enum import Enum

from py_client.aidm import (
    AlgorithmTrainSimulationEvent,
    AlgorithmTrainSimulationRealizationForecast,
    AlgorithmTrain,
    AlgorithmTrainPathNode,
)
from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
from dispatcher_service import DispatcherService
from algorithm_name import WALKTHROUGH_NAME


class DispatcherType(Enum):
    simple_dispatcher = "simpleDispatcher"
    dispatcher_adding_a_stop_to_reverse_train_order = "addStopDispatcher"
    change_order_dispatcher = "changeOrderDispatcher"


# @dispatchers_structure[:]
class _Dispatcher:
    @abstractmethod
    def make_decision_for_event(self, simulation_event: AlgorithmTrainSimulationEvent) -> AlgorithmTrainSimulationRealizationForecast:
        pass


# @SimpleDispatcher[:]
class SimpleDispatcher(_Dispatcher):
    _algorithm_interface: AlgorithmInterface

    def __init__(self, algorithm_interface: AlgorithmInterface):
        self._algorithm_interface = algorithm_interface

    def make_decision_for_event(self, simulation_event: AlgorithmTrainSimulationEvent) -> AlgorithmTrainSimulationRealizationForecast:
        return self._algorithm_interface.realize_next_train_simulation_event()


# @ChangeTrainOrderInFirstCommonTrainPathNodeDispatcher[:]
class ChangeTrainOrderInFirstCommonTrainPathNodeDispatcher(_Dispatcher):
    _algorithm_interface: AlgorithmInterface
    _preceding_train: AlgorithmTrain
    _tpn_first_common_node_preceding_train: AlgorithmTrainPathNode
    _tpn_first_common_node_succeeding_train: AlgorithmTrainPathNode
    _dispatcher_service: DispatcherService

    def __init__(
        self,
        algorithm_interface: AlgorithmInterface,
        preceding_train: AlgorithmTrain,
        tpn_first_common_node_preceding_train: AlgorithmTrainPathNode,
        tpn_first_common_node_succeeding_train: AlgorithmTrainPathNode,
    ):
        self._algorithm_interface = algorithm_interface
        self._preceding_train = preceding_train
        self._tpn_first_common_node_preceding_train = tpn_first_common_node_preceding_train
        self._tpn_first_common_node_succeeding_train = tpn_first_common_node_succeeding_train
        self._dispatcher_service = DispatcherService(algorithm_interface)

    def make_decision_for_event(self, simulation_event: AlgorithmTrainSimulationEvent) -> AlgorithmTrainSimulationRealizationForecast:
        return self._dispatcher_service.postpone_departure_in_given_node_of_preceding_train_or_realize_event(
            simulation_event, self._preceding_train, self._tpn_first_common_node_preceding_train, self._tpn_first_common_node_succeeding_train
        )


# @ChangeTrainOrderInFirstCommonTrainPathNodeAddingAStopDispatcher[:]
class ChangeTrainOrderInFirstCommonTrainPathNodeAddingAStopDispatcher(_Dispatcher):
    _algorithm_interface: AlgorithmInterface
    _preceding_train = AlgorithmTrain
    _tpn_first_common_node_preceding_train: AlgorithmTrainPathNode
    _tpn_first_common_node_succeeding_train: AlgorithmTrainPathNode
    _dispatcher_service: DispatcherService

    def __init__(
        self,
        algorithm_interface: AlgorithmInterface,
        preceding_train: AlgorithmTrain,
        tpn_first_common_node_preceding_train: AlgorithmTrainPathNode,
        tpn_first_common_node_succeeding_train: AlgorithmTrainPathNode,
    ):
        self._algorithm_interface = algorithm_interface
        self._preceding_train = preceding_train
        self._tpn_first_common_node_preceding_train = tpn_first_common_node_preceding_train
        self._tpn_first_common_node_succeeding_train = tpn_first_common_node_succeeding_train
        self._dispatcher_service = DispatcherService(algorithm_interface)

    def make_decision_for_event(self, simulation_event: AlgorithmTrainSimulationEvent) -> AlgorithmTrainSimulationRealizationForecast:
        if self._dispatcher_service.event_of_preceding_train_is_passing_at_given_node(simulation_event, self._tpn_first_common_node_preceding_train):
            node_code = self._algorithm_interface.get_node(self._tpn_first_common_node_preceding_train.node_id).code
            self._algorithm_interface.notify_user(
                WALKTHROUGH_NAME,
                "Train {} departing from first node at {}: stop introduced at node {}.".format(
                    self._preceding_train.code, self._preceding_train.train_path_nodes[0].departure_time, node_code
                ),
            )

            return self._algorithm_interface.replace_next_train_simulation_event_by_stop()
        else:
            return self._dispatcher_service.postpone_departure_in_given_node_of_preceding_train_or_realize_event(
                simulation_event, self._preceding_train, self._tpn_first_common_node_preceding_train, self._tpn_first_common_node_succeeding_train
            )
