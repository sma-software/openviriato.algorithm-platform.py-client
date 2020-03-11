from AlgorithmInterface.AlgorithmInterface import AlgorithmicPlatformInterface


def create(base_url: str):
    return AlgorithmicPlatformInterface(base_url=base_url)
