import logging
import os
import sys
from abc import ABC, abstractmethod
from .lib import pprint_dict_to_json

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


class ParseFileContent(Command):
    """
        Parses content of file after csv parse.
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'ParseFileContent'

    def get_default_object(self):
        return {
            "name": "",
            "description": "",
            "position": [],
            "attribute": [],
            "type": [],
        }

    def execute(self, ctx):
        content = ctx.content
        types = ctx.types
        collection = ctx.collection

        object_type = None
        obj = None

        for idx, tokens in enumerate(content):

            identifier = tokens[0].lower()

            if identifier == "o":
                obj_type = tokens[1].lower()

                obj = self.get_default_object()
                collection[obj_type].append(obj)

            elif identifier == "a":
                obj["name"] = tokens[1]
                obj["description"] = tokens[2]

            elif identifier == "b":
                psn_obj = {}

                def degrees(tokens):
                    deg, mint, sec, sign = tokens
                    value = int(deg) + (int(mint) + int(sec) / 60) / 60
                    return value if sign.lower() != "w" and sign.lower() != "s" else value * -1

                psn_tokens = tokens[1:]

                psn_obj["latitude"] = degrees(psn_tokens[:4])
                psn_obj["longitude"] = degrees(psn_tokens[4:])

                obj["position"].append(psn_obj)

            elif identifier == "c":

                values = tokens[1:]

                for value in values:
                    obj["attribute"].append(value)

            elif identifier == "d":
                values = tokens[1:]

                for value in values:
                    obj["type"].append(value)


class GenerateXmlFIle(Command):
    """
        Generates xml file from parsed content.
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'GenerateXmlFIle'

    def execute(self, ctx):
        user_map_name, user_map_desc = ctx.content[0]
        collection = ctx.collection

        import xml.etree.ElementTree as ET
        import xml.etree.cElementTree as cET
        from xml.dom import minidom

        userchart = ET.Element('userchart')

        lines = collection["line"]
        if len(lines) > 0:
            line_items = ET.SubElement(userchart, 'lines')

            for line_obj in lines:
                line = ET.SubElement(line_items, 'line')
                line.set("name", line_obj["name"])
                line.set("description", line_obj["description"])

                position = ET.SubElement(line, 'position')
                for id, psn_obj in enumerate(line_obj["position"], start=1):
                    lat, lon = psn_obj.values()
                    vertex = ET.SubElement(position, 'vertex')
                    vertex.set("id", str(id))
                    vertex.set("latitude", f"{lat:.6f}")
                    vertex.set("longitude", f"{lon:.6f}")

                attribute = ET.SubElement(line, 'attribute')
                attribute.set("lineType", line_obj["attribute"][0])

                type = ET.SubElement(line, "type")
                type.set("checkDanger", line_obj["type"][0])
                type.set("displayRadar", line_obj["type"][1])
                type.set("hasNotes", line_obj["type"][2])
                type.set("rangeOfNotes", line_obj["type"][3])

        areas = collection["area"]

        circles = collection["circle"]

        labels = collection["label"]

        # print(ET.tostring(userchart))

        # wrap it in an ElementTree instance, and save as XML
        tree = cET.ElementTree(userchart)

        # Since ElementTree write() has no pretty printing support, used minidom to beautify the xml.
        t = minidom.parseString(ET.tostring(userchart)).toprettyxml()
        tree1 = ET.ElementTree(ET.fromstring(t))

        tree1.write("filename.xml", encoding='utf-8', xml_declaration=True)
        # pprint_dict_to_json(collection)
