from Mapping.mapper import Mapper
import math

from exceptions import InvalidMapException


class EnumMapper(Mapper):
    """Maps string values to unique integer indices based on a fixed list of allowed values."""
    def __init__(self, values: list[str]):
        self.map = {}
        self.values = values
        for i in range(len(values)):
            self.map[values[i]] = i

    def mapped_size(self) -> int:
        return int(math.ceil(len(self.map).bit_length() / 8.0))

    def internal_map(self, value: str) -> int:
        if value not in self.map:
            raise InvalidMapException(f"{value} is not present in the mappings for {self.__class__.__name__}")
        return self.map[value]

    def unmap_value(self, value: int) -> str:
        return self.values[value]


class TownMapper(EnumMapper):
    """EnumMapper for mapping town."""
    pass

class FlatTypeMapper(EnumMapper):
    """EnumMapper for mapping flat_type."""
    pass

class FlatModelMapper(EnumMapper):
    """EnumMapper for mapping flat_model."""
    pass

class StoreyRangeMapper(EnumMapper):
    """EnumMapper for mapping storey_range."""
    pass
