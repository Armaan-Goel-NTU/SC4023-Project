import struct

from Mapping.mapper import Mapper
from exceptions import InvalidConversionException, InvalidMapException, DateOverflowException


class FloatMapper(Mapper):
    def mapped_size(self):
        return 4

    def internal_map(self, value):
        try:
            return float(value)
        except Exception:
            raise InvalidConversionException(f"{value} cannot be converted to a float.")

    def to_bytes(self, value: float):
        return struct.pack(">f", value)

    def from_bytes(self, value):
        return struct.unpack(">f", value)[0]

    def unmap_value(self, value):
        return str(value)

class CharMapper(Mapper):
    def __init__(self, size):
        self.size = size

    def mapped_size(self):
        return self.size

    def internal_map(self, value):
        if len(value) > self.size:
            raise InvalidMapException(f"{value} is longer than fixed size {self.size}")
        return value

    def to_bytes(self, value: str):
        return value.encode("ascii").ljust(self.mapped_size(), b"\x00")

    def from_bytes(self, value: bytes):
        return value.rstrip("\x00").decode("ascii")

    def from_bytes(self, value):
        return struct.unpack(">f", value)[0]

    def unmap_value(self, value):
        return value

class ShortMapper(Mapper):
    def mapped_size(self):
        return 2

    def internal_map(self, value):
        try:
            mapped = int(value)
        except Exception:
            raise InvalidConversionException(f"{value} cannot be converted to a short.")

        if mapped > 2 ** 16 - 1:
            raise DateOverflowException(f"{value} is too large for a short.")

        return mapped

    def unmap_value(self, value):
        return str(value)
