from flask import redirect
from flask import request
from flask import url_for
from flask_login import current_user
from functools import update_wrapper

def loginRequired(endpoint = None):
	def decorator(fn):
		def wrapped_function(*args, **kwargs):

			if not current_user.is_authenticated:
				if endpoint == None:
					next = url_for(request.endpoint)
				else:
					next = url_for(endpoint)

				return redirect(url_for("authenticationController.login", next = next))

			return fn(*args, **kwargs)

		return update_wrapper(wrapped_function, fn)
	return decorator
