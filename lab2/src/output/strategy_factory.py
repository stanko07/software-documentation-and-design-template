"""Factory that reads config.json and builds the correct output strategy."""

from __future__ import annotations

import json
import os

from src.output.i_output_strategy import IOutputStrategy

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "config.json")


def load_config(path: str = CONFIG_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def create_strategy(config: dict | None = None) -> IOutputStrategy:
    """
    Read the 'output.strategy' key from config and instantiate
    the matching strategy. Supported values: 'console', 'kafka'.
    """
    if config is None:
        config = load_config()

    strategy_name = config.get("output", {}).get("strategy", "console")

    if strategy_name == "kafka":
        kafka_cfg = config.get("kafka", {})
        from src.output.kafka_strategy import KafkaOutputStrategy
        return KafkaOutputStrategy(
            bootstrap_servers=kafka_cfg.get("bootstrap_servers", "localhost:9092"),
            topic=kafka_cfg.get("topic", "tickets-import"),
        )

    if strategy_name == "file":
        file_cfg = config.get("file", {})
        from src.output.file_strategy import FileOutputStrategy
        return FileOutputStrategy(path=file_cfg.get("path", "data/output.log"))

    # default: console
    from src.output.console_strategy import ConsoleOutputStrategy
    return ConsoleOutputStrategy()
