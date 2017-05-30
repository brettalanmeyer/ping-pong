from BaseTest import BaseTest
from pingpong.services.MailService import MailService

mailService = MailService()

class TestMailService(BaseTest):

	def test_sendFeedback(self):
		with self.ctx:
			mailService.sendFeedback("Send Feedback Name", "brettmeyerxpx@gmail.com", "Send Feedback Message")
