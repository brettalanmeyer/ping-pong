import Service
from models import IsmModel
from datetime import datetime

class IsmService(Service.Service):

	def __init__(self, session):
		Service.Service.__init__(self, session, IsmModel.IsmModel)

	def select(self):
		return self.session.query(self.model).filter(self.model.approved == True)

	def selectById(self, id):
		return self.session.query(self.model).filter(self.model.id == id).one()

	def new(self):
		return self.model(0, 0, "", False, None, None)

	def create(self, form):
		ism = self.model(form["left"], form["right"], form["saying"], False, datetime.now(), datetime.now())
		self.session.add(ism)
		self.session.commit()

		return ism

	def update(self, id, form):
		ism = self.selectById(id)
		ism.left = form["left"]
		ism.right = form["right"]
		ism.saying = form["saying"]
		ism.approved = False
		ism.modifiedAt = datetime.now()
		self.session.commit()

		return ism

	def delete(self, id):
		ism = self.selectById(id)
		self.session.delete(ism)
		self.session.commit()

		return ism

	def serialize(self, isms):
		data = []

		for ism in isms:
			data.append({
				"id": int(ism.id),
				"left": int(ism.left),
				"right": int(ism.right),
				"saying": ism.saying
			})

		return data