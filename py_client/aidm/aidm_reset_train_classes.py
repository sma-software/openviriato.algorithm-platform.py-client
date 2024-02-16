class ResetSummary:
    __number_of_deleted_links: int
    __number_of_reset_trains: int

    def __init__(self, number_of_deleted_links: int, number_of_reset_trains: int):
        self.__number_of_deleted_links = number_of_deleted_links
        self.__number_of_reset_trains = number_of_reset_trains

    @property
    def number_of_deleted_links(self) -> int:
        return self.__number_of_deleted_links

    @property
    def number_of_reset_trains(self) -> int:
        return self.__number_of_reset_trains
