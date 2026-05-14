"""Concrete strategy: write messages to a log file."""

from __future__ import annotations

from src.output.i_output_strategy import IOutputStrategy


class FileOutputStrategy(IOutputStrategy):

    def __init__(self, path: str) -> None:
        self._file = open(path, "a", encoding="utf-8")
        print(f"[FileOutputStrategy] writing to '{path}'")

    def write(self, message: str) -> None:
        self._file.write(message + "\n")
        self._file.flush()

    def close(self) -> None:
        self._file.close()
        print("[FileOutputStrategy] file closed")
