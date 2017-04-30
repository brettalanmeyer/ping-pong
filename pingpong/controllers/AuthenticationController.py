from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from pingpong.app import login_manager
from pingpong.decorators.LoginRequired import loginRequired
from pingpong.services.AuthenticationService import AuthenticationService
from pingpong.utils import util

authenticationController = Blueprint("authenticationController", __name__)

authenticationService = AuthenticationService()

@authenticationController.route("/login", methods = ["GET"])
def login_form():
	next = util.param("next", "")
	return render_template("authentication/login.html", next = next)

@authenticationController.route("/login", methods = ["POST"])
def login():
	authenticated = authenticationService.authenticate(request.form)

	next = util.paramForm("next", "/")

	if authenticated:
		login_user(authenticationService.admin())
		flash("Welcome, Administrator.", "success")
		return redirect(next)

	else:
		flash("Login information is incorrect.", "danger")
		return render_template("authentication/login.html", next = next), 401

@authenticationController.route("/logout", methods = ["GET"])
def logout():
	if current_user.is_authenticated:
		logout_user()
		flash("You've been logged out.", "success")

	return redirect(url_for("mainController.index"))

@login_manager.user_loader
def load_user(id):
	return authenticationService.admin()
