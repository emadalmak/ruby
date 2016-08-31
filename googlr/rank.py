import math
import Queue
import threading


class RankThread(threading.Thread):
    def __init__(self, src, keywords, num, dl, avgdl, result):
        self.src = src
        self.keywords = keywords
        self.num = num
        self.dl = dl
        self.avgdl = avgdl
        self.result = result
        threading.Thread.__init__(self)

    def score(self):
        query = self.src.get()
        l = dict()
        for doc in query.values():
            W = math.log(
                (self.num - float(self.keywords.get(doc.keys())) + 0.5) / (float(self.keywords.get(doc.keys())) + 0.5)
            )
            fi = doc.values()
            K = 1.2 * (0.25 + 0.75 * self.dl.get(doc.keys()) / self.avgdl)
            R = 2.2 * fi / (fi + K)
            score = W * R
            if l.get(doc) is None:
                l.setdefault(doc, score)
            else:
                value = l.get(doc) + score
                dic = {doc: value}
                l.update(dic)
        return l

    def run(self):
        try:
            list = self.score()
            return self.result.put(list)
        except Queue.Empty:
            pass
