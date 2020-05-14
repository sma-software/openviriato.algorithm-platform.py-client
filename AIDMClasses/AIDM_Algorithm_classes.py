from AIDMClasses.AIDM_base_classes import HasID, HasCode, HasDebugString
from AIDMClasses.AIDM_TrainPathNode_classes import AlgorithmTrainPathNode
from typing import List


class AlgorithmNodeTrack(HasID, HasCode, HasDebugString):

    def __init__(self, ID: int, Code: str, DebugString: str):
        HasID.__init__(self, ID)
        HasCode.__init__(self, Code)
        HasDebugString.__init__(self, DebugString)


class AlgorithmNode(HasID, HasCode, HasDebugString):
    __NodeTracks: [AlgorithmNodeTrack]

    def __init__(self, ID: int, Code: str, DebugString: str, NodeTracks: List[AlgorithmNodeTrack] = []):
        HasID.__init__(self, ID)
        HasCode.__init__(self, Code)
        HasDebugString.__init__(self, DebugString)
        self.__NodeTracks = NodeTracks

    @property
    def NodeTracks(self) -> List[AlgorithmNodeTrack]:
        return self.__NodeTracks


class AlgorithmSectionTrack(HasID, HasCode, HasDebugString):
    __Weight: int
    __SectionCode: str

    def __init__(self, ID: int, Code: str, DebugString: str, Weight: int, SectionCode: str):
        HasID.__init__(self, ID)
        HasCode.__init__(self, Code)
        HasDebugString.__init__(self, DebugString)
        self.__Weight = Weight
        self.__SectionCode = SectionCode

    @property
    def Weight(self) -> int:
        return self.__Weight

    @property
    def SectionCode(self) -> str:
        return self.__SectionCode


class AlgorithmTrain(HasID, HasDebugString):
    __trainPathNodes: List[AlgorithmTrainPathNode]

    def __init__(self, ID: int, DebugString: str, TrainPathNodes: List[AlgorithmTrainPathNode]):
        HasID.__init__(self, ID)
        HasDebugString.__init__(self, DebugString)
        self.__TrainPathNodes = TrainPathNodes

    @property
    def TrainPathNodes(self) -> List[AlgorithmTrainPathNode]:
        return self.__TrainPathNodes


class AlgorithmFormation(HasID, HasDebugString):
    __VehicleTypeIDs: List[int]

    def __init__(self, ID: int, DebugString: str, VehicleTypeIDs: List[int]):
        HasID.__init__(self, ID)
        HasDebugString.__init__(self, DebugString)
        self.__VehicleTypeIDs = VehicleTypeIDs

    @property
    def VehicleTypeIDs(self) -> List[int]:
        return self.__VehicleTypeIDs


class AlgorithmVehicleType(HasID, HasDebugString):
    __IsEngine: bool

    def __init__(self, ID: int, DebugString: str, IsEngine: bool):
        HasID.__init__(self, ID)
        HasDebugString.__init__(self, DebugString)
        self.__IsEngine = IsEngine

    @property
    def IsEngine(self) -> bool:
        return self.__IsEngine