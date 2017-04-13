from flask import current_app as app
import requests
import threading

def doPost(url, message):
	try:
		requests.post(url, data = { "message": message })
	except:
		pass

def send(message):
	app.logger.info("Skype message being sent %s", message)
	t = threading.Thread(target = doPost, args = (app.config["SKYPE_URL"], message))
	t.daemon = True
	t.start()
