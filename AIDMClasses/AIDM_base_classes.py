from void import AlgorithmTypeCheck


class IhasID:
    __ID: int

    def __init__(self, element_id: int):
        AlgorithmTypeCheck.assert_parameter_is_int(element_id, 'element_id', '__init()__')
        self.__ID = element_id

    @property
    def ID(self) -> int:
        return self.__ID


class IhasCode:
    __Code: str

    def __init__(self, code_string: str):
        AlgorithmTypeCheck.assert_parameter_is_str(code_string, 'code_string', '__init()__')
        self.__Code = code_string

    @property
    def Code(self) -> str:
        return self.__Code


class IhasDebugString:
    __DebugString: str

    def __init__(self, debug_string: str = None):
        if debug_string is not None:
            AlgorithmTypeCheck.assert_parameter_is_str(debug_string, 'debug_string', '__init()__')
        self.__DebugString = debug_string

    @property
    def DebugString(self):
        return self.__DebugString