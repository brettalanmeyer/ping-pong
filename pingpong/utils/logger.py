import logging, re
from logging.handlers import TimedRotatingFileHandler

ACCESS_LEVEL = 60

class FilterAppLogs(logging.Filter):
	def filter(self, record):
		return record.levelno != ACCESS_LEVEL

class FilterAccessLogs(logging.Filter):
	def filter(self, record):
		return record.levelno == ACCESS_LEVEL

def access(self, message, *args, **kws):
	self._log(ACCESS_LEVEL, message, args, **kws)

def setupLogging(app):
	logging.addLevelName(ACCESS_LEVEL, "ACCESS")
	logging.Logger.access = access

	formatter = logging.Formatter(app.config["LOG_FORMAT"])

	handlerApp = TimedRotatingFileHandler(
		app.config["LOG_FILE_APPLICATION"],
		when = app.config["LOG_WHEN"],
		interval = app.config["LOG_INTERVAL"],
		backupCount = app.config["LOG_BACKUP_COUNT"]
	)
	handlerApp.setFormatter(formatter)
	handlerApp.addFilter(FilterAppLogs())

	handlerAccess = TimedRotatingFileHandler(
		app.config["LOG_FILE_ACCESS"],
		when = app.config["LOG_WHEN"],
		interval = app.config["LOG_INTERVAL"],
		backupCount = app.config["LOG_BACKUP_COUNT"]
	)
	handlerAccess.setFormatter(formatter)
	handlerAccess.addFilter(FilterAccessLogs())

	app.logger.addHandler(handlerApp)
	app.logger.addHandler(handlerAccess)
	app.logger.setLevel(logging.INFO)
