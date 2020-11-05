"""
    This module contains the implementation of the uchart context.
"""
import logging
import os

from .models import Jan9021
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
        self._uchart_work_dir = os.environ.get('UCHART_WORK_DIR', os.getcwd())
        self._jan = Jan9021()
        self._filenames = list()
        self._usercharts_by_name = {}
        self._usercharts_objects_by_userchart = {}
        self._userchart_objects = set()

    @property
    def uchart_work_dir(self):
        return self._uchart_work_dir

    @property
    def ecdis(self):
        return self._jan

    @property
    def usercharts_objects_by_userchart(self):
        return self._usercharts_objects_by_userchart

    @property
    def usercharts_by_name(self):
        return self._usercharts_by_name

    @property
    def userchart_objects(self):
        return self._userchart_objects

    @property
    def filenames(self):
        return self._filenames

    @filenames.setter
    def filenames(self, filenames):
        self._filenames = filenames
