import argparse
import datetime

from py_client.algorithm_interface import algorithm_interface_factory
from py_client.aidm import (
    UpdateTimesTrainPathNode,
    AlgorithmTrainSimulationEventType,
    TimeWindow,
    StopStatus,
    AlgorithmTrainPathNode,
    AlgorithmTrainSimulationCreationArguments,
)
from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
from dispatcher_factory import DispatcherFactory


def run(api_url: str) -> None:
    with algorithm_interface_factory.create(api_url) as algorithm_interface:
        # @start_simulation[:3]
        time_window = algorithm_interface.get_time_window_algorithm_parameter("trainSimulationTimeWindow")
        algorithm_train_simulation_creation_arguments = AlgorithmTrainSimulationCreationArguments(time_window=time_window)
        algorithm_interface.create_train_simulation(algorithm_train_simulation_creation_arguments=algorithm_train_simulation_creation_arguments)

        dispatcher = DispatcherFactory(algorithm_interface).create_dispatcher()
        if dispatcher is None:
            return

        # @main_loop_controlling_simulation[1:5]
        algorithm_interface.show_status_message("Running simulation...")
        realization_forecast = algorithm_interface.get_next_train_simulation_event()
        while realization_forecast.next_realizable_event is not None:
            algorithm_interface.show_status_message("Simulating at {}".format(realization_forecast.next_realizable_event.forecast_time))
            realization_forecast = dispatcher.make_decision_for_event(realization_forecast.next_realizable_event)

        algorithm_interface.show_status_message("Writing back result to Viriato")
        _persist_updated_trains(algorithm_interface, time_window)
        algorithm_interface.notify_user("Walkthrough Train Simulation", "Simulation carried out. Result written back to Viriato.")


# @persisting_updated_trains[:]
def _persist_updated_trains(algorithm_interface: AlgorithmInterface, time_window: TimeWindow) -> None:
    all_trains = algorithm_interface.get_trains(time_window)
    all_train_simulations_trains = algorithm_interface.get_train_simulation_trains()

    realized_arrival_times_by_tpn_id = dict()
    realized_departure_times_by_tpn_id = dict()
    for simulation_train in all_train_simulations_trains:
        for event in simulation_train.events:
            if event.type == AlgorithmTrainSimulationEventType.passing or event.type == AlgorithmTrainSimulationEventType.arrival:
                realized_arrival_times_by_tpn_id[event.algorithm_train_path_node_id] = event.forecast_time
            if event.type == AlgorithmTrainSimulationEventType.passing or event.type == AlgorithmTrainSimulationEventType.departure:
                realized_departure_times_by_tpn_id[event.algorithm_train_path_node_id] = event.forecast_time

    for train in all_trains:
        updated_train_path_nodes = []

        for train_path_node in train.train_path_nodes:
            stop_status = _determine_stop_status(
                train_path_node, realized_arrival_times_by_tpn_id[train_path_node.id], realized_departure_times_by_tpn_id[train_path_node.id]
            )

            updated_train_path_node = UpdateTimesTrainPathNode(
                train_path_node.id,
                realized_arrival_times_by_tpn_id[train_path_node.id],
                realized_departure_times_by_tpn_id[train_path_node.id],
                None,
                None,
                stop_status,
            )
            updated_train_path_nodes.append(updated_train_path_node)
        algorithm_interface.update_train_times(train.id, updated_train_path_nodes)


def _determine_stop_status(train_path_node: AlgorithmTrainPathNode, arrival_time: datetime, departure_time: datetime) -> StopStatus:
    if train_path_node.stop_status is StopStatus.passing and arrival_time is not departure_time:
        return StopStatus.operational_stop
    else:
        return train_path_node.stop_status


def parse_api_url_from_command_line_arguments() -> str:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-u", "--api_url", required=True)
    command_line_arguments = vars(argument_parser.parse_args())
    api_url: str = command_line_arguments["api_url"]
    return api_url


def main():
    api_url = parse_api_url_from_command_line_arguments()
    run(api_url=api_url)


if __name__ == "__main__":
    main()
