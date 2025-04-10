from enum import Enum

# Enum flat type.
# There are 7 unique flat type in 'ResalePricesSingapore.csv'.
# These can be represented using 3 bits.
class FlatType(Enum):
    ONE_ROOM = "1 ROOM"
    TWO_ROOM = "2 ROOM"
    THREE_ROOM = "3 ROOM"
    FOUR_ROOM = "4 ROOM"
    FIVE_ROOM = "5 ROOM"
    EXECUTIVE = "EXECUTIVE"
    MULTI_GENERATION = "MULTI-GENERATION"

    # Get flat type using index, used for querying.
    @classmethod
    def get_flat_type_by_index(cls, index: int) -> str:
        return list(cls)[index].value

    # Get index using flat type, used for storing.
    @classmethod
    def get_index_by_flat_type(cls, flat_type: str) -> int:
        return list(cls).index(cls(flat_type))
