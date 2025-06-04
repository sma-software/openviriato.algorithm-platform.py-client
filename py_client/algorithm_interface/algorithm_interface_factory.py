from py_client.algorithm_interface.algorithm_interface import AlgorithmInterface


def create(base_url: str, log_file: str = None) -> AlgorithmInterface:
    return AlgorithmInterface(base_url=base_url, log_file=log_file)
