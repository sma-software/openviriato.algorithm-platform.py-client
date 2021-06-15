import argparse

from py_client.algorithm_interface import algorithm_interface_factory


def count_trains_in_time_window(api_url: str):
    with algorithm_interface_factory.create(api_url) as algorithm_interface:
        time_window = algorithm_interface.get_time_window_algorithm_parameter("timeWindowParameter")
        trains_in_window = algorithm_interface.get_trains(time_window)

        algorithm_interface.notify_user(
            "count_trains_algorithm",
            "Found {0} trains in time window from {1} to {2}".format(
                len(trains_in_window),
                time_window.from_time,
                time_window.to_time))


def parse_api_url_from_command_line_arguments() -> str:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-u", "--api_url", required=True)
    command_line_arguments = vars(argument_parser.parse_args())
    api_url: str = command_line_arguments["api_url"]
    return api_url


def main():
    api_url = parse_api_url_from_command_line_arguments()
    count_trains_in_time_window(api_url=api_url)


if __name__ == '__main__':
    main()
