class BaseObject:
    def __init__(self, object_type, total_lines, comments_count):
        self.object_type = object_type
        self.content = []
        self.total_lines = total_lines
        self.comments_count = comments_count

    def __str__(self):
        return self.object_type


class BaseEcdisModel:
    def __init__(self, header):
        self.content = header


class Symbol(BaseObject):
    def __init__(self, obj_type, total_lines, comments_count):
        BaseObject.__init__(self, obj_type, total_lines, comments_count)


class DangerSymbol(BaseObject):
    def __init__(self, obj_type, total_lines, comments_count):
        BaseObject.__init__(self, obj_type, total_lines, comments_count)


class LineAggregate(BaseObject):
    def __init__(self, obj_type, total_lines, comments_count):
        BaseObject.__init__(self, obj_type, total_lines, comments_count)


class LineCircle(BaseObject):
    def __init__(self, obj_type, total_lines, comments_count):
        BaseObject.__init__(self, obj_type, total_lines, comments_count)


class LineEllipse(BaseObject):
    def __init__(self, obj_type, total_lines, comments_count):
        BaseObject.__init__(self, obj_type, total_lines, comments_count)


class Arc(BaseObject):
    def __init__(self, obj_type, total_lines, comments_count):
        BaseObject.__init__(self, obj_type, total_lines, comments_count)


class DangerLineAggregate(BaseObject):
    def __init__(self, obj_type, total_lines, comments_count):
        BaseObject.__init__(self, obj_type, total_lines, comments_count)


class Arrow(BaseObject):
    def __init__(self, obj_type, total_lines, comments_count):
        BaseObject.__init__(self, obj_type, total_lines, comments_count)


class Polygon(BaseObject):
    def __init__(self, obj_type, total_lines, comments_count):
        BaseObject.__init__(self, obj_type, total_lines, comments_count)


class Circle(BaseObject):
    def __init__(self, obj_type, total_lines, comments_count):
        BaseObject.__init__(self, obj_type, total_lines, comments_count)


class Ellipse(BaseObject):
    def __init__(self, obj_type, total_lines, comments_count):
        BaseObject.__init__(self, obj_type, total_lines, comments_count)


class Fan(BaseObject):
    def __init__(self, obj_type, total_lines, comments_count):
        BaseObject.__init__(self, obj_type, total_lines, comments_count)


class DangerArea(BaseObject):
    def __init__(self, obj_type, total_lines, comments_count):
        BaseObject.__init__(self, obj_type, total_lines, comments_count)


class Text(BaseObject):
    def __init__(self, obj_type, total_lines, comments_count):
        BaseObject.__init__(self, obj_type, total_lines, comments_count)
