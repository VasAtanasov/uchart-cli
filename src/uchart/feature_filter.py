
import logging
import os
import sys
import csv

from .libcmds import Macro, Command, ListCsvFiles, ReadCsvFiles, ParseJAN9201Content
from .libuchart import uchart_plugin
from .context import create_global_context

logger = logging.getLogger(__name__)


@uchart_plugin
class Filter:

    @classmethod
    def get_argparser(cls, parser):
        """
            Returns a base parser with common arguments for the generate plugin
        """
        init_parser = parser.add_parser(
            "filter",
            help="Filters usermap objects by positions"
        )

        init_parser.add_argument(
            "north_latitude",
            metavar="<north_latitude>",
            help="The north boundary",
            type=int
        )

        init_parser.add_argument(
            "south_latitude",
            metavar="<south_latitude>",
            help="The south boundary",
            type=int
        )

        init_parser.add_argument(
            "east_longitude",
            metavar="<east_longitude>",
            help="The east boundary",
            type=int
        )

        init_parser.add_argument(
            "west_longitude",
            metavar="<west_longitude>",
            help="The east boundary",
            type=int
        )

    def run(self, args):
        """
            Executes the filter command of the uchart tool.
        """
        if args.cmd != 'filter':
            return False

        ctx = create_global_context()
        logger.debug(ctx.uchart_work_dir)
        macro = Macro()

        macro.add(ListCsvFiles())
        macro.add(ReadCsvFiles())
        macro.add(ParseJAN9201Content())
        macro.add(FilterCommand(args))

        macro.run(ctx)

        return True


class FilterCommand(Command):
    """
        Implements the filter by bounds command.
    """

    def __init__(self, bounds):
        super().__init__()
        self._north_latitude = bounds.north_latitude
        self._south_latitude = bounds.south_latitude
        self._east_longitude = bounds.east_longitude
        self._west_longitude = bounds.west_longitude

    def __str__(self):
        return 'filter'

    def get_message(self):
        return f"Filtering between latitudes {abs(self._north_latitude)}{'N' if self._north_latitude >= 0 else 'S'} " \
            f"and {abs(self._south_latitude)}{'N' if self._south_latitude >= 0 else 'S'} " \
            f"and longitudes {abs(self._east_longitude)}{'E' if self._east_longitude >= 0 else 'W'} " \
            f"and {abs(self._west_longitude)}{'E' if self._west_longitude >= 0 else 'W'} "

    def execute(self, ctx):
        """
            Executes the filter command.
        """
        logger.info(self.get_message())

        filtered_objects = set()
