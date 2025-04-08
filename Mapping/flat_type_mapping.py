# Mapping from integer ID to string representation of flat type.
# There are 7 unique flat types in 'ResalePricesSingapore.csv'.
# These can be represented using 3 bits.
# Can be used for querying flat_type in the future.
flat_type_mapping_id = {
    0: "1 ROOM",
    1: "2 ROOM",
    2: "3 ROOM",
    3: "4 ROOM",
    4: "5 ROOM",
    5: "EXECUTIVE",
    6: "MULTI-GENERATION"
}

# Reverse mapping from string representation to integer ID.
# For space optimisation.
flat_type_mapping_string = {v: k for k, v in flat_type_mapping_id.items()}
