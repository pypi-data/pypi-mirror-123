# Copyright (c) Qotto, 2021

"""
Eventy messaging API

The messaging API itself is backend-agnostic, there is currently only a Kafka backend implemented.
"""

from eventy.messaging.base import (
    RecordProducer, AioRecordProducer,
    RecordConsumer, AioRecordConsumer,
    RecordProcessor, AioRecordProcessor,
)
from eventy.messaging.errors import (
    MessagingError,
    ProducerCreationError,
    ProducerProduceError,
    ConsumerCreationError,
    ConsumerPollError,
    ConsumerCommitError,
    ProcessorTransactionError,
)
from eventy.messaging.router import (
    RecordRouter,
    ServiceTopicRecordRouter,
)

__all__ = [
    # base
    'RecordProducer',
    'AioRecordProducer',
    'RecordConsumer',
    'AioRecordConsumer',
    'RecordProcessor',
    'AioRecordProcessor',
    # router
    'RecordRouter',
    'ServiceTopicRecordRouter',
    # errors
    'MessagingError',
    'ProducerCreationError',
    'ProducerProduceError',
    'ConsumerCreationError',
    'ConsumerPollError',
    'ConsumerCommitError',
    'ProcessorTransactionError',
]
