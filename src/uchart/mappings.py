from .constants import *
from .models import UserchartObject


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


symbols_jan9201_to_jan901b = {
    '~WARNSY0': '~WARNSY6',
    '~CIRCLE0': '~CIRCLE6',
    '~TRIANG0': '~TRIANG6',
    '~SQUARE0': '~SQUARE6',
    '~DIAMND0': '~DIAMND6',
    '~XSHAPE0': '~XSHAPE6',
}


mappings = {
    'SYMBOL': 'SYMBOL',
    'DANGER_SYMBOL': 'SYMBOL',
    'ALARM_SYMBOL': 'SYMBOL',
    'CAUTION_SYMBOL': 'SYMBOL',
    'LINE_AGGREGATE': 'LINE',
    'LINE_CIRCLE': 'CIRCLE',
    'LINE_ELLIPSE': 'ELLIPSE',
    'ARC': 'ARC',
    'DANGER_LINE_AGGREGATE': 'DANGER_LINE',
    'ALARM_LINE_AGGREGATE': 'DANGER_LINE',
    'CAUTION_LINE_AGGREGATE': 'DANGER_LINE',
    'ARROW': None,
    'POLYGON': 'POLYGON',
    'CIRCLE': 'CIRCLE',
    'ELLIPSE': 'ELLIPSE',
    'FAN': 'FAN',
    'DANGER_AREA': 'DANGER_AREA',
    'ALARM_AREA': 'DANGER_AREA',
    'CAUTION_AREA': 'DANGER_AREA',
    'TEXT': 'TEXT',
}


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
    content = list(map(list, obj.content))
    current_symbol = obj.content[3][1]
    new_symbol = symbols_jan9201_to_jan901b[current_symbol]
    obj.content[3][1] = new_symbol

    if obj.object_type == danger_symbol:
        obj.content[3][0] = symbol

    return obj


def map_line_aggregate(obj):
    if obj.object_type not in mappings:
        return None

    new_object_type = mappings[obj.object_type]

    if new_object_type == None:
        return None

    new_content = list(map(list, obj.content))
    new_content[0][0] = new_object_type
    for i in range(obj.vertex_start, len(obj.content)):
        new_content[i] = new_content[i][:6]

    a = 5
    return UserchartObject.create(content=tuple(map(tuple, new_content)))


def map_line_circle(obj):
    obj.content[0][0] = '// CIRCLE'
    obj.content[3][0] = 'CIRCLE'
    return obj


def map_line_ellipse(obj):
    obj.content[0][0] = '// ELLIPSE'
    obj.content[3][0] = 'ELLIPSE'
    return obj


object_mappers = {
    # 'SYMBOL': map_symbol,
    'LINE_AGGREGATE': map_line_aggregate
}
