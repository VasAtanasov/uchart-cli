import logging

from .models import Jan9201Object
from .constants import *

logger = logging.getLogger(__name__)


class Jan9201ObjectFactory:

    def create_static_object(self, content, index, obj_type, total_lines, comments_count, vertex_start=5):
        obj = Jan9201Object(obj_type, total_lines,
                            comments_count, vertex_start)
        obj.content = content[index: index + obj.total_lines]
        return obj

    def create_dynamic_object(self,  content, index, obj_type, comments_count, vertex_start=5):

        def index_of_end(current_content):
            for i, t in enumerate(current_content):
                if len(t) > 0 and t[0] == "END":
                    return i
        last_line = index_of_end(content[index:])

        if last_line == None:
            return None

        total_lines = (last_line + 1)
        obj = Jan9201Object(obj_type, total_lines,
                            comments_count, vertex_start)
        obj.content = content[index: index + obj.total_lines]
        return obj

    def get_object(self, row, index, content):
        obj = None
        if len(row) > 0 and row[0].startswith("// SYMBOL"):
            obj = self.create_static_object(
                content, index, symbol, six, three)
        elif len(row) > 0 and row[0].startswith("// DANGER_SYMBOL"):
            obj = self.create_static_object(
                content, index, danger_symbol, six, three)
        elif len(row) > 0 and row[0].startswith("// LINE_AGGREGATE"):
            obj = self.create_dynamic_object(
                content, index, line_aggregate, four, six)
        elif len(row) > 0 and row[0].startswith("// LINE_CIRCLE"):
            obj = self.create_static_object(
                content, index, line_circle, six, three)
        elif len(row) > 0 and row[0].startswith("// LINE_ELLIPSE"):
            obj = self.create_static_object(
                content, index, line_ellipse, six, three)
        elif len(row) > 0 and row[0].startswith("// ARC"):
            obj = self.create_static_object(
                content, index, arc, six, three)
        elif len(row) > 0 and row[0].startswith("// DANGER_LINE_AGGREGATE"):
            obj = self.create_dynamic_object(
                content, index, danger_line_aggregate, four, six)
        elif len(row) > 0 and row[0].startswith("// ARROW"):
            obj = self.create_static_object(
                content, index, arrow, ten, five, 8)
        elif len(row) > 0 and row[0].startswith("// POLYGON"):
            obj = self.create_dynamic_object(
                content, index, polygon, three)
        elif len(row) > 0 and row[0].startswith("// CIRCLE"):
            obj = self.create_static_object(
                content, index, circle, six, three)
        elif len(row) > 0 and row[0].startswith("// ELLIPSE"):
            obj = self.create_static_object(
                content, index, ellipse, six, three)
        elif len(row) > 0 and row[0].startswith("// FAN"):
            obj = self.create_static_object(
                content, index, fan, six, three)
        elif len(row) > 0 and row[0].startswith("// DANGER_AREA"):
            obj = self.create_dynamic_object(
                content, index, danger_area, three)
        elif len(row) > 0 and row[0].startswith("// TEXT"):
            obj = self.create_static_object(
                content, index, text, six, three)
        return obj
