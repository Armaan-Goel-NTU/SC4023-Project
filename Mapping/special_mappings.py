import re

from Mapping.mapper import Mapper
from exceptions import InvalidDateException, DateOverflowException, InvalidBlockException


class MonthMapper(Mapper):
    def __init__(self):
        self.pattern = re.compile(r'[0-9]{4}-[0-9]{2}')

    def mapped_size(self):
        return 2

    def internal_map(self, value):
        if not re.match(self.pattern, value):
            raise InvalidDateException(f"{value} is not in the format YYYY-MM.")

        try:
            year = int(value[:4])
        except Exception:
            raise InvalidDateException(f"{value[:4]} is not a valid year.")

        try:
            month = int(value[-2:])
            if not (0 < month <= 12):
                raise Exception()
        except Exception:
            raise InvalidDateException(f"{value[-2:]} is not a valid month")

        mapped = year * 12 + (month - 1)
        if mapped > 2 ** 16 - 1:
            raise DateOverflowException(f"{value} is too big to fit into 2 bytes.")

        return mapped

    def unmap_value(self, value):
        month = value % 12 + 1
        year = value // 12
        return str(year).zfill(4) + "-" + str(month).zfill(2)

class BlockMapper(Mapper):
    def __init__(self):
        self.pattern = re.compile(r"[0-9]+[A-Z]?")

    def mapped_size(self):
        return 3
    
    def internal_map(self, value):
        if not re.match(self.pattern, value):
            raise InvalidBlockException(f"{value} should be a number followed by an optional uppercase letter.")

        result = 0
        if ord('A') <= ord(value[-1]) <= ord('Z'):
            result = ord(value[-1])
            value = value[:-1]

        result <<= 16
        block = int(value)

        if block > 2 ** 16 - 1:
            raise DateOverflowException(f"{block} too big to fit into 2 bytes.")

        result += int(value)
        return result

    def unmap_value(self, value):
        block = str(value & 0xFFFF)
        letter = value >> 16
        if letter != 0:
            block += chr(letter)
        
        return block
