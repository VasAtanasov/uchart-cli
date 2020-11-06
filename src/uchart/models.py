class EcdisUserchart:
    def __init__(self, content=None):
        if content == None:
            content = [
                ['// USER CHART SHEET exported by JRC ECDIS.'],
                ['// <<NOTE>>This strings // indicate comment column/cells. You can edit freely.'],
                ['// USERMAP', '', '']
            ]
        self._content = content
        self._usercart_objects = set()

    @property
    def content(self):
        return self._content

    @property
    def usercart_objects(self):
        return self._usercart_objects


class UserchartObject:
    def __init__(self, object_type, content, total_lines, vertex_start):
        self.object_type = object_type
        self._content = content
        self.total_lines = total_lines
        self.vertex_start = vertex_start

    @classmethod
    def create(cls, content):
        object_type = content[0][0]
        vertex_start = 2 if not object_type == "ARROW" else 3
        total_lines = len(content)
        return cls(object_type, content, total_lines, vertex_start)

    @property
    def content(self):
        return self._content

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
