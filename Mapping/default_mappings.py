from Mapping.mapper import Mapper

class FloatMapper(Mapper):
    def mapped_size(self):
        return 4

    def internal_map(self, value):
        try:
            return float(value), None
        except Exception as e:
            return 0, f"{value} cannot be converted to a float."
    
    def unmap_value(self, value):
        return str(value)

class CharMapper(Mapper):
    def __init__(self, size):
        self.size = size

    def mapped_size(self):
        return self.size
    
    def internal_map(self, value):
        if len(value) > self.size:
            return "", f"{value} is longer than fixed size {self.size}"
        return value, None
    
    def unmap_value(self, value):
        return value

class ShortMapper(Mapper):
    def mapped_size(self):
        return 2
    
    def internal_map(self, value):
        mapped = 0
        try:
            mapped = int(value)
        except Exception as e:
            return 0, f"{value} cannot be converted to a short."
        
        if mapped > 2 ** 16 - 1:
            return 0, f"{value} is too large for a short."
        
        return value, None
    
    def unmap_value(self, value):
        return str(value)


        
    

        
