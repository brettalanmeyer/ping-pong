import Service, logging
from models import IsmModel
from datetime import datetime

logger = logging.getLogger(__name__)

class IsmService(Service.Service):

	def __init__(self, session):
		logger.info("Initializing Ism Service")
		Service.Service.__init__(self, session, IsmModel.IsmModel)

	def select(self):
		logger.info("Selecting isms")

		return self.session.query(self.model).filter(self.model.approved == True)

	def selectById(self, id):
		logger.info("Selecting ism=%d", id)

		return self.session.query(self.model).filter(self.model.id == id).one()

	def new(self):
		logger.info("New ism")

		return self.model(0, 0, "", False, None, None)

	def create(self, form):
		ism = self.model(form["left"], form["right"], form["saying"], False, datetime.now(), datetime.now())
		self.session.add(ism)
		self.session.commit()

		logger.info("Creating ism=%d left=%d right=%d saying=%s", ism.id, ism.left, ism.right, ism.saying)

		return ism

	def update(self, id, form):

		ism = self.selectById(id)
		ism.left = form["left"]
		ism.right = form["right"]
		ism.saying = form["saying"]
		ism.approved = False
		ism.modifiedAt = datetime.now()
		self.session.commit()

		logger.info("Updating ism=%d left=%d right=%d saying=%s", ism.id, ism.left, ism.right, ism.saying)

		return ism

	def delete(self, id):
		logger.info("Deleting ism=%d", id)

		ism = self.selectById(id)
		self.session.delete(ism)
		self.session.commit()

		return ism

	def serialize(self, isms):
		logger.info("Serializing isms")

		data = []

		for ism in isms:
			data.append({
				"id": int(ism.id),
				"left": int(ism.left),
				"right": int(ism.right),
				"saying": ism.saying
			})

		return data
