"""
    This module contains the implementation of the uchart context.
"""
import logging
import os

__context__ = None

logger = logging.getLogger(__name__)


def create_global_context():
    """
        Creates global context as singleton.
    """
    global __context__
    __context__ = Context()
    return __context__


def get_context():
    """
        Returns singleton global context.
    """
    return __context__


class Context:
    """
        Implements the uchart build context.
    """

    def __init__(self):
        self.__uchart_work_dir = os.getcwd()
        self._state = {}

    @property
    def state(self):
        return self._state