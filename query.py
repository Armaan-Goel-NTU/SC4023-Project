import math

from store import ColumnStore

class QueryHelper():
    def __init__(self, store: ColumnStore):
        self.store = store
        self.clear_results()
    
    def get_results(self):
        return "\n".join(self.results)

    def clear_results(self):
        self.results = ["Year,Month,town,Category,Value"]
    
    def add_result(self, year, month, town, category, value):
        year = str(year).zfill(4)
        month = str(month).zfill(2)
        value = str(round(value, 2))
        self.results.append(",".join([year, month, town, category, value]))
    
    def minimum_price(self, year, month1, month2, town):
        pos2 = []
        for pos in range(self.store.get_size()):
            month = self.store.get_month(pos)
            y = int(month[:4])
            m = int(month[-2:])
            if y == year and m >= month1 and m <= month2:
                pos2.append(pos)
        
        pos3 = []
        for pos in pos2:
            t = self.store.get_town(pos)
            if t == town:
                pos3.append(pos)
            
        pos4 = []
        for pos in pos3:
            sqm = self.store.get_floor_area_sqm(pos)
            if sqm >= 80:
                pos4.append(pos)
        
        if len(pos4) == 0:
            self.add_result(year, month1, town, "Minimum Price", "No result")
            return

        min_price = math.inf
        for pos in pos4:
            price = self.store.get_resale_price(pos)
            if price < min_price:
                min_price = price
        
        self.add_result(year, month1, town, "Minimum Price", min_price)
    
    def average_price(self, year, month1, month2, town):
        pos2 = []
        for pos in range(self.store.get_size()):
            month = self.store.get_month(pos)
            y = int(month[:4])
            m = int(month[-2:])
            if y == year and m >= month1 and m <= month2:
                pos2.append(pos)
        
        pos3 = []
        for pos in pos2:
            t = self.store.get_town(pos)
            if t == town:
                pos3.append(pos)
            
        pos4 = []
        for pos in pos3:
            sqm = self.store.get_floor_area_sqm(pos)
            if sqm >= 80:
                pos4.append(pos)
        
        if len(pos4) == 0:
            self.add_result(year, month1, town, "Average Price", "No result")
            return
        
        total_price = 0
        for pos in pos4:
            price = self.store.get_resale_price(pos)
            total_price += price
        
        self.add_result(year, month1, town, "Average Price", total_price/len(pos4))
    """
    def stddev_price(self, year, month1, month2, town):
        pos2 = []
        for pos in range(self.store.get_size()):
            month = self.store.get_month(pos)
            y = int(month[:4])
            m = int(month[-2:])
            if y == year and m >= month1 and m <= month2:
                pos2.append(pos)
        
        pos3 = []
        for pos in pos2:
            t = self.store.get_town(pos)
            if t == town:
                pos3.append(pos)
            
        pos4 = []
        for pos in pos3:
            sqm = self.store.get_floor_area_sqm(pos)
            if sqm >= 80:
                pos4.append(pos)
        
        if len(pos4) == 0:
            self.add_result(year, month1, town, "Standard Deviation of Price", "No result")
            return
        
        total_price = 0
        for pos in pos4:
            price = self.store.get_resale_price(pos)
            total_price += price

        n = len(pos4)
        average = total_price/n

        stddev = 0
        for pos in pos4:
            price = self.store.get_resale_price(pos)
            stddev += (price - average) ** 2
        
        stddev /= n
        stddev = math.sqrt(stddev)

        self.add_result(year, month1, town, "Standard Deviation of Price", stddev)
    """
    def stddev_price(self, year, month1, month2, town):
        """
        Calculation of standard deviation using single reference to pos4 instead of 2 passes of avg then stddev.
        Credits: https://jonisalonen.com/2013/deriving-welfords-method-for-computing-variance/
        """
        pos2 = []
        for pos in range(self.store.get_size()):
            month = self.store.get_month(pos)
            y = int(month[:4])
            m = int(month[-2:])
            if y == year and m >= month1 and m <= month2:
                pos2.append(pos)
        
        pos3 = []
        for pos in pos2:
            t = self.store.get_town(pos)
            if t == town:
                pos3.append(pos)
            
        pos4 = []
        for pos in pos3:
            sqm = self.store.get_floor_area_sqm(pos)
            if sqm >= 80:
                pos4.append(pos)
        
        if len(pos4) == 0:
            self.add_result(year, month1, town, "Standard Deviation of Price", "No result")
            return
        
        # Welford's Algorithm
        count = 0
        average = 0
        ssd = 0  
        for pos in pos4:
            count += 1
            price = self.store.get_resale_price(pos)
            diff = price - average
            average += diff
            updated_diff = price - average
            ssd = diff * updated_diff

        n = len(pos4)
        stddev = math.sqrt(ssd/n)

        self.add_result(year, month1, town, "Standard Deviation of Price", stddev)

    def minimum_price_per_sqm(self, year, month1, month2, town):
        pos2 = []
        for pos in range(self.store.get_size()):
            month = self.store.get_month(pos)
            y = int(month[:4])
            m = int(month[-2:])
            if y == year and m >= month1 and m <= month2:
                pos2.append(pos)
        
        pos3 = []
        for pos in pos2:
            t = self.store.get_town(pos)
            if t == town:
                pos3.append(pos)
            
        pos4 = []
        for pos in pos3:
            sqm = self.store.get_floor_area_sqm(pos)
            if sqm >= 80:
                pos4.append(pos)
        
        if len(pos4) == 0:
            self.add_result(year, month1, town, "Minimum Price per Square Meter", "No result")
            return
        
        min_price_per_sqm = math.inf
        for pos in pos4:
            price = self.store.get_resale_price(pos)
            sqm = self.store.get_floor_area_sqm(pos)
            price_per_sqm = price / sqm
            if price_per_sqm < min_price_per_sqm:
                min_price_per_sqm = price_per_sqm

        self.add_result(year, month1, town, "Minimum Price per Square Meter", min_price_per_sqm)
    
    def shared_scan(self, year, month1, month2, town):
        pos2 = []
        for pos in range(self.store.get_size()):
            month = self.store.get_month(pos)
            y = int(month[:4])
            m = int(month[-2:])
            if y == year and m >= month1 and m <= month2:
                pos2.append(pos)
        
        pos3 = []
        for pos in pos2:
            t = self.store.get_town(pos)
            if t == town:
                pos3.append(pos)
            
        pos4 = []
        for pos in pos3:
            sqm = self.store.get_floor_area_sqm(pos)
            if sqm >= 80:
                pos4.append(pos)
        
        if len(pos4) == 0:
            self.add_result(year, month1, town, "Minimum Price", "No result")
            self.add_result(year, month1, town, "Standard Deviation of Price", "No result")
            self.add_result(year, month1, town, "Average Price", "No result")
            self.add_result(year, month1, town, "Minimum Price per Square Meter", "No result")
            return

        min_price = math.inf
        min_price_per_sqm = math.inf
        total_price = 0
        for pos in pos4:
            price = self.store.get_resale_price(pos)
            total_price += price
            if price < min_price:
                min_price = price
            sqm = self.store.get_floor_area_sqm(pos)
            price_per_sqm = price / sqm
            if price_per_sqm < min_price_per_sqm:
                min_price_per_sqm = price_per_sqm

        # Welford's Algorithm
        count = 0
        average = 0
        total_price = 0
        ssd = 0  
        for pos in pos4:
            count += 1
            price = self.store.get_resale_price(pos)
            total_price += price
            diff = price - average
            average += diff
            updated_diff = price - average
            ssd = diff * updated_diff

        n = len(pos4)
        stddev = math.sqrt(ssd/n)
        average_price = total_price/n

        self.add_result(year, month1, town, "Minimum Price", min_price)
        self.add_result(year, month1, town, "Average Price", average_price)
        self.add_result(year, month1, town, "Standard Deviation of Price", stddev)
        self.add_result(year, month1, town, "Minimum Price per Square Meter", min_price_per_sqm)





