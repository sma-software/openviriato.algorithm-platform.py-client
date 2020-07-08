from algorithm_interface.algorithm_interface import AlgorithmInterface


def create(base_url: str) -> AlgorithmInterface:
    return AlgorithmInterface(base_url=base_url)
