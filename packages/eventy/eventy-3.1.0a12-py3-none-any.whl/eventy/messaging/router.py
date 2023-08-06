from eventy.record import Record


class RecordRouter:
    """
    Interface to route record to a topic
    """

    def route(self, record: Record) -> str:
        raise NotImplementedError


class SimpleRouter(RecordRouter):
    """
    Routing all records to the same topic
    """

    def __init__(
        self,
        topic: str,
    ):
        self._topic = topic

    def route(self, record: Record) -> str:
        return self._topic


class ServiceTopicRecordRouter(RecordRouter):
    """
    Routing records according to the <service>-<suffix> eventy convention
    """

    def route(self, record: Record) -> str:
        service = record.namespace.split(':')[-1]
        suffix = {
            'EVENT': 'events',
            'REQUEST': 'requests',
            'RESPONSE': 'responses',
        }.get(record.type, 'unknown')
        return f'{service}-{suffix}'
