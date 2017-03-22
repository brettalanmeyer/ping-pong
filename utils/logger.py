import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

def setupLogging(app):
	if app.config["DEBUG"]:
		handler = RotatingFileHandler(
			app.config["LOG_FILE"],
			maxBytes = 100000,
			backupCount = 1
		)
	else:
		handler = TimedRotatingFileHandler(
			app.config["LOG_FILE"],
			when = app.config["LOG_WHEN"],
			interval = app.config["LOG_INTERVAL"],
			backupCount = app.config["LOG_BACKUP_COUNT"]
		)

	handler.setLevel(logging.INFO)
	formatter = logging.Formatter(app.config["LOG_FORMAT"])
	handler.setFormatter(formatter)
	app.logger.addHandler(handler)
