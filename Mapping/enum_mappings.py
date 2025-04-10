from Mapping.mapper import Mapper

class EnumMapper(Mapper):
    def __init__(self, values):
        self.map = {}
        self.values = values
        for i in range(len(values)):
            self.map[values[i]] = i
        
    
    def mapped_size(self):
        return len(self.map).bit_length()
    
    def internal_map(self, value):
        if value not in self.map:
            return 0, f"{value} is not present in the mappings for {self.__class__.__name__}"
        return self.map[value], None
    
    def unmap_value(self, value):
        return self.values[value]

class TownMapper(EnumMapper):
    pass

class FlatTypeMapper(EnumMapper):
    pass

class FlatModelMapper(EnumMapper):
    pass

class StoreyRangeMapper(EnumMapper):
    pass