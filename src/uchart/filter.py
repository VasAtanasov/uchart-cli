
import logging
import os
import sys
import csv

from .libcmds import Macro, ListCsvFiles, ReadCsvFiles, ParseJAN9201Content
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
        logger.info(get_message(args))

        ctx = create_global_context()
        logger.debug(ctx.uchart_work_dir)
        macro = Macro()

        macro.add(ListCsvFiles())
        macro.add(ReadCsvFiles())
        macro.add(ParseJAN9201Content())
        # macro.add(ParseFileContent())
        # macro.add(GenerateXmlFIle())

        macro.run(ctx)

        return True


def get_message(args):
    return f"Filtering between latitudes {abs(args.north_latitude)}{'N' if args.north_latitude >= 0 else 'S'} " \
        f"and {abs(args.south_latitude)}{'N' if args.south_latitude >= 0 else 'S'} " \
        f"and longitudes {abs(args.east_longitude)}{'E' if args.east_longitude >= 0 else 'W'} " \
        f"and {abs(args.west_longitude)}{'E' if args.west_longitude >= 0 else 'W'} "
