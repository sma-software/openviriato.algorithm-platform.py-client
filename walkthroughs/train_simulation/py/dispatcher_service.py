from datetime import timedelta

from py_client.aidm import (
    AlgorithmTrainSimulationEvent,
    AlgorithmTrainSimulationEventType,
    AlgorithmTrainSimulationRealizationForecast,
    AlgorithmTrainSimulationTrainPathNode,
    AlgorithmTrain,
)
from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
from algorithm_name import WALKTHROUGH_NAME


class DispatcherService:
    _algorithm_interface: AlgorithmInterface

    def __init__(self, algorithm_interface: AlgorithmInterface):
        self._algorithm_interface = algorithm_interface

    # @postpone_departure_in_given_node_of_preceding_train_or_realize_event[:]
    def postpone_departure_in_given_node_of_preceding_train_or_realize_event(
        self,
        simulation_event: AlgorithmTrainSimulationEvent,
        preceding_train: AlgorithmTrain,
        preceding_tpn_at_given_node: AlgorithmTrainSimulationTrainPathNode,
        succeeding_tpn_at_given_node: AlgorithmTrainSimulationTrainPathNode,
    ) -> AlgorithmTrainSimulationRealizationForecast:
        if self._need_to_postpone_preceding_tpn(simulation_event, preceding_tpn_at_given_node, succeeding_tpn_at_given_node):
            node_code = self._algorithm_interface.get_node(preceding_tpn_at_given_node.node_id).code
            self._algorithm_interface.notify_user(
                WALKTHROUGH_NAME,
                "Train {} departing from first node at {}: departure postponed at node {}.".format(
                    preceding_train.code, preceding_train.train_path_nodes[0].departure_time, node_code
                ),
            )

            time_to_postpone_preceding_train = self._calculate_time_to_postpone_to(simulation_event, succeeding_tpn_at_given_node)
            return self._algorithm_interface.postpone_next_train_simulation_event(time_to_postpone_preceding_train)

        return self._algorithm_interface.realize_next_train_simulation_event()

    @staticmethod
    def event_of_preceding_train_is_departure_at_given_node(
        simulation_event: AlgorithmTrainSimulationEvent, preceding_tpn_at_given_node: AlgorithmTrainSimulationTrainPathNode
    ) -> bool:

        if simulation_event.type is not AlgorithmTrainSimulationEventType.departure:
            return False

        return simulation_event.train_simulation_train_path_node_id == preceding_tpn_at_given_node.id

    @staticmethod
    def event_of_preceding_train_is_passing_at_given_node(
        simulation_event: AlgorithmTrainSimulationEvent, preceding_tpn_at_given_node: AlgorithmTrainSimulationTrainPathNode
    ) -> bool:

        if simulation_event.type is not AlgorithmTrainSimulationEventType.passing:
            return False

        return simulation_event.train_simulation_train_path_node_id == preceding_tpn_at_given_node.id

    @staticmethod
    def _need_to_postpone_preceding_tpn(
        any_simulation_event: AlgorithmTrainSimulationEvent,
        preceding_tpn_at_given_node: AlgorithmTrainSimulationTrainPathNode,
        succeeding_tpn_at_given_node: AlgorithmTrainSimulationTrainPathNode,
    ) -> bool:
        if not DispatcherService.event_of_preceding_train_is_departure_at_given_node(any_simulation_event, preceding_tpn_at_given_node):
            return False
        else:
            departure_event_of_preceding_train_at = any_simulation_event
            return departure_event_of_preceding_train_at.forecast_time <= succeeding_tpn_at_given_node.forecast_departure_time

    @staticmethod
    def _calculate_time_to_postpone_to(
        simulation_event: AlgorithmTrainSimulationEvent, succeeding_tpn_at_given_node: AlgorithmTrainSimulationTrainPathNode
    ) -> timedelta:
        return succeeding_tpn_at_given_node.forecast_departure_time - simulation_event.forecast_time + timedelta(minutes=1)
