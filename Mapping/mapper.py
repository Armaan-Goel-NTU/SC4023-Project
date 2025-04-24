from exceptions import MappingException


class Mapper:
    """Base class for all mappers. Handles byte-level serialization and deserialization."""
    def mapped_size(self) -> int:
        pass

    def internal_map(self, value: str) -> int:
        pass

    def from_bytes(self, value: bytes) -> int:
        return int.from_bytes(value, byteorder="big")

    def to_bytes(self, value: int) -> bytes:
        return value.to_bytes(self.mapped_size(), byteorder="big")

    def map_value(self, value: str) -> int:
        try:
            mapped = self.internal_map(value)
        except Exception as e:
            raise MappingException(e)
        return mapped

    def unmap_value(self, value: int):
        pass
