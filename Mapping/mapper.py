class MapException(Exception):
    pass

class Mapper:
    def mapped_size(self):
        pass
    
    def internal_map(self, value):
        pass

    def map_value(self, value):
        mapped, reason = self.internal_map(value)
        if reason:
            raise MapException(reason)
        return mapped

    def unmap_value(self, value):
        pass