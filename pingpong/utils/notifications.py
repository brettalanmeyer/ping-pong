from flask import current_app as app
from flask_mail import Mail
from flask_mail import Message
from pingpong.app import app as context
from pingpong.decorators.Async import async
from pingpong.services.OfficeService import OfficeService
import requests
import threading

officeService = OfficeService()

def getRecipients(officeIds):
	recipients = []

	if isinstance(officeIds, list):
		offices = officeService.selectByIds(officeIds)
		for office in offices:
			if office.hasSkypeChatId():
				recipients.append(office.skypeChatId)

	else:
		office = officeService.selectById(officeIds)
		recipients.append(office.skypeChatId)

	return recipients

def mailError( message):
	app.logger.info("Sending Error Email...")

	subject = "Ping Pong App ERROR"
	body = "Ping Pong App ERROR\nMessage: {}".format(message)
	html = "<h2>Ping Pong App ERROR</h2><p>Message: {}".format(message)
	mail(subject, body, html)

def mailFeedback(name, email, message):
	app.logger.info("Sending Feedback...")

	subject = "Ping Pong App Feedback"
	body = "Ping Pong App Feedback\nName: {}\nEmail: {}\n\n{}".format(name, email, message)
	html = "<h2>Ping Pong App Feedback</h2><p>Name: {}<br />Email: {}<p><p>{}</p>".format(name, email, message)
	mail(subject, body, html)

def send(message, officeIds):
	app.logger.info("Skype message being sent %s", message)
	url = app.config["SKYPE_URL"]
	recipients = getRecipients(officeIds)
	doSend(app, url, message, recipients)

def mail(subject, body, html):
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

	doMail(mail, messages)

@async
def doSend(app, url, message, recipients):
	requests.post(url, data = { "message": message, "recipients": recipients })

@async
def doMail(mail, messages):
	with context.app_context():
		mail.send(messages)
