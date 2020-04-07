

class TrainClassification:
    __Description: str

    def __init__(self, Description: str):
        self.__Description = Description

    @property
    def Description(self) -> str:
        return self.__Description
