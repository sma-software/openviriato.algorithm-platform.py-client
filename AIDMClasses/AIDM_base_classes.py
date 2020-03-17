from void import AlgorithmTypeCheck


class IhasID:
    __ID: int

    def __init__(self, ID: int):
        self.__ID = ID

    @property
    def ID(self) -> int:
        return self.__ID


class IhasCode:
    __Code: str

    def __init__(self, Code: str):
        self.__Code = Code

    @property
    def Code(self) -> str:
        return self.__Code


class IhasDebugString:
    __DebugString: (str, None)

    def __init__(self, DebugString: (str, None) = None):
        if DebugString is not None:
            self.__DebugString = DebugString

    @property
    def DebugString(self) -> (str, None):
        return self.__DebugString


class IUpdateTrain:
    __TrainID: int

    def __init__(self, TrainID):
        self.__TrainID = TrainID

    @property
    def TrainID(self) -> int:
        return self.__TrainID


class IRoutingEdge:
    __NodeID: int

    def __init__(self, NodeID):
        self.__NodeID = NodeID

    @property
    def NodeID(self) -> int:
        return self.__NodeID