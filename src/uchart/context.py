"""
    This module contains the implementation of the uchart context.
"""
import logging
import os

from .models import EcdisUserchart
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
        self._filenames = list()
        self._file_content_by_userchart_name = {}
        self._usercharts_objects_by_userchart = {}
        self._userchart_objects = set()
        self._usercharts = list()

    @property
    def uchart_work_dir(self):
        return self._uchart_work_dir

    @property
    def usercharts(self):
        return self._usercharts

    @property
    def usercharts_objects_by_userchart(self):
        return self._usercharts_objects_by_userchart

    @property
    def file_content_by_userchart_name(self):
        return self._file_content_by_userchart_name

    @property
    def userchart_objects(self):
        return self._userchart_objects

    @property
    def filenames(self):
        return self._filenames

    @filenames.setter
    def filenames(self, filenames):
        self._filenames = filenames
