from tests.connection import get_connection

assignment_towns = [
    "BEDOK",
    "BUKIT PANJANG",
    "CLEMENTI",
    "CHOA CHU KANG",
    "HOUGANG",
    "JURONG WEST",
    "PASIR RIS",
    "TAMPINES",
    "WOODLANDS",
    "YISHUN",
]

class ResalePricesSingapore:
    def __init__(self, month, town, flat_type, block, street_name, storey_range, floor_area_sqm, flat_model,
                 lease_commence_date, resale_price):
        self.month = month
        self.town = town
        self.flat_type = flat_type
        self.block = block
        self.street_name = street_name
        self.storey_range = storey_range
        self.floor_area_sqm = floor_area_sqm
        self.flat_model = flat_model
        self.lease_commence_date = lease_commence_date
        self.resale_price = resale_price

    def to_csv_row(self) -> str:
        return ','.join(str(value) for value in [
            self.month,
            self.town,
            self.flat_type,
            self.block,
            self.street_name,
            self.storey_range,
            self.floor_area_sqm,
            self.flat_model,
            self.lease_commence_date,
            self.resale_price
        ])

def query_resale_prices_singapore_results(last_three_digit: str) -> list[float]:
    if len(last_three_digit) != 3:
        raise Exception("Less than 3 digits provided!")
    town = assignment_towns[int(last_three_digit[0])]
    month_start = int(last_three_digit[1])
    month_end = month_start + 1
    year = int('201' + last_three_digit[2])
    area = 80
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f'SELECT MIN(resale_price), STDDEV_POP(resale_price), AVG(resale_price), MIN(resale_price / floor_area_sqm) '
                        f'FROM ResalePricesSingapore '
                        f'WHERE EXTRACT(YEAR FROM TO_DATE(month, \'YYYY-MM\')) = %s '
                        f'AND EXTRACT(MONTH FROM TO_DATE(month, \'YYYY-MM\')) BETWEEN %s AND %s '
                        f'AND (town = %s) '
                        f'AND (floor_area_sqm >= %s)', (year, month_start, month_end, town, area))
            return cur.fetchall()
