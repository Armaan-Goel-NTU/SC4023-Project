# Mapping from integer ID to string representation of storey range.
# There are 17 unique storey ranges in 'ResalePricesSingapore.csv'.
# These can be represented using 5 bits.
# Can be used for querying storey_range in the future.
storey_range_mapping_id = {
    0: "01 TO 03",
    1: "04 TO 06",
    2: "07 TO 09",
    3: "10 TO 12",
    4: "13 TO 15",
    5: "16 TO 18",
    6: "19 TO 21",
    7: "22 TO 24",
    8: "25 TO 27",
    9: "28 TO 30",
    10: "31 TO 33",
    11: "34 TO 36",
    12: "37 TO 39",
    13: "40 TO 42",
    14: "43 TO 45",
    15: "46 TO 48",
    16: "49 TO 51"
}

# Reverse mapping from string representation to integer ID.
# For space optimisation.
storey_range_mapping_string = {v: k for k, v in storey_range_mapping_id.items()}
