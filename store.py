from pathlib import Path
import os
from Mapping.mapper import MapException, Mapper

BLOCK_SIZE = 4096

class StorageException(Exception):
    pass

class ColumnStore:

    def __init__(self, columns, mappings: list[Mapper], critical):
        if len(mappings) != len(columns):
            raise StorageException(
                f"Number of columns {len(columns)} must match number of mappings {len(self.mappings)}."
            )

        self.critical = critical
        self.mappings = mappings
        self.size = 0
        self.reads = 0

        source = Path(__file__).resolve().parent
        self.columns = [os.path.join(source, f"_{c}") for c in columns]

        self.write_pointers = [open(c, "wb") for c in self.columns]
        self.write_buffers = [b""] * len(columns)

        self.read_pointers = [None] * len(columns)
        self.read_buffers = [b""] * len(columns)

    def clear_disk(self):
        self.flush_write_buffers()
        self.clear_read_state()
        for column in self.columns:
            if os.path.isfile(column):
                os.remove(column)

    def clear_read_state(self):
        self.reads = 0
        for fp in self.read_pointers:
            if fp is not None:
                fp.close()

        self.read_pointers = [None] * len(self.columns)
        self.read_buffers = [b""] * len(self.columns)

    def flush_write_buffer(self, i):
        if self.write_buffers[i] == b"":
            return

        self.write_pointers[i].write(self.write_buffers[i].ljust(4096, b"\x00"))
        self.write_buffers[i] = b""

    def flush_write_buffers(self):
        for i in range(len(self.write_buffers)):
            self.flush_write_buffer(i)
            self.write_pointers[i].close()

    def print_storage_stats(self):
        row_format = "{:>15}" * 2
        print(row_format.format("Column", "Blocks"))
        total = 0
        for column in self.columns:
            size = os.path.getsize(column) // BLOCK_SIZE
            print(row_format.format(os.path.basename(column)[1:], size))
            total += size
        print(row_format.format("Total", total))

    def add_entry(self, tokens):
        if len(tokens) != len(self.mappings):
            raise StorageException(
                f"Expected {self.mappings} tokens, got {len(tokens)}."
            )

        for pos in self.critical:
            if not tokens[pos]:
                raise StorageException(f"Expected attribute {pos} to be non-empty.")

        try:
            for i in range(len(tokens)):
                tokens[i] = self.mappings[i].map_value(tokens[i])
        except MapException as e:
            raise StorageException(str(e))

        self.size += 1
        for i in range(len(tokens)):
            packed = self.mappings[i].to_bytes(tokens[i])

            if len(self.write_buffers[i]) + self.mappings[i].mapped_size() > BLOCK_SIZE:
                self.flush_write_buffer(i)

            self.write_buffers[i] += packed

    def get_size(self):
        return self.size

    def get_item(self, pos, i):
        items_per_page = BLOCK_SIZE // self.mappings[i].mapped_size()
        block_number = pos // items_per_page
        if self.read_pointers[i] is None:
            self.read_pointers[i] = open(self.columns[i], "rb")

        if self.read_pointers[i].tell() != (block_number + 1) * BLOCK_SIZE:
            self.reads += 1
            self.read_pointers[i].seek(block_number * BLOCK_SIZE)
            self.read_buffers[i] = self.read_pointers[i].read(BLOCK_SIZE)

        start = (pos % items_per_page) * self.mappings[i].mapped_size()
        return self.mappings[i].from_bytes(
            self.read_buffers[i][start : start + self.mappings[i].mapped_size()]
        )

    def get_month(self, pos):
        return self.get_item(pos, 0)

    def get_town(self, pos):
        return self.get_item(pos, 1)

    def get_floor_area_sqm(self, pos):
        return self.get_item(pos, 6)

    def get_resale_price(self, pos):
        return self.get_item(pos, 9)

    def unmap_town(self, index):
        return self.mappings[1].unmap_value(index)

    def unmap_month(self, month):
        return self.mappings[0].unmap_value(month)
