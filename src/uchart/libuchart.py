from .constants import *
from .models import UserchartObject

def uchart_plugin(plugin_class):
    """
        A decorator that registers uchart plugins
    """
    if not hasattr(uchart_plugin, 'plugins'):
        setattr(uchart_plugin, 'plugins', [])
    getattr(uchart_plugin, 'plugins').append(plugin_class)


jan901B_line = [
    ['// LINE', 'InstName'],
    ['// Comment'],
    ['// Lat', '', '', 'Lon', 'Add "END" to the end of vertex.'],
    ['LINE', '***'],
]

jan901B_danger_line = [
    ['// DANGER_LINE'],
    ['// Comment'],
    ['// Lat', '', '', 'Lon', 'Add "END" to the end of vertex.'],
    ['DANGER_LINE'],
]


def map_objects(objects):
    mapped_objects = list()

    for obj in objects:
        obj_type = obj.object_type

        current_obj = None
        if obj_type == symbol or obj_type == danger_symbol:
            current_obj = map_symbol(obj)
        elif obj_type == line_aggregate:
            current_obj = map_line_aggregate(obj)
        elif obj_type == line_circle:
            current_obj = map_line_circle(obj)
        elif obj_type == line_ellipse:
            current_obj = map_line_ellipse(obj)
        elif obj_type == danger_line_aggregate:
            current_obj = map_line_aggregate(obj)
        elif obj_type in [arc, polygon, circle, ellipse, fan, danger_area, text]:
            current_obj = obj

        if current_obj:
            mapped_objects.append(current_obj)

    return mapped_objects


def map_symbol(obj):
    current_symbol = obj.content[3][1]
    new_symbol = symbols_jan9201_to_jan901b[current_symbol]
    obj.content[3][1] = new_symbol

    if obj.object_type == danger_symbol:
        obj.content[3][0] = symbol

    return obj


def map_line_aggregate(obj):
    total_lines = obj.total_lines - 1
    line_obj = UserchartObject(line, total_lines, three)

    line_obj.content.extend(obj.content[obj.comments_count + 1:])

    for i in range(5, len(line_obj.content)):
        line_obj.content[i] = line_obj.content[i][:6]

    return line_obj


def map_line_circle(obj):
    obj.content[0][0] = '// CIRCLE'
    obj.content[3][0] = 'CIRCLE'
    return obj


def map_line_ellipse(obj):
    obj.content[0][0] = '// ELLIPSE'
    obj.content[3][0] = 'ELLIPSE'
    return obj
