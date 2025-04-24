from constants import assignment_towns
from tests.connection import get_connection

def query_resale_prices_singapore_results(last_three_digit: str) -> tuple[float, float, float, float]:
    """Queries resale price statistics from the ResalePricesSingapore table using encoded 3-digit input."""
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
                        f'MIN(resale_price / floor_area_sqm) '
                        f'FROM ResalePricesSingapore '
                        f'WHERE EXTRACT(YEAR FROM TO_DATE(month, \'YYYY-MM\')) BETWEEN 2014 AND 2023 '
                        f'AND RIGHT(EXTRACT(YEAR FROM TO_DATE(month, \'YYYY-MM\'))::TEXT, 1) = %s '
                        f'AND EXTRACT(MONTH FROM TO_DATE(month, \'YYYY-MM\')) BETWEEN %s AND %s '
                        f'AND (town = %s) '
                        f'AND (floor_area_sqm >= %s)', (year, month_start, month_end, town, area))
            return cur.fetchall()[0]
