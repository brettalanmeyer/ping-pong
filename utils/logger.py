import logging, re
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

class FilterAppLogs(logging.Filter):
	def filter(self, record):
		return not record.getMessage().startswith("10.")

class FilterAccessLogs(logging.Filter):
	def filter(self, record):
		return record.getMessage().startswith("10.")

def setupLogging(app):
	formatter = logging.Formatter(app.config["LOG_FORMAT"])

	handler = TimedRotatingFileHandler(
		app.config["LOG_FILE_APPLICATION"],
		when = app.config["LOG_WHEN"],
		interval = app.config["LOG_INTERVAL"],
		backupCount = app.config["LOG_BACKUP_COUNT"]
	)
	handler.setFormatter(formatter)
	handler.addFilter(FilterAppLogs())
	app.logger.addHandler(handler)

	handler2 = TimedRotatingFileHandler(
		app.config["LOG_FILE_ACCESS"],
		when = app.config["LOG_WHEN"],
		interval = app.config["LOG_INTERVAL"],
		backupCount = app.config["LOG_BACKUP_COUNT"]
	)
	handler2.setFormatter(formatter)
	handler2.addFilter(FilterAccessLogs())
	app.logger.addHandler(handler2)
