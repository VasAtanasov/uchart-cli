symbol = 'SYMBOL'
six = 6
ten = 10
three = 3
four = 4
five = 5
danger_symbol = 'DANGER_SYMBOL'
line_aggregate = 'LINE_AGGREGATE'
line_circle = 'LINE_CIRCLE'
line_ellipse = 'LINE_ELLIPSE'
arc = 'ARC'
danger_line_aggregate = 'DANGER_LINE_AGGREGATE'
arrow = 'ARROW'
polygon = 'POLYGON'
circle = 'CIRCLE'
ellipse = 'ELLIPSE'
fan = 'FAN'
danger_area = 'DANGER_AREA'
text = 'TEXT'
line = 'LINE'


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

jan9201_objects = [
    "SYMBOL",
    "DANGER_SYMBOL",
    "ALARM_SYMBOL",
    "CAUTION_SYMBOL",
    "LINE_AGGREGATE",
    "LINE_CIRCLE",
    "LINE_ELLIPSE",
    "ARC",
    "DANGER_LINE_AGGREGATE",
    "ALARM_LINE_AGGREGATE",
    "CAUTION_LINE_AGGREGATE",
    "ARROW",
    "POLYGON",
    "CIRCLE",
    "ELLIPSE",
    "FAN",
    "DANGER_AREA",
    "ALARM_AREA",
    "CAUTION_AREA",
    "TEXT",
]

jan901b_objects = [
    'SYMBOL',
    'LINE',
    'ARC',
    'DANGER_LINE',
    'POLYGON',
    'CIRCLE',
    'ELLIPSE',
    'FAN',
    'DANGER_AREA',
    'TEXT',
    'END',
]

dynamic_objects = [
    "LINE_AGGREGATE",
    "DANGER_LINE_AGGREGATE",
    "ALARM_LINE_AGGREGATE",
    "CAUTION_LINE_AGGREGATE",
    "POLYGON",
    "DANGER_AREA"
    "ALARM_AREA"
    "CAUTION_AREA"
]
