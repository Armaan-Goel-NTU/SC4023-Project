class LengthException(Exception):
    pass

class EmptyException(Exception):
    pass

class ColumnStore():
    def __init__(self):
        self.critical = [0, 1, 6, 9]

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
        if len(tokens) != 10:
            raise LengthException(f"Expected 10 tokens, got {len(tokens)}.")

        for pos in self.critical:
            if not tokens[pos]:
                raise EmptyException(f"Expected attribute {pos} to be non-empty.")

        self.month.append(tokens[0])
        self.town.append(tokens[1])
        self.flat_type.append(tokens[2])
        self.block.append(tokens[3])
        self.street_name.append(tokens[4])
        self.storey_range.append(tokens[5])
        self.floor_area_sqm.append(float(tokens[6]))
        self.flat_model.append(tokens[7])
        self.lease_commence_date.append(tokens[8])
        self.resale_price.append(float(tokens[9]))
    
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
    


        