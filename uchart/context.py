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
        self._types = ["line", "area", "circle", "label"]
        self._collection = {
            "line": [],
            "area": [],
            "circle": [],
            "label": []
        }

    @property
    def state(self):
        return self._state

    @property
    def types(self):
        return self._types

    @property
    def collection(self):
        return self._collection

    @property
    def user_map_name(self):
        return self._user_map_name

    @user_map_name.setter
    def user_map_name(self, user_map_name):
        self._user_map_name = user_map_name

    @property
    def user_map_desc(self):
        return self._user_map_desc

    @user_map_desc.setter
    def user_map_desc(self, user_map_desc):
        self._user_map_desc = user_map_desc
