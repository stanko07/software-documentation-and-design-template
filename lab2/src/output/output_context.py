"""Context class that delegates output to the configured strategy."""

from src.output.i_output_strategy import IOutputStrategy


class OutputContext:
    """
    Holds a reference to an IOutputStrategy and delegates all writes to it.
    The strategy can be swapped at runtime if needed.
    """

    def __init__(self, strategy: IOutputStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: IOutputStrategy) -> None:
        self._strategy = strategy

    def write(self, message: str) -> None:
        self._strategy.write(message)

    def close(self) -> None:
        self._strategy.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
