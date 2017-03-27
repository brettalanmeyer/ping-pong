import logging, re
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

class FilterAppLogs(logging.Filter):
	def filter(self, record):
		return not isIp(record.getMessage())

class FilterAccessLogs(logging.Filter):
	def filter(self, record):
		return isIp(record.getMessage())

def isIp(message):
	matches = re.search("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", message)
	return bool(matches)

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
