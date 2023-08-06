from eventy.messaging.base import RecordProducer
from eventy.record import Record
from eventy.serialization import RecordSerializer


class MemoryRecordProducer(RecordProducer):
    def __init__(
        self,
        serializer: RecordSerializer,
    ):
        self._serializer = serializer
        self._serialized_list: list[bytes] = []

    def produce(self, record: Record) -> None:
        self._serialized_list.append(self._serializer.encode(record))

    def get_produced_records(self) -> list[Record]:
        return list(map(self._serializer.decode, self._serialized_list))

    def pop_produced_records(self) -> list[Record]:
        result = self.get_produced_records()
        self._serialized_list = []
        return result
