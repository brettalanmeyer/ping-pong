import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

def setupLogging(app):
	handler = TimedRotatingFileHandler(
		app.config["LOG_FILE"],
		when = app.config["LOG_WHEN"],
		interval = app.config["LOG_INTERVAL"],
		backupCount = app.config["LOG_BACKUP_COUNT"]
	)
	formatter = logging.Formatter(app.config["LOG_FORMAT"])
	handler.setFormatter(formatter)
	app.logger.setLevel(logging.INFO)
	app.logger.addHandler(handler)
