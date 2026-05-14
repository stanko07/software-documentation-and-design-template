"""Concrete strategy: write messages to stdout."""

from src.output.i_output_strategy import IOutputStrategy


class ConsoleOutputStrategy(IOutputStrategy):

    def write(self, message: str) -> None:
        print(message)

    def close(self) -> None:
        pass  # nothing to release for stdout
