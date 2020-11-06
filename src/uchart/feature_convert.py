
import logging
import os
import sys
import csv

from .libcmds import (Macro, Command, ListCsvFiles,
                      ReadCsvFiles, ParseJAN9201Content, WriteUserchartToCsv)
from .libuchart import uchart_plugin
from .context import create_global_context
from .models import EcdisUserchart

from .mappings import object_mappers

logger = logging.getLogger(__name__)


@uchart_plugin
class Convert:

    @classmethod
    def get_argparser(cls, parser):
        """
            Returns a base parser with common arguments for the convert plugin
        """
        init_parser = parser.add_parser(
            "convert",
            help="Converts JAN9201 usercharts to JAN901B usercharts"
        )

    def run(self, args):
        """
            Executes the convert command of the uchart tool.
        """
        if args.cmd != 'convert':
            return False

        ctx = create_global_context()
        logger.debug(ctx.uchart_work_dir)
        macro = Macro()

        macro.add(ListCsvFiles())
        macro.add(ReadCsvFiles())
        macro.add(ParseJAN9201Content())
        macro.add(ConvertCommand(args))
        macro.add(WriteUserchartToCsv())

        macro.run(ctx)

        return True


class ConvertCommand(Command):
    """
        Implements the filter by bounds command.
    """

    def __init__(self, args):
        super().__init__()

    def execute(self, ctx):
        """
            Executes the convert command.
        """
        logger.info("Converting JAN9201 usercharts to JAN901B usercharts")
        converts = 0
        objects = 0
        for userchart_name, userchart in ctx.usercharts_objects_by_userchart.items():
            jan901b_userchart = EcdisUserchart.copy_raw(userchart)

            for obj in userchart.usercart_objects:
                objects = objects + 1
                if obj.object_type in object_mappers:
                    mapper = object_mappers[obj.object_type]
                    if mapper == None:
                        jan901b_userchart.usercart_objects.add(obj)
                        converts = converts + 1
                        continue
                    new_obj = mapper(obj)
                    if not new_obj == None:
                        jan901b_userchart.usercart_objects.add(new_obj)
                        converts = converts + 1
                else:
                    logger.debug(f"No mapping for {obj.object_type}")

            for obj in jan901b_userchart.usercart_objects:
                jan901b_userchart.content.extend(obj.content)
            ctx.usercharts.append(jan901b_userchart)

        logger.info(f"Converted {converts} objects of {objects}")
