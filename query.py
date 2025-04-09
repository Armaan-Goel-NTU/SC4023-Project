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
    
    """
    def minimum_price(self, year, month1, month2, town, vector_range=[]):
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
    """

    def minimum_price(self, year, month1, month2, town, vector_range=[]):
        pos2 = []

        if vector_range:
            start_idx, stop_idx = vector_range
            for pos in range(start_idx, stop_idx):
                month = self.store.get_month(pos)
                y = int(month[:4])
                m = int(month[-2:])
                if y == year and m >= month1 and m <= month2:
                    pos2.append(pos)
        else:
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
        
        if len(pos4) == 0 and vector_range == []:
            self.add_result(year, month1, town, "Minimum Price", "No result")
            return
        
        if vector_range:
            return pos4

        min_price = math.inf
        for pos in pos4:
            price = self.store.get_resale_price(pos)
            if price < min_price:
                min_price = price
        
        self.add_result(year, month1, town, "Minimum Price", min_price)
    
    """
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

    def average_price(self, year, month1, month2, town, vector_range=[]):
        pos2 = []

        if vector_range != []:
            start_idx, stop_idx = vector_range
            for pos in range(start_idx, stop_idx):
                month = self.store.get_month(pos)
                y = int(month[:4])
                m = int(month[-2:])
                if y == year and m >= month1 and m <= month2:
                    pos2.append(pos)
        else:
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
        
        if len(pos4) == 0 and vector_range == []:
            self.add_result(year, month1, town, "Average Price", "No result")
            return

        if vector_range:
            return pos4
        
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

    def stddev_price(self, year, month1, month2, town, vector_range=[]):
        """
        Calculation of standard deviation using single reference to pos4 instead of 2 passes of avg then stddev.
        Credits: https://jonisalonen.com/2013/deriving-welfords-method-for-computing-variance/
        """

        pos2 = []

        if vector_range != []:
            start_idx, stop_idx = vector_range
            for pos in range(start_idx, stop_idx):
                month = self.store.get_month(pos)
                y = int(month[:4])
                m = int(month[-2:])
                if y == year and m >= month1 and m <= month2:
                    pos2.append(pos)
        else:
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
        
        if len(pos4) == 0 and vector_range == []:
            self.add_result(year, month1, town, "Standard Deviation of Price", "No result")
            return
        
        if vector_range:
            return pos4
        
        # Welford's Algorithm
        count = 0
        average = 0
        ssd = 0  
        for pos in pos4:
            count += 1
            price = self.store.get_resale_price(pos)
            diff = price - average
            average += diff/count
            updated_diff = price - average
            ssd += diff * updated_diff

        n = len(pos4)
        stddev = math.sqrt(ssd/n)

        self.add_result(year, month1, town, "Standard Deviation of Price", stddev)

    """
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
    """

    def minimum_price_per_sqm(self, year, month1, month2, town, vector_range=[]):
        pos2 = []

        if vector_range != []:
            start_idx, stop_idx = vector_range
            for pos in range(start_idx, stop_idx):
                month = self.store.get_month(pos)
                y = int(month[:4])
                m = int(month[-2:])
                if y == year and m >= month1 and m <= month2:
                    pos2.append(pos)
        else:
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
        
        if len(pos4) == 0 and vector_range == []:
            self.add_result(year, month1, town, "Minimum Price per Square Meter", "No result")
            return
        
        if vector_range:
            return pos4
        
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

        count = 0
        average = 0
        ssd = 0  
        for pos in pos4:
            count += 1
            price = self.store.get_resale_price(pos)
            total_price += price
            if price < min_price:
                min_price = price
            sqm = self.store.get_floor_area_sqm(pos)
            price_per_sqm = price / sqm
            if price_per_sqm < min_price_per_sqm:
                min_price_per_sqm = price_per_sqm

            # Welford's Algorithm
            diff = price - average
            average += diff/count
            updated_diff = price - average
            ssd += diff * updated_diff

        n = len(pos4)
        stddev = math.sqrt(ssd/n)
        average_price = total_price/n

        self.add_result(year, month1, town, "Minimum Price", min_price)
        self.add_result(year, month1, town, "Average Price", average_price)
        self.add_result(year, month1, town, "Standard Deviation of Price", stddev)
        self.add_result(year, month1, town, "Minimum Price per Square Meter", min_price_per_sqm)


    def vector_a_time(self, year, month1, month2, town, vector_size = 5000):
        list_of_pos4 = [[], [], [], []]  #[min, avg, stddev, minpsqm]
        store_size = self.store.get_size()

        for vector_start in range(0, store_size, vector_size):
            if vector_start+vector_size < store_size:
                min_pos4 = self.minimum_price(year, month1, month2, town, [vector_start, vector_start+vector_size])
                avg_pos4 = self.average_price(year, month1, month2, town, [vector_start, vector_start+vector_size])
                stddev_pos4 = self.stddev_price(year, month1, month2, town, [vector_start, vector_start+vector_size])
                minpsqm_pos4 = self.minimum_price_per_sqm(year, month1, month2, town, [vector_start, vector_start+vector_size])
            else:
                min_pos4 = self.minimum_price(year, month1, month2, town, [vector_start, store_size-1])
                avg_pos4 = self.average_price(year, month1, month2, town, [vector_start, store_size-1])
                stddev_pos4 = self.stddev_price(year, month1, month2, town, [vector_start, store_size-1])
                minpsqm_pos4 = self.minimum_price_per_sqm(year, month1, month2, town, [vector_start, store_size-1])
                
            if min_pos4:
                list_of_pos4[0].extend(min_pos4)
            if avg_pos4:
                list_of_pos4[1].extend(avg_pos4)
            if stddev_pos4:
                list_of_pos4[2].extend(stddev_pos4)
            if minpsqm_pos4:
                list_of_pos4[3].extend(minpsqm_pos4)

        # min
        if list_of_pos4[0] == []:
            self.add_result(year, month1, town, "Minimum Price", "No result")
        else:
            min_price = math.inf
            for pos in list_of_pos4[0]:
                price = self.store.get_resale_price(pos)
                if price < min_price:
                    min_price = price
            
            self.add_result(year, month1, town, "Minimum Price", min_price)

        # avg
        if list_of_pos4[1] == []:
            self.add_result(year, month1, town, "Average Price", "No result")
        else:
            total_price = 0
            for pos in list_of_pos4[1]:
                price = self.store.get_resale_price(pos)
                total_price += price
            
            self.add_result(year, month1, town, "Average Price", total_price/len(list_of_pos4[1]))

        # stddev
        if list_of_pos4[2] == []:
            self.add_result(year, month1, town, "Standard Deviation of Price", stddev)
        else:
            count = 0
            average = 0
            ssd = 0  
            for pos in list_of_pos4[2]:
                count += 1
                price = self.store.get_resale_price(pos)
                diff = price - average
                average += diff/count
                updated_diff = price - average
                ssd += diff * updated_diff

            stddev = math.sqrt(ssd/count)

            self.add_result(year, month1, town, "Standard Deviation of Price", stddev)

        # min per sqm
        if list_of_pos4[3] == []:
            self.add_result(year, month1, town, "Minimum Price per Square Meter", "No result")
        else:
            min_price_per_sqm = math.inf
            for pos in list_of_pos4[3]:
                price = self.store.get_resale_price(pos)
                sqm = self.store.get_floor_area_sqm(pos)
                price_per_sqm = price / sqm
                if price_per_sqm < min_price_per_sqm:
                    min_price_per_sqm = price_per_sqm

            self.add_result(year, month1, town, "Minimum Price per Square Meter", min_price_per_sqm)
