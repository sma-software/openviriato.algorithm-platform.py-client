import argparse

from py_client.algorithm_interface import algorithm_interface_factory
from RerouteTrainAlgorithm import RerouteTrainAlgorithm


def reroute_train_runner(api_url: str):
    with algorithm_interface_factory.create(api_url) as algorithm_interface:
        reroute_train_algorithm = RerouteTrainAlgorithm()
        reroute_train_algorithm.run(algorithm_interface)


def parse_api_url_from_command_line_arguments() -> str:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-u", "--api_url", required=True)
    command_line_arguments = vars(argument_parser.parse_args())
    api_url: str = command_line_arguments["api_url"]
    return api_url


def main():
    api_url = parse_api_url_from_command_line_arguments()
    reroute_train_runner(api_url=api_url)


if __name__ == '__main__':
    main()
