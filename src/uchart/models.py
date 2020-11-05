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
    def __init__(self, object_type, total_lines, comments_count, vertex_start=5):
        self.object_type = object_type
        self.content = ()
        self.total_lines = total_lines
        self.comments_count = comments_count
        self.vertex_start = vertex_start

    def __str__(self):
        return self.object_type

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return set(self.content[self.comments_count:]) == set(other.content[self.comments_count:])

    def __hash__(self):
        return hash((frozenset(self.content[self.comments_count:])))
