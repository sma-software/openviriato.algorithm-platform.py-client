import AlgorithmStatic


class hasID:
    """
        items in SMA​Algorithm​PlatformAlgorithm​Interface​AIDM  which have an ID.
    """
    __ID: int

    def __init__(self, node_id: int):
        AlgorithmStatic.assert_parameter_is_int(node_id, 'node_id', '__init()__')
        self.__ID = node_id

    @property  # getter for ID
    def ID(self) -> int:
        return self.__ID


class hasCode:
    """

    """
    __Code: str

    def __init__(self, code_string: str):
        AlgorithmStatic.assert_parameter_is_str(code_string, 'code_string', '__init()__')
        self.__Code = code_string

    @property  # getter for Code
    def Code(self) -> str:
        return self.__Code


class hasDebugString:
    """

    """
    __DebugString: str

    def __init__(self, debug_string: str = None):
        if debug_string is not None:
            AlgorithmStatic.assert_parameter_is_str(debug_string, 'debug_string', '__init()__')
        self.__DebugString = debug_string

    @property  # getter for Code
    def DebugString(self):
        return self.__DebugString


class AlgorithmNode(hasID, hasCode, hasDebugString):
    __NodeTracks: []

    def __init__(self, node_id: int, code_string: str, debug_string: str, node_tracks: list):
        hasID.__init__(self, node_id)
        hasCode.__init__(self, code_string)
        hasDebugString.__init__(self, debug_string)
        self.__NodeTracks = node_tracks

    @property  # getter for NodeTracks
    def NodeTracks(self) -> list:
        return self.__NodeTracks


class AlgorithmSectionTrack(hasID, hasCode, hasDebugString):
    __Weight: int
    __SectionCode: str

    def __init__(self, section_id: int, code_string: str, debug_string: str, section_weight: int, section_code: str):
        hasID.__init__(self, section_id)
        hasCode.__init__(self, code_string)
        hasDebugString.__init__(self, debug_string)
        self.__Weight = section_weight
        self.__SectionCode = section_code

    @property  # getter for Weight
    def Weight(self) -> int:
        return self.__Weight

    @property  # getter for SectionCode
    def SectionCode(self) -> str:
        return self.__SectionCode
