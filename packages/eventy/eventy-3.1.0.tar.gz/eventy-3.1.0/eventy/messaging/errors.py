# Copyright (c) Qotto, 2021

"""
Messaging errors
"""

__all__ = [
    'MessagingError',
    'ConsumerCreationError',
    'ConsumerPollError',
    'ConsumerCommitError',
    'ProducerProduceError',
    'ProducerCreationError',
    'ProcessorTransactionError',
]


class MessagingError(Exception):
    """
    Base Error class of all messaging API
    """


class ConsumerCreationError(MessagingError):
    """
    A consumer could not be initialized
    """


class ConsumerPollError(MessagingError):
    """
    A consumer could not poll messages
    """


class ConsumerCommitError(MessagingError):
    """
    A consumer could not commit messages
    """


class ProducerCreationError(MessagingError):
    """
    A producer could not be initialized
    """


class ProducerProduceError(MessagingError):
    """
    A producer could not produce a message
    """


class ProcessorTransactionError(MessagingError):
    """
    A transactional producer or processor could not commit a transaction
    """
