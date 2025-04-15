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

def query_resale_prices_singapore_results(last_three_digit: str) -> tuple[float, float, float, float]:
    if len(last_three_digit) != 3:
        raise Exception("Less than 3 digits provided!")
    town = assignment_towns[int(last_three_digit[0])]
    month_start = int(10 if last_three_digit[1] == "0" else last_three_digit[1])
    month_end = month_start + 1
    year = last_three_digit[2]
    area = 80
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f'SELECT MIN(resale_price), ROUND(CAST(STDDEV_POP(resale_price) as numeric), 2), '
                        f'ROUND(CAST(AVG(resale_price) as numeric), 2), '
                        f'ROUND(CAST(MIN(resale_price / floor_area_sqm) as numeric), 2) '
                        f'FROM ResalePricesSingapore '
                        f'WHERE EXTRACT(YEAR FROM TO_DATE(month, \'YYYY-MM\')) BETWEEN 2014 AND 2023 '
                        f'AND RIGHT(EXTRACT(YEAR FROM TO_DATE(month, \'YYYY-MM\'))::TEXT, 1) = %s '
                        f'AND EXTRACT(MONTH FROM TO_DATE(month, \'YYYY-MM\')) BETWEEN %s AND %s '
                        f'AND (town = %s) '
                        f'AND (floor_area_sqm >= %s)', (year, month_start, month_end, town, area))
            return cur.fetchall()[0]
