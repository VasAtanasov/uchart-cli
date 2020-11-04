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
        self._usercharts_by_name = {}
        self._objects_by_usermap = {}

    @property
    def uchart_work_dir(self):
        return self._uchart_work_dir

    @property
    def objects_by_usermap(self):
        return self._objects_by_usermap

    @property
    def usercharts_by_name(self):
        return self._usercharts_by_name

    @property
    def user_map_name(self):
        return self._user_map_name

    @user_map_name.setter
    def user_map_name(self, user_map_name):
        self._user_map_name = user_map_name

    @property
    def filenames(self):
        return self._filenames if self._filenames is not None else list()

    @filenames.setter
    def filenames(self, filenames):
        self._filenames = filenames
