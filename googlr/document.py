class Document:

    def __init__(self, id):
        self.id = id

    def __str__(self):
        return self.id


class Field:
    def __init__(self, score=None, max_length=None, index=True, **kwargs):
        self.score = score
        self.max_length = max_length
        self.index = index


class TextField(Field):

    def __init__(self, **kwargs):
        Field.__init__(self, **kwargs)
        self.index = True


class TimeField(Field):

    def __init__(self, **kwargs):
        Field.__init__(self, **kwargs)
        self.index = False

