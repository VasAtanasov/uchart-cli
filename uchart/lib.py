#!/usr/bin/env python
from uchart.constants import *
from uchart.models import *


def parse_jan9201_content(content):
    objects = list()

    index = 0
    while True:
        if len(content) <= 0 or index >= len(content):
            break

        row = content[index]
        obj = None
        if len(row) > 0 and row[0].startswith("// SYMBOL"):
            obj = create_static_object(
                Symbol, content, index, symbol, six, three)
        elif len(row) > 0 and row[0].startswith("// DANGER_SYMBOL"):
            obj = create_static_object(DangerSymbol, content, index, danger_symbol, six,
                                       three)
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
            obj = create_static_object(Text, content, index, text, six,
                                       three)

        if obj:
            objects.append(obj)

        index = index + 1

    return objects


def create_static_object(clazz, content, index, obj_type, total_lines, comments_count):
    obj = clazz(obj_type, total_lines, comments_count)
    obj.content = content[index: index + obj.total_lines]
    return obj


def create_dynamic_object(clazz, content, index, obj_type, comments_count):
    total_lines = (content[index:].index(['END']) + 1)
    obj = clazz(obj_type, total_lines, comments_count)
    obj.content = content[index: index + obj.total_lines]
    return obj
