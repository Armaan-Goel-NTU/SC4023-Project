import sys
import os
import re

from store import ColumnStore, LengthException, EmptyException
from query import QueryHelper
from pathlib import Path

source = Path(__file__).resolve().parent
DATAFILE = os.path.join(source, "ResalePricesSingapore.csv")
if not os.path.isfile(DATAFILE):
    print(f"{DATAFILE} not found!")
    sys.exit(1)

if len(sys.argv) != 2:
    print("Usage: python3 main.py <Matric>")
    sys.exit(1)

MATRIC = sys.argv[1]
pattern = re.compile(r'[A-Z][0-9]{7}[A-Z]')

if not re.match(pattern=pattern, string=MATRIC):
    print("Invalid Matric format. Should be A1234567B")
    sys.exit(1)

YEAR = int(MATRIC[-2]) + 2010
if YEAR < 2014:
    YEAR += 10

MONTH1 = int(MATRIC[-3])
MONTH2 = MONTH1 + 1

TOWNS = ['BEDOK', 'BUKIT PANJANG', 'CLEMENTI', 'CHOA CHU KANG', 'HOUGANG', 'JURONG WEST', 'PASIR RIS', 'TAMPINES', 'WOODLANDS', 'YISHUN']
TOWN = TOWNS[int(MATRIC[-4])]

print("Loading data")
store = ColumnStore()
with open(DATAFILE, 'r') as f:
    line = f.readline()
    while True:
        line = f.readline()[:-1]
        if not line:
            break
        try:
            store.add_entry(line.split(','))
        except LengthException as l:
            print("Line {}:", str(l), "Skipping...")
        except EmptyException as e:
            print("Line {}:", str(l), "Skipping...")

print(f"Running queries for {TOWN} from months {MONTH1} to {MONTH2} in {YEAR}")
query = QueryHelper(store=store)

print("\n---------INDIVIDUAL SCANS---------")
query.minimum_price(YEAR, MONTH1, MONTH2, TOWN)
query.average_price(YEAR, MONTH1, MONTH2, TOWN)
query.stddev_price(YEAR, MONTH1, MONTH2, TOWN)
query.minimum_price_per_sqm(YEAR, MONTH1, MONTH2, TOWN)
print(query.get_results())

query.clear_results()

print("\n---------SHARED SCANS---------")
query.shared_scan(YEAR, MONTH1, MONTH2, TOWN)
print(query.get_results())

query.clear_results()

print("\n---------VECTOR AT A TIME---------")
query.vector_a_time(YEAR, MONTH1, MONTH2, TOWN)  # By default vector_size = 5000
print(query.get_results())

