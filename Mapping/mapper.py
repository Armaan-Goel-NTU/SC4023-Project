from exceptions import MappingException


class Mapper:
    def mapped_size(self):
        pass

    def internal_map(self, value):
        pass

    def from_bytes(self, value):
        return int.from_bytes(value, byteorder="big")

    def to_bytes(self, value: int):
        return value.to_bytes(self.mapped_size(), byteorder="big")

    def map_value(self, value):
        try:
            mapped = self.internal_map(value)
        except Exception as e:
            raise MappingException(e)
        return mapped

    def unmap_value(self, value):
        pass
