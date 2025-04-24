import struct

from Mapping.mapper import Mapper
from exceptions import InvalidConversionException, InvalidMapException, DataOverflowException

class FloatMapper(Mapper):
    """Maps float values into 4-byte float representation."""
    def mapped_size(self) -> int:
        return 4

    def internal_map(self, value: str) -> float:
        try:
            return float(value)
        except Exception:
            raise InvalidConversionException(f"{value} cannot be converted to a float.")

    def to_bytes(self, value: float) -> bytes:
        return struct.pack(">f", value)

    def from_bytes(self, value: bytes) -> float:
        return struct.unpack(">f", value)[0]

    def unmap_value(self, value: float) -> str:
        return str(value)


class CharMapper(Mapper):
    """Maps strings to a fixed-size ASCII representation padded with null bytes."""
    def __init__(self, size: int):
        self.size = size

    def mapped_size(self) -> int:
        return self.size

    def internal_map(self, value: str) -> str:
        if len(value) > self.size:
            raise InvalidMapException(f"{value} is longer than fixed size {self.size}")
        return value

    def to_bytes(self, value: str) -> bytes:
        return value.encode("ascii").ljust(self.mapped_size(), b"\x00")

    def from_bytes(self, value: bytes) -> str:
        return value.rstrip("\x00").decode("ascii")

    def unmap_value(self, value: str) -> str:
        return value


class ShortMapper(Mapper):
    """Maps integers into 2-byte unsigned short representation."""
    def mapped_size(self) -> int:
        return 2

    def internal_map(self, value: str) -> int:
        try:
            mapped = int(value)
        except Exception:
            raise InvalidConversionException(f"{value} cannot be converted to a short.")

        if mapped > 2 ** 16 - 1:
            raise DataOverflowException(f"{value} is too large for a short.")

        return mapped

    def unmap_value(self, value: int) -> str:
        return str(value)
