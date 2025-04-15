import sys
import os

from constants import assignment_towns, town, flat_type, storey_range, flat_model
from store import ColumnStore, StorageException
from query import QueryHelper
from Mapping.default_mappings import *
from Mapping.enum_mappings import *
from Mapping.special_mappings import *

if len(sys.argv) != 3:
    print("Usage: python3 main.py <CSV file> <Matric>")
    sys.exit(1)

DATAFILE = sys.argv[1]
if not os.path.isfile(DATAFILE):
    print(f"{DATAFILE} not found!")
    sys.exit(1)

MATRIC = sys.argv[2]
pattern = re.compile(r'[A-Z][0-9]{7}[A-Z]')

if not re.match(pattern=pattern, string=MATRIC):
    print("Invalid Matric format. Should be A1234567B")
    sys.exit(1)

townMapper = TownMapper(town)

TOWN_NAME = assignment_towns[int(MATRIC[-4])]
TOWN = townMapper.map_value(TOWN_NAME)

monthMapper = MonthMapper()
floatMapper = FloatMapper()
shortMapper = ShortMapper()

YEAR = int(MATRIC[-2]) + 2010
if YEAR < 2014:
    YEAR += 10

month_str = "10" if f"0{MATRIC[-3]}" == "00" else f"0{MATRIC[-3]}"
MONTH = monthMapper.map_value(f"{YEAR}-{month_str}")

print("Loading data")
basic_mappings = [
    CharMapper(7),
    CharMapper(15),
    CharMapper(16),
    CharMapper(5),
    CharMapper(20),
    CharMapper(12),
    floatMapper,
    CharMapper(22),
    shortMapper,
    floatMapper,
]

compressed_mappings = [
    monthMapper,
    townMapper,
    FlatTypeMapper(flat_type),
    BlockMapper(),
    CharMapper(20),
    StoreyRangeMapper(storey_range),
    floatMapper,
    FlatModelMapper(flat_model),
    shortMapper,
    floatMapper,
]

critical = [0, 1, 6, 9]

with open(DATAFILE, 'r') as f:
    print("\n---------BASIC STORE---------")
    columns = f.readline()[:-1].split(",")
    basic_store = ColumnStore(
        columns=columns, mappings=basic_mappings, critical=critical, basic=True
    )
    while True:
        line = f.readline()[:-1]
        if not line:
            break
        try:
            basic_store.add_entry(line.split(","))
        except StorageException as s:
            print(f"Line {line}:", str(s), "Skipping...")
    basic_store.flush_write_buffers()
    basic_store.print_storage_stats()
    basic_store.clear_disk()

with open(DATAFILE, "r") as f:
    print("\n---------COMPRESSED STORE---------")
    columns = f.readline()[:-1].split(",")
    store = ColumnStore(
        columns=columns, mappings=compressed_mappings, critical=critical
    )
    while True:
        line = f.readline()[:-1]
        if not line:
            break
        try:
            store.add_entry(line.split(","))
        except StorageException as s:
            print(f"Line {line}:", str(s), "Skipping...")
    store.flush_write_buffers()
    store.print_storage_stats()

    print(
        f"\n\nRunning queries for {TOWN_NAME} from months {int(MATRIC[-3])} to {int(MATRIC[-3])+1} in {YEAR}"
    )

    print("\n---------FILTER PERMUTATIONS (ZM OFF; IDX OFF)---------")
    query = QueryHelper(store=store)
    query.test_filter_permutations(MONTH, TOWN, False, False)

    print("\n---------FILTER PERMUTATIONS (ZM ON; IDX OFF)---------")
    query = QueryHelper(store=store)
    query.test_filter_permutations(MONTH, TOWN, True, False)

    print("\n---------FILTER PERMUTATIONS (ZM OFF; IDX ON)---------")
    query = QueryHelper(store=store)
    query.test_filter_permutations(MONTH, TOWN, False, True)

    print("\n---------FILTER PERMUTATIONS (ZM ON; IDX ON)---------")
    query = QueryHelper(store=store)
    query.test_filter_permutations(MONTH, TOWN, True, True)

    reads = 0
    print("\n---------INDIVIDUAL SCANS---------")
    query.minimum_price(MONTH, TOWN)
    reads += store.reads
    print(f"{store.reads} block reads for min price")

    query.average_price(MONTH, TOWN)
    reads += store.reads
    print(f"{store.reads} block reads for avg price")

    query.stddev_price(MONTH, TOWN)
    reads += store.reads
    print(f"{store.reads} block reads for stddev price")

    query.minimum_price_per_sqm(MONTH, TOWN)
    reads += store.reads
    print(f"{store.reads} block reads for min price/sqm")
    print(f"{reads} total block reads")
    results = query.get_results()
    with open(f"ScanResult_{MATRIC}.csv", "w") as g:
        g.write(results)
    print(results)

    query.clear_results()

    print("\n---------SHARED SCANS---------")
    query.shared_scan(MONTH, TOWN)
    print(f"{store.reads} block reads")
    print(query.get_results())

    query.clear_results()

    print("\n---------VECTOR AT A TIME---------")
    query.vector_a_time(MONTH, TOWN)
    print(f"{store.reads} block reads")
    print(query.get_results())

    store.clear_disk()
