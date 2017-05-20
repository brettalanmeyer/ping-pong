from flask_mail import Mail
from flask_mail import Message
from flask import current_app as app

class MailService():

	def sendFeedback(self, name, message):
		subject = "Ping Pong App Feedback"
		body = "body"
		html = "html"
		self.send(subject, body, html)

	def send(self, subject, body, html):
		sender = (app.config["MAILER_FROM_NAME"], app.config["MAILER_FROM_EMAIL"])
		recipients = app.config["MAILER_RECIPIENT_EMAILS"]

		mail = Mail(app)
		messages = Message(subject, sender = sender, recipients = recipients)
		messages.body = body
		messages.html = html
		mail.send(messages)
