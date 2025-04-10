from enum import Enum

# Enum storey range.
# There are 17 unique storey ranges in 'ResalePricesSingapore.csv'.
# These can be represented using 5 bits.
class StoreyRange(Enum):
    STOREY_01_TO_03 = "01 TO 03"
    STOREY_04_TO_06 = "04 TO 06"
    STOREY_07_TO_09 = "07 TO 09"
    STOREY_10_TO_12 = "10 TO 12"
    STOREY_13_TO_15 = "13 TO 15"
    STOREY_16_TO_18 = "16 TO 18"
    STOREY_19_TO_21 = "19 TO 21"
    STOREY_22_TO_24 = "22 TO 24"
    STOREY_25_TO_27 = "25 TO 27"
    STOREY_28_TO_30 = "28 TO 30"
    STOREY_31_TO_33 = "31 TO 33"
    STOREY_34_TO_36 = "34 TO 36"
    STOREY_37_TO_39 = "37 TO 39"
    STOREY_40_TO_42 = "40 TO 42"
    STOREY_43_TO_45 = "43 TO 45"
    STOREY_46_TO_48 = "46 TO 48"
    STOREY_49_TO_51 = "49 TO 51"

    # Get storey_range using index, used for querying.
    @classmethod
    def get_storey_range_by_index(cls, index: int) -> str:
        return list(cls)[index].value

    # Get index using storey_range, used for storing.
    @classmethod
    def get_index_by_storey_range(cls, storey_range: str) -> int:
        return list(cls).index(cls(storey_range))
