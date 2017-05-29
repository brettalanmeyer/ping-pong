from flask import current_app as app
from pingpong.services.OfficeService import OfficeService
import requests
import threading

officeService = OfficeService()

def doPost(url, message, recipients):
	try:
		requests.post(url, data = { "message": message, "recipients": recipients })
	except:
		pass

def getRecipients(officeIds):
	recipients = []

	if isinstance(officeIds, list):
		offices = officeService.selectByIds(officeIds)
		for office in offices:
			if office.hasSkypeChatId():
				recipients.append(office.skypeChatId)

	else:
		recipients.append(officeIds)

	return recipients

def send(message, officeIds):
	app.logger.info("Skype message being sent %s", message)
	t = threading.Thread(target = doPost, args = (app.config["SKYPE_URL"], message, getRecipients(officeIds)))
	t.daemon = True
	t.start()
