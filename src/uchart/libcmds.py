"""
    This module contains common commands used by uchart tool.
"""
import logging
import csv

from os import listdir
from os.path import join
from .factories import Jan9201ObjectFactory

logger = logging.getLogger(__name__)


class Macro:
    """
        Contains commands and provides method to run them.
    """

    def __init__(self):
        self.commands = []

    def add(self, command):
        """
            Appends commands to the command list.
        """
        self.commands.append(command)

    def run(self, ctx):
        """
            Runs a command from the command list with respect to the
            configuration.
        """
        for command in self.commands:
            command_name = str(command)
            logging.debug('execute %s', command_name)
            command.execute(ctx)


class Command:
    """
        An abstract class that defines the interface of a command.
    """

    def execute(self, ctx):
        """
            This method executes the command.
        """
        pass


class ListCsvFiles(Command):
    """
        Reads and csv filenames in current dir.
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'ListCsvFiles'

    def execute(self, ctx):

        def find_csv_filenames(path_to_dir=".", suffix=".csv"):
            filenames = listdir(path_to_dir)
            return [filename for filename in filenames if filename.endswith(suffix)]

        ctx.filenames = find_csv_filenames(ctx.uchart_work_dir)
        logger.info(f"Total of {len(ctx.filenames)} csv files found")


class ReadCsvFiles(Command):
    """
        Reads and csv filenames in current dir.
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'ReadCsvFiles'

    def execute(self, ctx):
        filenames = ctx.filenames
        for filename in filenames:
            with open(join(ctx.uchart_work_dir, filename)) as csv_file:
                logging.debug(f"Reading {filename}...")
                content = tuple(tuple(i) for i in csv.reader(csv_file))
                userchart_name = f"{content[2][0][3:]}.csv"
                ctx.usercharts_by_name[userchart_name] = content


class ParseJAN9201Content(Command):
    """
        Parses JRC JAN 9201 ECDIS csv usermap file to objects.
    """

    def __init__(self):
        super().__init__()
        self._object_factory = Jan9201ObjectFactory()

    def __str__(self):
        return 'ParseJAN9201Content'

    def execute(self, ctx):
        for userchart_name, content in ctx.usercharts_by_name.items():
            ctx.objects_by_usermap[userchart_name] = self._object_factory.get_objects(
                content[3:])

        a = 5
