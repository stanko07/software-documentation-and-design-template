"""Concrete strategy: send messages to a Kafka topic."""

from __future__ import annotations

from src.output.i_output_strategy import IOutputStrategy


class KafkaOutputStrategy(IOutputStrategy):
    """
    Sends each message as a UTF-8 encoded Kafka record.

    Requires:  pip install kafka-python
    Config keys used:
        kafka.bootstrap_servers  — e.g. "localhost:9092"
        kafka.topic              — target topic name
    """

    def __init__(self, bootstrap_servers: str, topic: str) -> None:
        from kafka import KafkaProducer  # imported lazily so kafka-python is optional
        self._topic = topic
        self._producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: v.encode("utf-8"),
        )
        print(f"[KafkaOutputStrategy] connected to {bootstrap_servers}, topic='{topic}'")

    def write(self, message: str) -> None:
        self._producer.send(self._topic, value=message)

    def close(self) -> None:
        self._producer.flush()
        self._producer.close()
        print("[KafkaOutputStrategy] producer closed")
