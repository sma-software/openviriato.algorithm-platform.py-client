from AIDMClasses.AIDM_base_classes import HasID, HasCode, HasDebugString
from AIDMClasses.AIDM_TrainPathNode_classes import AlgorithmTrainPathNode
from typing import List


class AlgorithmNodeTrack(HasID, HasCode, HasDebugString):

    def __init__(self, id: int, code: str, debug_string: str):
        HasID.__init__(self, id)
        HasCode.__init__(self, code)
        HasDebugString.__init__(self, debug_string)


class AlgorithmNode(HasID, HasCode, HasDebugString):
    __node_tracks: [AlgorithmNodeTrack]

    def __init__(self, id: int, code: str, debug_string: str, node_tracks: List[AlgorithmNodeTrack] = []):
        HasID.__init__(self, id)
        HasCode.__init__(self, code)
        HasDebugString.__init__(self, debug_string)
        self.__node_tracks = node_tracks

    @property
    def node_tracks(self) -> List[AlgorithmNodeTrack]:
        return self.__node_tracks


class AlgorithmSectionTrack(HasID, HasCode, HasDebugString):
    __weight: int
    __section_code: str

    def __init__(self, id: int, code: str, debug_string: str, weight: int, section_code: str):
        HasID.__init__(self, id)
        HasCode.__init__(self, code)
        HasDebugString.__init__(self, debug_string)
        self.__weight = weight
        self.__section_code = section_code

    @property
    def weight(self) -> int:
        return self.__weight

    @property
    def section_code(self) -> str:
        return self.__section_code


class AlgorithmTrain(HasID, HasDebugString):
    __train_path_nodes: List[AlgorithmTrainPathNode]

    def __init__(self, id: int, debug_string: str, train_path_nodes: List[AlgorithmTrainPathNode]):
        HasID.__init__(self, id)
        HasDebugString.__init__(self, debug_string)
        self.__train_path_nodes = train_path_nodes

    @property
    def train_path_nodes(self) -> List[AlgorithmTrainPathNode]:
        return self.__train_path_nodes


class AlgorithmFormation(HasID, HasDebugString):
    __vehicle_type_ids: List[int]

    def __init__(self, id: int, debug_string: str, vehicle_type_ids: List[int]):
        HasID.__init__(self, id)
        HasDebugString.__init__(self, debug_string)
        self.__vehicle_type_ids = vehicle_type_ids

    @property
    def vehicle_type_ids(self) -> List[int]:
        return self.__vehicle_type_ids


class AlgorithmVehicleType(HasID, HasDebugString):
    __is_engine: bool

    def __init__(self, id: int, debug_string: str, is_engine: bool):
        HasID.__init__(self, id)
        HasDebugString.__init__(self, debug_string)
        self.__is_engine = is_engine

    @property
    def is_engine(self) -> bool:
        return self.__is_engine