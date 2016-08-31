import jieba
import time
import Queue
import logging
import threading

logging.basicConfig(level=logging.INFO)
_log = logging.getLogger(__name__)


class SegmentThread(threading.Thread):
	def __init__(self, src, dest, dictionary=None):
		self.src = src
		self.dest = dest
		self.dictionary = dictionary
		self.terminated = threading.Event()
		threading.Thread.__init__(self)

	def run(self):
		if self.dictionary is not None:
			jieba.load_userdict(self.dictionary)
		while not self.terminated.isSet():
			try:
				doc = self.src.get(block=False)
				keywords = jieba.cut_for_search(doc.content)
				for keyword in set(keywords):
					if self.dest.get(keyword) is None:
						self.dest.setdefault(keyword, 1)
					else:
						count = self.dest.get(keyword) + 1
						dic = {keyword: count}
						self.dest.update(dic)
					_log.info("Segment keywords: %s", keyword)
			except Queue.Empty:
				time.sleep(1)

	def terminate(self):
		_log.info("Segment thread terminate.")
		self.terminated.set()

