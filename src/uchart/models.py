class BaseEcdisModel:
    def __init__(self, header):
        self.content = header


class Jan901B(BaseEcdisModel):
    def __init__(self, header):
        BaseEcdisModel.__init__(self, header)


class Jan9021(BaseEcdisModel):
    def __init__(self, header):
        BaseEcdisModel.__init__(self, header)

    def __init__(self):
        header = [
            ['// USER CHART SHEET exported by JRC ECDIS.'],
            ['// <<NOTE>>This strings // indicate comment column/cells. You can edit freely.'],
            ['// USERMAP', '', '']
        ]
        BaseEcdisModel.__init__(self, header)


class Jan9201Object:
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
        return set(self.content) == set(other.content)

    def __hash__(self):
        return hash((frozenset(self.content)))
