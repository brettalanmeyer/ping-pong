from datetime import datetime
from flask import request

def param(name, default = None, paramType = None):
	value = request.args.get(name)

	if value == None:
		value = default

	if value != None and paramType != None:
		if paramType == "int":
			value = int(value)
		elif paramType == "str":
			value = str(value)

	return value

def jsonSerial(obj):
	if isinstance(obj, datetime):
		return str(obj)