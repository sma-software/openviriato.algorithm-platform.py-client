from typing import List

from py_client.aidm.aidm_base_classes import _HasID, _HasCode, _HasDebugString
from py_client.aidm.aidm_train_path_node_classes import AlgorithmTrainPathNode


class AlgorithmNodeTrack(_HasID, _HasCode, _HasDebugString):

    def __init__(self, id: int, code: str, debug_string: str):
        _HasID.__init__(self, id)
        _HasCode.__init__(self, code)
        _HasDebugString.__init__(self, debug_string)


class AlgorithmNode(_HasID, _HasCode, _HasDebugString):
    __node_tracks: [AlgorithmNodeTrack]

    def __init__(self, id: int, code: str, debug_string: str, node_tracks: List[AlgorithmNodeTrack] = []):
        _HasID.__init__(self, id)
        _HasCode.__init__(self, code)
        _HasDebugString.__init__(self, debug_string)
        self.__node_tracks = node_tracks

    @property
    def node_tracks(self) -> List[AlgorithmNodeTrack]:
        return self.__node_tracks


class AlgorithmSectionTrack(_HasID, _HasCode, _HasDebugString):
    __distance_units: int
    __section_code: str

    def __init__(self, id: int, code: str, debug_string: str, distance_units: int, section_code: str):
        _HasID.__init__(self, id)
        _HasCode.__init__(self, code)
        _HasDebugString.__init__(self, debug_string)
        self.__distance_units = distance_units
        self.__section_code = section_code

    @property
    def distance_units(self) -> int:
        return self.__distance_units

    @property
    def section_code(self) -> str:
        return self.__section_code


class AlgorithmTrain(_HasID, _HasCode, _HasDebugString):
    __train_path_nodes: List[AlgorithmTrainPathNode]

    def __init__(self, id: int, code: str, debug_string: str, train_path_nodes: List[AlgorithmTrainPathNode]):
        _HasID.__init__(self, id)
        _HasCode.__init__(self, code)
        _HasDebugString.__init__(self, debug_string)
        self.__train_path_nodes = train_path_nodes

    @property
    def train_path_nodes(self) -> List[AlgorithmTrainPathNode]:
        return self.__train_path_nodes


class AlgorithmFormation(_HasID, _HasDebugString):
    __places_first_class: int
    __places_second_class: int
    __vehicle_type_ids: List[int]

    def __init__(self,
                 id: int,
                 debug_string: str,
                 places_first_class: int,
                 places_second_class: int,
                 vehicle_type_ids: List[int]):
        _HasID.__init__(self, id)
        _HasDebugString.__init__(self, debug_string)
        self.__places_first_class = places_first_class
        self.__places_second_class = places_second_class
        self.__vehicle_type_ids = vehicle_type_ids

    @property
    def places_first_class(self) -> int:
        return self.__places_first_class

    @property
    def places_second_class(self) -> int:
        return self.__places_second_class

    @property
    def vehicle_type_ids(self) -> List[int]:
        return self.__vehicle_type_ids


class AlgorithmVehicleType(_HasID, _HasDebugString):
    __is_engine: bool
    __places_first_class: int
    __places_second_class: int

    def __init__(self, id: int, debug_string: str, is_engine: bool, places_first_class: int, places_second_class: int):
        _HasID.__init__(self, id)
        _HasDebugString.__init__(self, debug_string)
        self.__places_first_class = places_first_class
        self.__places_second_class = places_second_class
        self.__is_engine = is_engine

    @property
    def is_engine(self) -> bool:
        return self.__is_engine

    @property
    def places_first_class(self) -> int:
        return self.__places_first_class

    @property
    def places_second_class(self) -> int:
        return self.__places_second_class
