from enum import Enum

# Enum flat model.
# There are 21 unique flat model in 'ResalePricesSingapore.csv'.
# These can be represented using 5 bits.
class FlatModel(Enum):
    TWO_ROOM = "2-room"
    THREE_GEN = "3Gen"
    ADJOINED_FLAT = "Adjoined flat"
    APARTMENT = "Apartment"
    DBSS = "DBSS"
    IMPROVED = "Improved"
    IMPROVED_MAISONETTE = "Improved-Maisonette"
    MAISONETTE = "Maisonette"
    MODEL_A = "Model A"
    MODEL_A2 = "Model A2"
    MODEL_A_MAISONETTE = "Model A-Maisonette"
    MULTI_GENERATION = "Multi Generation"
    NEW_GENERATION = "New Generation"
    PREMIUM_APARTMENT = "Premium Apartment"
    PREMIUM_APARTMENT_LOFT = "Premium Apartment Loft"
    PREMIUM_MAISONETTE = "Premium Maisonette"
    SIMPLIFIED = "Simplified"
    STANDARD = "Standard"
    TERRACE = "Terrace"
    TYPE_S1 = "Type S1"
    TYPE_S2 = "Type S2"

    # Get flat model using index, used for querying.
    @classmethod
    def get_flat_model_by_index(cls, index: int) -> str:
        return list(cls)[index].value

    # Get index using flat model, used for storing.
    @classmethod
    def get_index_by_flat_model(cls, flat_model: str) -> int:
        return list(cls).index(cls(flat_model))
