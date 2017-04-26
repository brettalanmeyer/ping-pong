from datetime import datetime
from flask import request
import random

def formatTime(seconds):
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	return "%02d:%02d:%02d" % (h, m, s)

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

def paramForm(name, default = None, paramType = None):
	value = None

	if name in request.form:
		value = request.form[name]

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

def shuffle(ary):
	if len(ary) < 2:
		return ary

	newAry = ary[:]
	random.shuffle(newAry)

	if ary == newAry:
		return shuffle(ary)

	return newAry
