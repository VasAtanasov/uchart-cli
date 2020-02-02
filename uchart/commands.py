import logging
import os
import sys
from abc import ABC, abstractmethod

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
            logger.debug(f'Execute {command_name}.', )
            command.execute(ctx)


class Command(ABC):
    """
        An abstract class that defines the interface of a command.
    """

    @abstractmethod
    def execute(self, ctx):
        """
            This method executes the command.
        """
        pass


class IsFile(Command):
    """
        Check if file exists.
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'IsFile'

    def execute(self, ctx):
        filename = ctx.file
        logging.debug("Checking if the file exists")
        is_file = os.path.isfile(filename)
        if not is_file:
            logging.critical(f"File does not exists: \'{filename}\'")
            sys.exit(1)

        logging.debug(f"File {filename} is present!")


class IsCsv(Command):
    """
        Check if file is with csv extention.
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'IsCsv'

    def execute(self, ctx):
        filename = ctx.file
        if not filename.endswith(".csv"):
            logging.debug("File must be with csv extension!")
            sys.exit(1)
        logging.debug(f"File is with csv extention!")


class OpenCsvFile(Command):
    """
        Reads and parses csv file.
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'OpenCsvFile'

    def execute(self, ctx):
        filename = ctx.file
        csv_file = open(filename)
        logging.debug(f"Reading {filename} ...")
        import csv
        logging.debug(f"Parsing csv file: {filename} ...")
        ctx.content = list(csv.reader(csv_file))
