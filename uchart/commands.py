import logging
import os
import sys
from abc import ABC, abstractmethod
from .lib import pprint_dict_to_json
from .constants import *

logger = logging.getLogger(__name__)


def get_default_object():
    return {
        "name": "",
        "description": "",
        "position": [],
        "attribute": [],
        "type": [],
    }


def get_default_type_notes():
    return ["0", "0", "0", "0"]


def get_default_type_range():
    return {
        "checkDanger": "0",
        "displayRadar": "0",
        "hasNotes": "0",
        "rangeOfNotes": "1.000000"
    }


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

    def execute(self, ctx):
        content = ctx.content
        types = ctx.types
        collection = ctx.collection

        ctx.user_map_name = content[0][0]
        ctx.user_map_desc = content[0][1]

        object_type = None
        obj = None

        for idx, tokens in enumerate(content):

            identifier = tokens[0].lower()

            if identifier == "o":
                obj_type = tokens[1].lower()

                obj = get_default_object()
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


class ParseJAN9201Content(Command):
    """
        Parses JRC JAN 9201 ECDIS csv usermap file.
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'ParseJAN9201Content'

    def get_static_content(self, content, index, total_lines):
        return content[index: index + total_lines]

    def get_dynamic_content(self, clazz, content, index, obj_type, comments_count):
        total_lines = (content[index:].index(['END']) + 1)
        obj = clazz(obj_type, total_lines, comments_count)
        obj.content = content[index: index + obj.total_lines]
        return obj

    def execute(self, ctx):
        content = ctx.content
        collection = ctx.collection

        ctx.user_map_name = content[2][0][3:]
        ctx.user_map_desc = content[2][1]

        def degrees(tokens):
            deg, mint, sign = tokens
            value = int(deg) + (float(mint) / 60)
            return value if sign.lower() != "w" and sign.lower() != "s" else value * -1

        index = 0
        while True:
            if len(content) <= 0 or index >= len(content):
                break

            row = content[index]
            object_type = None
            obj = None

            if len(row) > 0 and row[0].startswith("// SYMBOL"):
                pass
            elif len(row) > 0 and row[0].startswith("// DANGER_SYMBOL"):
                pass
            elif len(row) > 0 and row[0].startswith("// LINE_AGGREGATE"):

                obj = create_dynamic_object(
                    LineAggregate, content, index, line_aggregate, four)

            elif len(row) > 0 and row[0].startswith("// LINE_CIRCLE"):
                obj = create_static_object(LineCircle, content, index, line_circle, six,
                                           three)
            elif len(row) > 0 and row[0].startswith("// LINE_ELLIPSE"):
                obj = create_static_object(LineEllipse, content, index, line_ellipse, six,
                                           three)
            elif len(row) > 0 and row[0].startswith("// ARC"):
                obj = create_static_object(Arc, content, index, arc, six,
                                           three)
            elif len(row) > 0 and row[0].startswith("// DANGER_LINE_AGGREGATE"):
                obj = create_dynamic_object(DangerLineAggregate, content, index, danger_line_aggregate,
                                            four)
            elif len(row) > 0 and row[0].startswith("// ARROW"):
                obj = create_static_object(
                    Arrow, content, index, arrow, ten, five)
            elif len(row) > 0 and row[0].startswith("// POLYGON"):
                obj = create_dynamic_object(
                    Polygon, content, index, polygon, three)
            elif len(row) > 0 and row[0].startswith("// CIRCLE"):
                obj = create_static_object(Circle, content, index, circle, six,
                                           three)
            elif len(row) > 0 and row[0].startswith("// ELLIPSE"):
                obj = create_static_object(Ellipse, content, index, ellipse, six,
                                           three)
            elif len(row) > 0 and row[0].startswith("// FAN"):
                obj = create_static_object(Fan, content, index, fan, six,
                                           three)
            elif len(row) > 0 and row[0].startswith("// DANGER_AREA"):
                obj = create_dynamic_object(
                    DangerArea, content, index, danger_area, three)
            elif len(row) > 0 and row[0].startswith("// TEXT"):
                obj = get_default_object()
                object_type = "label"

                content = self.get_static_content(content, index, six)

                label_text = content[3][1]

                psn_tokens = content[5][:6]
                psn_obj = {}
                psn_obj["latitude"] = degrees(psn_tokens[:3])
                psn_obj["longitude"] = degrees(psn_tokens[3:])
                obj["position"].append(psn_obj)
                obj["attribute"].append("1")
                obj["attribute"].append(label_text)
                obj["type"] = get_default_type_notes()

            if obj:
                collection[object_type].append(obj)

            index = index + 1

class ParseXmlFIle(Command):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'GenerateXmlFIle'

    def execute(self, ctx):
        collection = ctx.collection

class GenerateXmlFIle(Command):
    """
        Generates xml file from parsed content.
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'GenerateXmlFIle'

    def execute(self, ctx):
        collection = ctx.collection

        import xml.etree.ElementTree as ET
        import xml.etree.cElementTree as cET
        from xml.dom import minidom

        userchart = ET.Element('userchart')
        userchart.set("name", ctx.user_map_name)
        userchart.set("description", ctx.user_map_desc)
        userchart.set("version", "1.0")

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
        if len(areas) > 0:
            area_items = ET.SubElement(userchart, 'areas')

            for area_obj in areas:
                area = ET.SubElement(area_items, 'area')
                area.set("name", area_obj["name"])
                area.set("description", area_obj["description"])

                position = ET.SubElement(area, 'position')
                for id, psn_obj in enumerate(area_obj["position"], start=1):
                    lat, lon = psn_obj.values()
                    vertex = ET.SubElement(position, 'vertex')
                    vertex.set("id", str(id))
                    vertex.set("latitude", f"{lat:.6f}")
                    vertex.set("longitude", f"{lon:.6f}")

                type = ET.SubElement(area, "type")
                type.set("checkDanger", area_obj["type"][0])
                type.set("displayRadar", area_obj["type"][1])
                type.set("hasNotes", area_obj["type"][2])
                type.set("notesType", area_obj["type"][3])

        circles = collection["circle"]
        if len(circles) > 0:
            circle_items = ET.SubElement(userchart, 'circles')

            for circle_obj in circles:
                circle = ET.SubElement(circle_items, 'circle')
                circle.set("name", circle_obj["name"])
                circle.set("description", circle_obj["description"])

                position = ET.SubElement(circle, 'position')
                for id, psn_obj in enumerate(circle_obj["position"], start=1):
                    lat, lon = psn_obj.values()
                    vertex = ET.SubElement(position, 'vertex')
                    vertex.set("id", str(id))
                    vertex.set("latitude", f"{lat:.6f}")
                    vertex.set("longitude", f"{lon:.6f}")

                attribute = ET.SubElement(circle, 'attribute')
                range = float(circle_obj["attribute"][0])
                attribute.set("range", f"{range:.6f}")

                type = ET.SubElement(circle, "type")
                type.set("checkDanger", circle_obj["type"][0])
                type.set("displayRadar", circle_obj["type"][1])
                type.set("hasNotes", circle_obj["type"][2])
                type.set("notesType", circle_obj["type"][3])

        labels = collection["label"]
        if len(labels) > 0:
            label_items = ET.SubElement(userchart, "labels")

            for label_obj in labels:
                label = ET.SubElement(label_items, 'label')
                label.set("name", label_obj["name"])
                label.set("description", label_obj["description"])

                position = ET.SubElement(label, 'position')
                for id, psn_obj in enumerate(label_obj["position"], start=1):
                    lat, lon = psn_obj.values()
                    vertex = ET.SubElement(position, 'vertex')
                    vertex.set("id", str(id))
                    vertex.set("latitude", f"{lat:.6f}")
                    vertex.set("longitude", f"{lon:.6f}")

                attribute = ET.SubElement(label, 'attribute')
                attribute.set("labelStyle", label_obj["attribute"][0])
                attribute.set("labelText", label_obj["attribute"][1])

                type = ET.SubElement(label, "type")
                type.set("checkDanger", label_obj["type"][0])
                type.set("displayRadar", label_obj["type"][1])

        tree = cET.ElementTree(userchart)

        t = minidom.parseString(ET.tostring(userchart)).toprettyxml()
        tree1 = ET.ElementTree(ET.fromstring(t))

        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"umap_{timestamp}.xml"
        tree1.write(file_name, encoding='utf-8',  xml_declaration=True)
        logger.info(f"Generated: {file_name}")
