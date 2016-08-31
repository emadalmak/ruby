import os
import jieba
import logging
import Queue
import threading
from document import Document

logging.basicConfig(level=logging.INFO)
_log = logging.getLogger(__name__)


class NotExistException(Exception):
    pass


class IndexThread(threading.Thread):
    def __init__(self, src, indexs, keywords, rank, dl, avgdl, num, dictionary=None):
        self.src = src
        self.indexs = indexs
        self.keywords = keywords
        self.rank = rank
        self.dl = dl
        self.avgdl = avgdl
        self.num = num
        self.dictionary = dictionary
        threading.Thread.__init__(self)

    def run(self):
        try:
            item = self.src.get()
            if isinstance(item, str):
                result = dict()
                item = self.src.get()
                keywords = jieba.cut_for_search(item)
                for keyword in set(keywords):
                    if self.indexs.get(keyword):
                        if result.get(keyword) is None:
                            result.setdefault(keyword, self.indexs.get(keyword))
                self.rank.put(result)
            elif isinstance(item, Document):
                words = jieba.cut_for_search(item)
                self.dl.setdefault(item.id, len(words))
                self.avgdl = (self.avgdl * (self.num - 1) + len(words)) * self.num
                for keyword in self.keywords:
                    for word in words:
                        if word == keyword:
                            if self.indexs.get(keyword) is None:
                                self.indexs.setdefault(keyword, {item.id: 1})
                            else:
                                count = self.indexs.get(keyword).values() + 1
                                dic = {keyword, {item.id: count}}
                                self.indexs.update(dic)
        except Queue.Empty:
            pass
