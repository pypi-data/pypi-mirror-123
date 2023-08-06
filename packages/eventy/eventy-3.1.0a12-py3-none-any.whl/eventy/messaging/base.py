from typing import Optional

from eventy.record import Record


class RecordProducer:

    def start(self) -> None:
        pass

    def close(self) -> None:
        pass

    def produce(self, record: Record) -> None:
        raise NotImplementedError


class AioRecordProducer:

    async def start(self) -> None:
        pass

    async def close(self) -> None:
        pass

    async def produce(self, record: Record) -> None:
        raise NotImplementedError


class RecordConsumer:

    def start(self) -> None:
        pass

    def close(self) -> None:
        pass

    def poll(self) -> Optional[Record]:
        raise NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError


class AioRecordConsumer:
    async def start(self) -> None:
        pass

    async def close(self) -> None:
        pass

    async def poll(self) -> Optional[Record]:
        raise NotImplementedError

    async def commit(self) -> None:
        raise NotImplementedError


class Transaction:
    def get_consumed(self) -> Record:
        raise NotImplementedError

    def send_in_transaction(self, record: Record) -> None:
        raise NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError


class RecordProcessor:
    def start(self) -> None:
        pass

    def close(self) -> None:
        pass

    def transaction(self) -> Optional[Transaction]:
        raise NotImplementedError


class AioRecordProcessor:
    async def start(self) -> None:
        pass

    async def close(self) -> None:
        pass

    async def transaction(self) -> Optional[Transaction]:
        raise NotImplementedError
