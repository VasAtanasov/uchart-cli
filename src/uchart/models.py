class EcdisUserchart:
    def __init__(self, content=None, name=None):
        self._content = content if not content == None else list()
        self._name = name
        self._usercart_objects = set()

    @classmethod
    def create_with_name(cls, content, name):
        userchart_content = content if not content == None else list()
        return cls(userchart_content, name)

    @classmethod
    def copy_raw(cls, other):
        if not isinstance(other, cls):
            return NotImplemented
        return cls(name=other.name)

    @property
    def name(self):
        return self._name

    @property
    def content(self):
        return self._content

    @property
    def usercart_objects(self):
        return self._usercart_objects


class UserchartObject:
    def __init__(self, object_type, content,  vertex_start):
        self.object_type = object_type
        self._content = content
        self.vertex_start = vertex_start

    @classmethod
    def create(cls, content):
        object_type = content[0][0]
        vertex_start = 2 if not object_type == "ARROW" else 3
        return cls(object_type, content,  vertex_start)

    @property
    def content(self):
        return self._content

    @property
    def total_lines(self):
        return len(self._content)

    @property
    def vertexes(self):
        return self._content[self.vertex_start:]

    def __str__(self):
        return self.object_type

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return set(self.content) == set(other.content)

    def __hash__(self):
        return hash((frozenset(self.content)))
