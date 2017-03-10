import Service
from models import PlayerModel
from datetime import datetime

class PlayerService(Service.Service):

	def __init__(self):
		Service.Service.__init__(self, PlayerModel.PlayerModel)

	def select(self):
		return self.session.query(self.model).order_by(self.model.name)

	def selectById(self, id):
		return self.session.query(self.model).filter(self.model.id == id).one()

	def selectByName(self, name):
		return self.session.query(self.model).filter_by(name = name)

	def new(self):
		return self.model("", None, None)

	def create(self, form):
		player = self.model(form["name"], datetime.now(), datetime.now())
		self.session.add(player)
		self.session.commit()

		return player

	def update(self, id, name):
		player = self.selectById(id)
		player.name = name
		player.modifiedAt = datetime.now()
		self.session.commit()

		return player

	def excludeByName(self, id, name):
		return self.session.query(self.model).filter(self.model.id != id, self.model.name == name)

