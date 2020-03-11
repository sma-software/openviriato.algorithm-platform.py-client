from CommunicationLayer import AlgorithmInterfaceCommunicationLayer


class AlgorithmicPlatformBaseClass:
    """
    Interface to the algorithmic platform of VIRIATO. A wrapper around the REST-API.
    Supports and is intended to be used in with statements
    """
    __communication_layer: AlgorithmInterfaceCommunicationLayer.CommunicationLayer

    def __init__(self, base_url: str):
        self.__communication_layer = AlgorithmInterfaceCommunicationLayer.CommunicationLayer(base_url)

    def __enter__(self):
        return self  # to be used in with statement

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__communication_layer.currentSession.close()

    @property
    def base_url(self) -> str:
        return self.__communication_layer.base_url
