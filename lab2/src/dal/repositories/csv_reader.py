"""CSV reader implementation."""

import csv
from typing import Iterator

from src.dal.interfaces.i_csv_reader import ICsvReader


class CsvReader(ICsvReader):
    """Reads a CSV file and yields each row as a dict."""

    def read(self, file_path: str) -> Iterator[dict]:
        with open(file_path, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                yield dict(row)
