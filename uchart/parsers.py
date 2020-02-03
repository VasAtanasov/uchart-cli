import logging
import os
import sys
import csv

from .lib import parse_jan9201_content
from .context import get_context
from .lib import (uchart_plugin)
from .commands import (
    Macro,
    IsFile,
    IsCsv,
    OpenCsvFile,
    ParseFileContent,
    GenerateXmlFIle
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
            help="Generates Furuno ECDIS usermap from tsv file."
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
