# Copyright (c) Qotto, 2021

"""
Request record
"""

from eventy.record import Record

__all__ = [
    'Request',
]


class Request(Record):
    """
    Request implementation of the Record abstract base class
    """

    @property
    def type(self):
        """
        Record type (REQUEST)

        :return: "REQUEST"
        """

        return 'REQUEST'
