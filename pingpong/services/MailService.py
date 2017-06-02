from flask_mail import Mail
from flask_mail import Message
from flask import current_app as app

class MailService():

	def sendFeedback(self, name, email, message):
		app.logger.info("Sending Feedback...")

		subject = "Ping Pong App Feedback"
		body = "Ping Pong App Feedback\nName: {}\nEmail: {}\n\n{}".format(name, email, message)
		html = "<h2>Ping Pong App Feedback</h2><p>Name: {}<br />Email: {}<p><p>{}</p>".format(name, email, message)
		self.send(subject, body, html)

	def send(self, subject, body, html):
		sender = (app.config["MAIL_FROM_NAME"], app.config["MAIL_FROM_EMAIL"])
		recipients = app.config["MAIL_RECIPIENTS"]

		app.logger.info("\
			Sending Mail...\n\
			FROM: %s\n\
			TO: %s\n\
			SUBJECT: %s\n\
			BODY: %s\n\
			HTML: %s\
		", sender, recipients, subject, body, html)

		mail = Mail(app)
		messages = Message(subject, sender = sender, recipients = recipients)
		messages.body = body
		messages.html = html
		mail.send(messages)

		app.logger.info("Mail Sent")
