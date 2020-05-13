from AIDMClasses.AIDM_base_classes import IhasID, IhasCode, IhasDebugString
from AIDMClasses.AIDM_TrainPathNode_classes import TrainPathNode
from typing import List


class AlgorithmNodeTrack(IhasID, IhasCode, IhasDebugString):

    def __init__(self, ID: int, Code: str, DebugString: str):
        IhasID.__init__(self, ID)
        IhasCode.__init__(self, Code)
        IhasDebugString.__init__(self, DebugString)


class AlgorithmNode(IhasID, IhasCode, IhasDebugString):
    __NodeTracks: [AlgorithmNodeTrack]

    def __init__(self, ID: int, Code: str, DebugString: str, NodeTracks: List[AlgorithmNodeTrack] = []):
        IhasID.__init__(self, ID)
        IhasCode.__init__(self, Code)
        IhasDebugString.__init__(self, DebugString)
        self.__NodeTracks = NodeTracks

    @property
    def NodeTracks(self) -> List[AlgorithmNodeTrack]:
        return self.__NodeTracks


class AlgorithmSectionTrack(IhasID, IhasCode, IhasDebugString):
    __Weight: int
    __SectionCode: str

    def __init__(self, ID: int, Code: str, DebugString: str, Weight: int, SectionCode: str):
        IhasID.__init__(self, ID)
        IhasCode.__init__(self, Code)
        IhasDebugString.__init__(self, DebugString)
        self.__Weight = Weight
        self.__SectionCode = SectionCode

    @property
    def Weight(self) -> int:
        return self.__Weight

    @property
    def SectionCode(self) -> str:
        return self.__SectionCode


class AlgorithmTrain(IhasID, IhasDebugString):
    __trainPathNodes: List[TrainPathNode]

    def __init__(self, ID: int, DebugString: str, TrainPathNodes: List[TrainPathNode]):
        IhasID.__init__(self, ID)
        IhasDebugString.__init__(self, DebugString)
        self.__TrainPathNodes = TrainPathNodes

    @property
    def TrainPathNodes(self) -> List[TrainPathNode]:
        return self.__TrainPathNodes


class AlgorithmFormation(IhasID, IhasDebugString):
    __VehicleTypeIDs: List[int]

    def __init__(self, ID: int, DebugString: str, VehicleTypeIDs: List[int]):
        IhasID.__init__(self, ID)
        IhasDebugString.__init__(self, DebugString)
        self.__VehicleTypeIDs = VehicleTypeIDs

    @property
    def VehicleTypeIDs(self) -> List[int]:
        return self.__VehicleTypeIDs


class AlgorithmVehicleType(IhasID, IhasDebugString):
    __IsEngine: bool

    def __init__(self, ID: int, DebugString: str, IsEngine: bool):
        IhasID.__init__(self, ID)
        IhasDebugString.__init__(self, DebugString)
        self.__IsEngine = IsEngine

    @property
    def IsEngine(self) -> bool:
        return self.__IsEngine