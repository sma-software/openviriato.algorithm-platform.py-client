from typing import List

from py_client.aidm.aidm_table_cell_classes import TableCellDataType, _TableCell


class TableColumnDefinition:
    __column_data_type: TableCellDataType
    __header: _TableCell
    __header_data_type: TableCellDataType
    __key: str

    def __init__(self,
                 key: str,
                 header: _TableCell,
                 header_data_type: TableCellDataType,
                 column_data_type: TableCellDataType):
        self.__key = key
        self.__header = header
        self.__column_data_type = column_data_type
        self.__header_data_type = header_data_type

    @property
    def column_data_type(self) -> TableCellDataType:
        return self.__column_data_type

    @property
    def header(self) -> _TableCell:
        return self.__header

    @property
    def header_data_type(self) -> TableCellDataType:
        return self.__header_data_type

    @property
    def key(self) -> str:
        return self.__key


class TableDefinition:
    __columns: List[TableColumnDefinition]
    __name: str

    def __init__(self, name: str, columns: List[TableColumnDefinition]):
        self.__name = name
        self.__columns = columns

    @property
    def name(self) -> str:
        return self.__name

    @property
    def columns(self) -> List[TableColumnDefinition]:
        return self.__columns


class TableRow:
    __cells: List[_TableCell]

    def __init__(self, cells: List[_TableCell]):
        self.__cells = cells

    @property
    def cells(self) -> List[_TableCell]:
        return self.__cells
