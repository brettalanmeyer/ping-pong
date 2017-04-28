from BaseTest import BaseTest

class TestRulesController(BaseTest):

	def test_rules(self):
		rv = self.app.get("/rules")
		assert rv.status == self.ok
