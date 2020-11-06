"""
    This module contains common commands used by uchart tool.
"""
import logging
import csv
import sys

from datetime import datetime
from os import listdir
from os.path import join
from .factories import UserchartObjectFactory
from .models import EcdisUserchart, UserchartObject
from .constants import *

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


class Loop(Command):
    """
        A class that defines a set of commands as a loop.
    """

    def __init__(self, name):
        self.commands = []
        self.name = name

    def __str__(self):
        return self.name

    def add(self, command):
        """
            Appends a command to the loop.
        """
        self.commands.append(command)

    def execute(self, ctx):
        """
            Executes the loop.
        """
        loop_name = str(self)

        def executor(command):
            command_name = str(command)
            logging.debug('Loop %s: execute %s', loop_name, command_name)
            return command.execute(ctx)

        while all(executor(c) for c in self.commands):
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

        def predicate(row):
            try:
                return not row[0].startswith('//')
            except IndexError:
                return True

        filenames = ctx.filenames
        for filename in filenames:
            with open(join(ctx.uchart_work_dir, filename)) as csv_file:
                logger.debug(f"Reading {filename}...")
                content = tuple(tuple(i) for i in csv.reader(csv_file))
                userchart_name = f"{content[2][0][3:]}"
                no_comments_content = tuple(filter(predicate, content))
                ctx.file_content_by_userchart_name[userchart_name] = no_comments_content
                csv_file.close()


class ParseJAN9201Content(Command):
    """
        Parses JRC JAN 9201 ECDIS csv usermap file to objects.
    """

    def __init__(self):
        super().__init__()
        self._object_factory = UserchartObjectFactory()

    def __str__(self):
        return 'ParseJAN9201Content'

    def get_end_index(self, start_index, content):
        end_index = len(content)
        for i in range(start_index, len(content)):
            row = content[i]
            if len(row) > 0 and row[0] in jan9201_objects:
                return i
        return end_index

    def execute(self, ctx):
        duplicates = 0
        total_objects = 0

        for userchart_name, content in ctx.file_content_by_userchart_name.items():
            if userchart_name not in ctx.usercharts_objects_by_userchart:
                ctx.usercharts_objects_by_userchart[userchart_name] = EcdisUserchart(
                    content)

            start_index = 0
            while True:
                if len(content) <= 0 or start_index >= len(content):
                    break

                end_index = self.get_end_index(start_index+1, content)
                object_content = content[start_index:end_index]

                try:
                    object_type = object_content[0][0]
                    if object_type not in jan9201_objects:
                        logger.critical(
                            f"Invalid object of type {object_type} in userchart {userchart_name}")
                        sys.exit(1)
                except IndexError:
                    logger.critical(
                        f"Invalid object type at row {start_index} in userchart {userchart_name}")
                    sys.exit(1)

                userchart_object = UserchartObject.create(object_content)

                if userchart_object:
                    total_objects = total_objects + 1
                    before_insert = len(ctx.userchart_objects)
                    ctx.userchart_objects.add(userchart_object)
                    ctx.usercharts_objects_by_userchart[userchart_name].usercart_objects.add(
                        userchart_object)
                    after_insert = len(ctx.userchart_objects)
                    if before_insert == after_insert:
                        duplicates = duplicates + 1

                start_index = end_index
        logger.info(
            f"Parsed: {total_objects} objects of which {duplicates} duplicates")


class WriteUserchartToCsv(Command):
    """
        Writes Userchart objects to ecdis csv file.
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'WriteUserchartToCsv'

    def execute(self, ctx):
        import time
        if len(ctx.usercharts) == 0:
            logger.error("No files to write")
            return
        for userchart in ctx.usercharts:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = join(ctx.uchart_work_dir, f"umap_{timestamp}.csv")
            userchart_content_length = len(userchart.content[3:])
            if userchart_content_length == 0:
                logger.error("No content to write. The usermap is empty")
                return

            with open(filename, 'w', newline='') as csvfile:
                csv_writer = csv.writer(
                    csvfile, escapechar='\\', skipinitialspace=True, doublequote=False, dialect='excel')
                # userchart.content[2][0] = f"// USERMAP {timestamp}"
                for row in userchart.content:
                    csv_writer.writerow(row)
            logger.info(f"Writing of \"{filename}\" completed...")
            csvfile.close()
            time.sleep(1)
