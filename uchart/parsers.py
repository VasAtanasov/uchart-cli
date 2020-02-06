import logging
import os
import sys
import csv

from .context import get_context
from .lib import (uchart_plugin)
from .commands import (
    Macro,
    IsFile,
    IsCsv,
    OpenCsvFile,
    ParseFileContent,
    GenerateXmlFIle,
    ParseJAN9201Content
)

logger = logging.getLogger(__name__)


@uchart_plugin
class Generate:

    @classmethod
    def get_argparser(cls, parser):
        """
            Returns a base parser with common arguments for the generate plugin
        """
        init_parser = parser.add_parser(
            "gen",
            help="Generates Furuno ECDIS usermap from csv file."
        )

        init_parser.add_argument(
            "file",
            metavar="<file>",
            help="file with user chart elements",
            type=str
        )

    def run(self, args):
        if args.cmd != 'gen':
            return False
        logger.debug("Running Generate:run")

        ctx = get_context()
        ctx.file = args.file

        macro = Macro()

        macro.add(IsFile())
        macro.add(IsCsv())
        macro.add(OpenCsvFile())
        macro.add(ParseFileContent())
        macro.add(GenerateXmlFIle())

        macro.run(ctx)

        return True


@uchart_plugin
class JrcParser:

    @classmethod
    def get_argparser(cls, parser):
        """
            Returns a base parser with common arguments for the generate plugin
        """
        init_parser = parser.add_parser(
            "jrc",
            help="Generates Furuno ECDIS usermap from JRC JAN 9201 ECIDS usermap csv file."
        )

        init_parser.add_argument(
            "file",
            metavar="<file>",
            help="file with user chart elements",
            type=str
        )

    def run(self, args):
        if args.cmd != 'jrc':
            return False
        logger.debug("Running JrcParser:run")

        ctx = get_context()
        ctx.file = args.file

        macro = Macro()

        macro.add(IsFile())
        macro.add(IsCsv())
        macro.add(OpenCsvFile())
        macro.add(ParseJAN9201Content())
        macro.add(GenerateXmlFIle())

        macro.run(ctx)

        return True


@uchart_plugin
class Converter:

    @classmethod
    def get_argparser(cls, parser):
        """
            Returns a base parser with common arguments for the generate plugin
        """
        init_parser = parser.add_parser(
            "cnv",
            help="Generates Furuno ECDIS usermap from JRC JAN 9201 ECIDS usermap csv file."
        )

        init_parser.add_argument(
            "file",
            metavar="<file>",
            help="file with user chart elements",
            type=str
        )

        init_parser.add_argument(
            "type",
            metavar="<type>",
            help="destination file typ",
            type=str
        )

    def run(self, args):
        if args.cmd != 'cnv':
            return False
        logger.debug("Running JrcParser:run")

        ctx = get_context()
        ctx.file = args.file
        ctx.type = args.type

        import json

        with open(ctx.file) as f:
            data = json.load(f)

        import csv

        with open('route.csv', mode='w', newline='') as csv_file:
            fieldnames = ['name', 'latitude', 'longitude']
            writer = csv.DictWriter(
                csv_file, fieldnames=fieldnames, extrasaction='ignore')

            writer.writeheader()
            for waypoint in data["routes"][0]["waypoints"]:
                writer.writerow(waypoint)
                lat = waypoint["latitude"]
                lon = waypoint["longitude"]
                name = waypoint["name"]

        macro = Macro()

        macro.add(IsFile())

        macro.run(ctx)

        return True
