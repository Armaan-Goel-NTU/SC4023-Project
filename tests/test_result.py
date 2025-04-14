import os
import pytest
from testcontainers.postgres import PostgresContainer
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

    request.addfinalizer(remove_container)
    os.environ["DB_HOST"] = postgres.get_container_host_ip()
    os.environ["DB_PORT"] = postgres.get_exposed_port(5432)
    os.environ["DB_USERNAME"] = postgres.username
    os.environ["DB_PASSWORD"] = postgres.password
    os.environ["DB_NAME"] = postgres.dbname
    create_table_from_csv("../ResalePricesSingapore.csv")

#TODO: Hardcoded, use parameterized tests, run subprocess, then do assert on the 4 methods in queryhelper
def test_query_result(request: str="567"):
    print(query_resale_prices_singapore_results(request))
