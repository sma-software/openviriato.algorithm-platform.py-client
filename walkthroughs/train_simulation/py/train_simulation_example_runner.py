import argparse

from py_client.algorithm_interface import algorithm_interface_factory
from py_client.aidm import UpdateTimesTrainPathNode
from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface
from dispatcher_factory import DispatcherFactory


def run(api_url: str) -> None:
    with algorithm_interface_factory.create(api_url) as algorithm_interface:
        # @start_simulation[:2]
        time_window = algorithm_interface.get_time_window_algorithm_parameter("trainSimulationTimeWindow")
        algorithm_interface.create_train_simulation(time_window)

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
        _persist_updated_trains(algorithm_interface)
        algorithm_interface.notify_user("Walkthrough Train Simulation", "Simulation carried out. Result written back to Viriato.")


# @persisting_updated_trains[:]
def _persist_updated_trains(algorithm_interface: AlgorithmInterface) -> None:
    for train in algorithm_interface.get_train_simulation_trains():
        updated_train_path_nodes = []
        for tpn in train.train_path_nodes:
            updated_train_path_node = UpdateTimesTrainPathNode(
                tpn.algorithm_train_path_node_id, tpn.forecast_arrival_time, tpn.forecast_departure_time, None, None, tpn.forecast_stop_status
            )
            updated_train_path_nodes.append(updated_train_path_node)

        algorithm_interface.update_train_times(train.algorithm_train_id, updated_train_path_nodes)


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
