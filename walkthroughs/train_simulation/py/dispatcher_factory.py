from typing import Tuple

from py_client.aidm import AlgorithmTrain, AlgorithmTrainSimulationTrainPathNode, AlgorithmTrainSimulationTrain, StopStatus
from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
from dispatchers import (
    _Dispatcher,
    SimpleDispatcher,
    ChangeTrainOrderInFirstCommonTrainPathNodeDispatcher,
    ChangeTrainOrderInFirstCommonTrainPathNodeAddingAStopDispatcher,
    DispatcherType,
)
from algorithm_name import WALKTHROUGH_NAME


class DispatcherFactory:
    _algorithm_interface: AlgorithmInterface

    def __init__(self, algorithm_interface: AlgorithmInterface):
        self._algorithm_interface = algorithm_interface

    def create_dispatcher(self) -> _Dispatcher:
        dispatcher_choice = self._algorithm_interface.get_enum_algorithm_parameter(DispatcherType, "dispatcherChoice")
        algorithm_train_one = self._algorithm_interface.get_algorithm_train_parameter("timetableTrainOne")
        algorithm_train_two = self._algorithm_interface.get_algorithm_train_parameter("timetableTrainTwo")

        if dispatcher_choice == DispatcherType.simple_dispatcher:
            if algorithm_train_one is not None or algorithm_train_two is not None:
                self._algorithm_interface.notify_user(WALKTHROUGH_NAME, "Warning: Ignoring train choice for simple dispatcher.")
            return SimpleDispatcher(self._algorithm_interface)

        else:
            tpn_pair_result = self._retrieve_simulation_train_path_node_pair_on_first_common_node(algorithm_train_one, algorithm_train_two)
            if tpn_pair_result is None:
                return None
            preceding_train, tpn_preceding_train_on_given_node, succeeding_train, tpn_succeeding_train_on_given_node = tpn_pair_result

            if dispatcher_choice == DispatcherType.dispatcher_adding_a_stop_to_reverse_train_order:
                if tpn_preceding_train_on_given_node.forecast_stop_status != StopStatus.passing:
                    self._algorithm_interface.notify_user(WALKTHROUGH_NAME, "Train has already a planned stop, please select an other dispatcher.")
                    return None

                return ChangeTrainOrderInFirstCommonTrainPathNodeAddingAStopDispatcher(
                    self._algorithm_interface, preceding_train, tpn_preceding_train_on_given_node, tpn_succeeding_train_on_given_node
                )

            elif dispatcher_choice == DispatcherType.change_order_dispatcher:
                if tpn_preceding_train_on_given_node.forecast_stop_status == StopStatus.passing:
                    self._algorithm_interface.notify_user(WALKTHROUGH_NAME, "Train doesn't have a planned stop, please select an other dispatcher.")
                    return None

                return ChangeTrainOrderInFirstCommonTrainPathNodeDispatcher(
                    self._algorithm_interface, preceding_train, tpn_preceding_train_on_given_node, tpn_succeeding_train_on_given_node
                )
            else:
                raise Exception("unexpected dispatcher type.")

    def _retrieve_simulation_train_path_node_pair_on_first_common_node(
        self, train_one: AlgorithmTrain, train_two: AlgorithmTrain
    ) -> Tuple[AlgorithmTrain, AlgorithmTrainSimulationTrainPathNode, AlgorithmTrain, AlgorithmTrainSimulationTrainPathNode]:
        if train_one is None:
            self._algorithm_interface.notify_user(WALKTHROUGH_NAME, "Train one has to be selected.")
            return None

        if train_two is None:
            self._algorithm_interface.notify_user(WALKTHROUGH_NAME, "Train two has to be selected.")
            return None

        simulation_train_one = self._retrieve_simulation_train(train_one)
        simulation_train_two = self._retrieve_simulation_train(train_two)

        if simulation_train_one is None or simulation_train_two is None:
            return None

        tpns_by_node_ids_of_second_train = {tpn.node_id: tpn for tpn in simulation_train_two.train_path_nodes}

        for tpn_first_train in simulation_train_one.train_path_nodes:
            if tpn_first_train.node_id in tpns_by_node_ids_of_second_train:
                return self._order_simulation_train_path_node_by_departure_time(
                    train_one, tpn_first_train, train_two, tpns_by_node_ids_of_second_train[tpn_first_train.node_id]
                )

        self._algorithm_interface.notify_user(WALKTHROUGH_NAME, "The selected trains have no nodes in common.")
        return None

    def _retrieve_simulation_train(self, train: AlgorithmTrain) -> AlgorithmTrainSimulationTrain:
        simulation_trains = self._algorithm_interface.get_train_simulation_trains()
        simulation_train = next((simulation_train for simulation_train in simulation_trains if simulation_train.algorithm_train_id == train.id), None)
        if simulation_train is None:
            self._algorithm_interface.notify_user(
                WALKTHROUGH_NAME, "Cannot retrieve the train {} in the simulation. Pick a train within the time window of the simulation.".format(train.Code)
            )
            return None
        return simulation_train

    @staticmethod
    def _order_simulation_train_path_node_by_departure_time(
        train_one: AlgorithmTrain, tpn_one: AlgorithmTrainSimulationTrainPathNode, train_two: AlgorithmTrain, tpn_two: AlgorithmTrainSimulationTrainPathNode
    ) -> Tuple[AlgorithmTrain, AlgorithmTrainSimulationTrainPathNode, AlgorithmTrain, AlgorithmTrainSimulationTrainPathNode]:
        if tpn_one.forecast_departure_time < tpn_two.forecast_departure_time:
            return train_one, tpn_one, train_two, tpn_two
        else:
            return train_two, tpn_two, train_one, tpn_one
