import time
import logging
import threading
import warnings
import document
from Queue import Queue

from segment import SegmentThread
from indexs import IndexThread
from rank import RankThread

logging.basicConfig(level=logging.DEBUG)
_log = logging.getLogger(__name__)

docs = {
    "This is not a SQL database. It does not have a relational data model, it does not support SQL queries, and it has no support for indexes.",
    "Only a single process (possibly multi-threaded) can access a particular database at a time.",
    "There is no client-server support builtin to the library. An application that needs such support will have to wrap their own server around the library.",
    " We generally will only accept changes that are both compiled, and tested on a POSIX platform - usually Linux. Very small changes will sometimes be accepted.",
    "All changes must be accompanied by a new (or changed) test, or a sufficient explanation as to why a new (or changed) test is not required."
}


class Googlr:
    def __init__(self, dictionary=None):
        self.terminated = threading.Event()
        self.segment_q = Queue()
        self.index_q = Queue()
        self.rank_q = Queue()
        self.result_q = Queue()
        self.keywords = dict()
        self.indexs = dict()
        self.dl = dict()
        self._dictionary = dictionary
        self.num = 0
        self.avgdl = 0
        self.segment_thread = SegmentThread(self.segment_q, self.keywords, self._dictionary)
        self.indexs_thread = IndexThread(self.index_q, self.indexs, self.keywords, self.rank_q, self.dl, self.avgdl, self.num, self._dictionary)
        self.rank_thread = RankThread(self.rank_q, self.keywords, self.num, self.dl, self.avgdl, self.result_q)

    def add_document(self, doc):
        if doc['id'] is None:
            warnings.warn("Missing id!")
        self.num += 1
        self.segment_q.put(doc)
        self.index_q.put(doc)

    def search_document(self, query):
        self.index_q.put(query)
        return self.result_q.get(block=True, timeout=300)

    def start(self):
        self.segment_thread.start()
        self.indexs_thread.start()
        try:
            while True:
                _log.info("Main thread wait: %s seconds", 2)
                time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
            self.segment_thread.terminate()
            self.segment_thread.join()
            self.indexs_thread.join()
            self.rank_thread.join()

        _log.info("Main thread exits.")


if __name__ == "__main__":
    googlr = Googlr()
    googlr.start()
