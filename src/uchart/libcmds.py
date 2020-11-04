"""
    This module contains common commands used by uchart tool.
"""
import logging
from os import listdir

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


class ReadCsvFilenames(Command):
    """
        Reads and csv filenames in current dir.
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'ReadCsvFilenames'

    def execute(self, ctx):

        def find_csv_filenames(path_to_dir=".", suffix=".csv"):
            filenames = listdir(path_to_dir)
            return [filename for filename in filenames if filename.endswith(suffix)]

        ctx.filenames = find_csv_filenames(ctx.uchart_work_dir)
        logger.info(f"Total of {len(ctx.filenames)} csv files found")
