

class AlgorithmTrainClassification:
    __description: str

    def __init__(self, description: str):
        self.__description = description

    @property
    def description(self) -> str:
        return self.__description
