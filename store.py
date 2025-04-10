from Mapping.mapper import MapException, Mapper


class StorageException(Exception):
    pass


class ColumnStore:

    def __init__(self, critical, mappings: list[Mapper]):
        self.critical = critical
        self.mappings = mappings

        if len(self.mappings) != 10:
            raise StorageException(f"Expected 10 mappings, got {len(self.mappings)}")

        self.month = []
        self.town = []
        self.flat_type = []
        self.block = []
        self.street_name = []
        self.storey_range = []
        self.floor_area_sqm = []
        self.flat_model = []
        self.lease_commence_date = []
        self.resale_price = []

    def add_entry(self, tokens):
        if len(tokens) != len(self.mappings):
            raise StorageException(
                f"Expected {self.mappings} tokens, got {len(tokens)}."
            )

        for pos in self.critical:
            if not tokens[pos]:
                raise StorageException(f"Expected attribute {pos} to be non-empty.")

        try:
            for i in range(len(tokens)):
                tokens[i] = self.mappings[i].map_value(tokens[i])
        except MapException as e:
            raise StorageException(str(e))

        self.month.append(tokens[0])
        self.town.append(tokens[1])
        self.flat_type.append(tokens[2])
        self.block.append(tokens[3])
        self.street_name.append(tokens[4])
        self.storey_range.append(tokens[5])
        self.floor_area_sqm.append(tokens[6])
        self.flat_model.append(tokens[7])
        self.lease_commence_date.append(tokens[8])
        self.resale_price.append(tokens[9])

    def get_size(self):
        return len(self.month)

    def get_month(self, pos):
        return self.month[pos]

    def get_town(self, pos):
        return self.town[pos]

    def get_floor_area_sqm(self, pos):
        return self.floor_area_sqm[pos]

    def get_resale_price(self, pos):
        return self.resale_price[pos]

    def unmap_town(self, index):
        return self.mappings[1].unmap_value(index)

    def unmap_month(self, month):
        return self.mappings[0].unmap_value(month)
