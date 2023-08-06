import asyncio
import logging
import time
from concurrent.futures import Future
from threading import Thread
from typing import Iterable, Union, Optional

from confluent_kafka import Producer

from eventy.messaging import RecordProducer, AioRecordProducer, ProducerProduceError, RecordRouter
from eventy.record import Record
from eventy.serialization import RecordSerializer

logger = logging.getLogger(__name__)


class ConfluentKafkaRecordProducer(RecordProducer):
    """
    Confluent-Kafka producer wrapper.
    """

    def __init__(
        self,
        serializer: RecordSerializer,
        router: RecordRouter,
        bootstrap_servers: Union[str, Iterable[str]],
        sasl_username: Optional[str] = None,
        sasl_password: Optional[str] = None,
        **extra_producer_config,
    ):
        self._router = router
        self._serializer = serializer
        if isinstance(bootstrap_servers, Iterable):
            bootstrap_servers = ','.join(bootstrap_servers)
        producer_config = {
            'bootstrap.servers': bootstrap_servers,
            'enable.idempotence': True,
        }
        if sasl_username and sasl_password:
            producer_config.update(
                {
                    'sasl_mechanism': 'PLAIN',
                    'sasl_plain_username': sasl_username,
                    'sasl_plain_password': sasl_password,
                }
            )
        if extra_producer_config:
            producer_config.update(extra_producer_config)
        self._confluent_producer = Producer(producer_config)
        self._cancelled = False
        self._poll_thread = Thread(target=self._poll_loop)
        self._poll_thread.start()

    def _poll_loop(self):
        while not self._cancelled:
            self._confluent_producer.poll(0.1)

    def close(self):
        self._cancelled = True
        self._poll_thread.join()

    def produce(self, record: Record):
        # message to send
        key = record.partition_key
        value = self._serializer.encode(record)
        topic = self._router.route(record)
        logger.debug(f"Will send {record.qualified_name} on topic {topic} with key {key}.")

        # handle callback
        future_result: Future = Future()

        def ack(err, msg):
            if err:
                future_result.set_exception(ProducerProduceError(err))
            else:
                future_result.set_result(msg)

        # produce message, will trigger callback
        self._confluent_producer.produce(topic=topic, value=value, key=key, on_delivery=ack)

        # wait callback
        while not future_result.done():
            time.sleep(0.05)

        # handle exceptions
        if exception := future_result.exception():
            raise exception


class AioConfluentKafkaRecordProducer(AioRecordProducer):
    """
    Confluent-Kafka producer wrapper.
    """

    def __init__(
        self,
        serializer: RecordSerializer,
        router: RecordRouter,
        bootstrap_servers: Union[str, Iterable[str]],
        sasl_username: Optional[str] = None,
        sasl_password: Optional[str] = None,
        **extra_producer_config,
    ):
        self._router = router
        self._serializer = serializer
        if isinstance(bootstrap_servers, Iterable):
            bootstrap_servers = ','.join(bootstrap_servers)
        producer_config = {
            'bootstrap.servers': bootstrap_servers,
            'enable.idempotence': True,
        }
        if sasl_username and sasl_password:
            producer_config.update(
                {
                    'sasl_mechanism': 'PLAIN',
                    'sasl_plain_username': sasl_username,
                    'sasl_plain_password': sasl_password,
                }
            )
        if extra_producer_config:
            producer_config.update(extra_producer_config)
        self._confluent_producer = Producer(producer_config)
        self._cancelled = False

    async def start(self) -> None:
        self._loop = asyncio.get_event_loop()
        self._poll_thread = Thread(target=self._poll_loop)
        self._poll_thread.start()

    def _poll_loop(self):
        while not self._cancelled:
            self._confluent_producer.poll(0.1)

    async def close(self):
        self._cancelled = True
        self._poll_thread.join()

    async def produce(self, record: Record):
        # message to send
        key = record.partition_key
        value = self._serializer.encode(record)
        topic = self._router.route(record)
        logger.debug(f"Will send {record.qualified_name} on topic {topic} with key {key}.")

        # asyncio future
        future_result = self._loop.create_future()

        def ack(err, msg):
            logger.warning(f"Callback {err} {msg}")
            if err:
                self._loop.call_soon_threadsafe(
                    future_result.set_exception, ProducerProduceError(err)
                )
            else:
                self._loop.call_soon_threadsafe(
                    future_result.set_result, msg
                )

        self._confluent_producer.produce(topic=topic, value=value, key=key, on_delivery=ack)

        await future_result
