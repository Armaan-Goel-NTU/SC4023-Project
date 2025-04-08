# Mapping from integer ID to string representation of flat model.
# There are 21 unique flat model in 'ResalePricesSingapore.csv'.
# These can be represented using 5 bits.
# Can be used for querying flat_model in the future.
flat_model_mapping_id = {
    0: "2-room",
    1: "3Gen",
    2: "Adjoined flat",
    3: "Apartment",
    4: "DBSS",
    5: "Improved",
    6: "Improved-Maisonette",
    7: "Maisonette",
    8: "Model A",
    9: "Model A2",
    10: "Model A-Maisonette",
    11: "Multi Generation",
    12: "New Generation",
    13: "Premium Apartment",
    14: "Premium Apartment Loft",
    15: "Premium Maisonette",
    16: "Simplified",
    17: "Standard",
    18: "Terrace",
    19: "Type S1",
    20: "Type S2"
}

# Reverse mapping from string representation to integer ID.
# For space optimisation.
flat_model_mapping_string = {v: k for k, v in flat_model_mapping_id.items()}
