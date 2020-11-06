import logging

from .models import UserchartObject
from .constants import *

logger = logging.getLogger(__name__)


class UserchartObjectFactory:

    def create_static_object(self, content, index, obj_type, total_lines, comments_count, vertex_start=5):

        obj = UserchartObject(obj_type,
                              total_lines,
                              comments_count,
                              vertex_start)

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

        obj = UserchartObject(obj_type,
                              total_lines,
                              comments_count,
                              vertex_start)

        obj.content = content[index: index + obj.total_lines]
        return obj



    def get_object(self, row, start_index, content):
        obj = None

        end_index = self.get_end_index(start_index+1, content)

        objet_content = content[start_index:end_index]

        if len(row) > 0 and row[0].startswith("// SYMBOL"):
            obj = self.create_static_object(
                content,
                start_index,
                symbol,
                six,
                three)
        elif len(row) > 0 and row[0].startswith("// DANGER_SYMBOL"):
            obj = self.create_static_object(
                content,
                start_index,
                danger_symbol,
                six,
                three)
        elif len(row) > 0 and row[0] in dynamic_objects:
            obj = self.create_dynamic_object(
                content, start_index, row[0], four, six)
        elif len(row) > 0 and row[0].startswith("// LINE_CIRCLE"):
            obj = self.create_static_object(
                content, start_index, line_circle, six, three)
        elif len(row) > 0 and row[0].startswith("// LINE_ELLIPSE"):
            obj = self.create_static_object(
                content, start_index, line_ellipse, six, three)
        elif len(row) > 0 and row[0].startswith("// ARC"):
            obj = self.create_static_object(
                content, start_index, arc, six, three)
        elif len(row) > 0 and row[0].startswith("// DANGER_LINE_AGGREGATE"):
            obj = self.create_dynamic_object(
                content, start_index, danger_line_aggregate, four, six)
        elif len(row) > 0 and row[0].startswith("// ARROW"):
            obj = self.create_static_object(
                content, start_index, arrow, ten, five, 8)
        elif len(row) > 0 and row[0].startswith("// POLYGON"):
            obj = self.create_dynamic_object(
                content, start_index, polygon, three)
        elif len(row) > 0 and row[0].startswith("// CIRCLE"):
            obj = self.create_static_object(
                content, start_index, circle, six, three)
        elif len(row) > 0 and row[0].startswith("// ELLIPSE"):
            obj = self.create_static_object(
                content, start_index, ellipse, six, three)
        elif len(row) > 0 and row[0].startswith("// FAN"):
            obj = self.create_static_object(
                content, start_index, fan, six, three)
        elif len(row) > 0 and row[0].startswith("// DANGER_AREA"):
            obj = self.create_dynamic_object(
                content, start_index, danger_area, three)
        elif len(row) > 0 and row[0].startswith("// TEXT"):
            obj = self.create_static_object(
                content, start_index, text, six, three)
        return obj
