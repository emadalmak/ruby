import googlr
from googlr import document

docs = [
    "This is not a SQL database. It does not have a relational data model, it does not support SQL queries, and it has no support for indexes.",
    "Only a single process (possibly multi-threaded) can access a particular database at a time.",
    "There is no client-server support builtin to the library. An application that needs such support will have to wrap their own server around the library.",
    " We generally will only accept changes that are both compiled, and tested on a POSIX platform - usually Linux. Very small changes will sometimes be accepted.",
    "All changes must be accompanied by a new (or changed) test, or a sufficient explanation as to why a new (or changed) test is not required."
]


class MyDocument(document.Document):
    content = document.TextField(score=5)
    create = document.TimeField()

for doc in docs:
    document = MyDocument(content=doc)
    googlr.add_document(document)

googlr.search("blabla")

