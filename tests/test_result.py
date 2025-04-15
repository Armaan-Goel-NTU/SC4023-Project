import csv
import glob
import os
import subprocess

import pytest
from testcontainers.postgres import PostgresContainer

from Enum.Metrics import Metrics
from .ResalePricesSingapore import query_resale_prices_singapore_results
from .connection import get_connection

postgres = PostgresContainer("postgres:16")

def create_table_from_csv(csv_file_name: str, table_name: str="ResalePricesSingapore"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
        month TEXT,
        town TEXT,
        flat_type TEXT,
        block TEXT,
        street_name TEXT,
        storey_range TEXT,
        floor_area_sqm REAL,
        flat_model TEXT,
        lease_commence_date INT,
        resale_price REAL);""")
    sql = f"COPY {table_name} FROM STDIN DELIMITER ',' CSV HEADER"
    cursor.copy_expert(sql, open(csv_file_name, "r"))
    conn.commit()
    cursor.close()
    conn.close()

@pytest.fixture(scope="module", autouse=True)
def setup(request):
    postgres.start()

    def remove_container():
        postgres.stop()

        for file in glob.glob("ScanResult_*.csv"):
            try:
                os.remove(file)
            except FileNotFoundError:
                pass

    request.addfinalizer(remove_container)
    os.environ["DB_HOST"] = postgres.get_container_host_ip()
    os.environ["DB_PORT"] = str(postgres.get_exposed_port(5432))
    os.environ["DB_USERNAME"] = postgres.username
    os.environ["DB_PASSWORD"] = postgres.password
    os.environ["DB_NAME"] = postgres.dbname
    create_table_from_csv("../ResalePricesSingapore.csv")

@pytest.mark.parametrize("last_3_digit_code", [str(i).zfill(3) for i in range(1000)])
def test_query_result(last_3_digit_code: str):
    min_price, stddev_price, avg_price, min_price_per_sqm = query_resale_prices_singapore_results(last_3_digit_code)
    print(min_price, stddev_price, avg_price, min_price_per_sqm)
    matriculation_number = "A1234" + last_3_digit_code + "B"
    subprocess.run(
        ["python", "../main.py", "../ResalePricesSingapore.csv", matriculation_number],
        capture_output=False,
        text=True
    )

    result_csv_path = f"ScanResult_{matriculation_number}.csv"
    assert os.path.exists(result_csv_path), f"{result_csv_path} not found."

    results = {}
    with open(result_csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            category = row["Category"]
            value = None if row["Value"] == "No result" else float(row["Value"])
            results[category] = value

    assert results.get(Metrics.MIN_PRICE.value) == min_price
    assert results.get(Metrics.STDDEV.value) == float(stddev_price)
    assert results.get(Metrics.AVG_PRICE.value) == float(avg_price)
    assert results.get(Metrics.MIN_PRICE_PER_SQM.value) == round(float(min_price_per_sqm), 2)
