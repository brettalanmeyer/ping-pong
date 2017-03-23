import math

class PagingService():

	total = 0
	page = 1
	limit = 10
	pages = 0

	def __init__(self, limit = 10):
		self.limit = limit

	def pager(self, records, page):
		self.page = page
		self.total = records.count()
		self.pages = int(math.ceil(self.total / float(self.limit)))

		return records.limit(self.limit).offset((self.page - 1) * self.limit).all()

	def data(self):
		return {
			"total": self.total,
			"page": self.page,
			"limit": self.limit,
			"pages": self.pages
		}
