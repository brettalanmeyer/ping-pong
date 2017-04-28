from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from pingpong.app import login_manager
from pingpong.services.AuthenticationService import AuthenticationService

authenticationController = Blueprint("authenticationController", __name__)

authenticationService = AuthenticationService()

@authenticationController.route("/login", methods = ["GET"])
def login_form():
	return render_template("authentication/login.html")

@authenticationController.route("/login", methods = ["POST"])
def login():
	authenticated = authenticationService.authenticate(request.form)

	if authenticated:
		login_user(authenticationService.admin())
		flash("Welcome, Administrator.", "success")
		return redirect("/")
	else:
		flash("Login information is incorrect.", "danger")
		return render_template("authentication/login.html"), 401

@authenticationController.route("/logout", methods = ["GET"])
@login_required
def logout():
	logout_user()
	flash("You've been logged out.", "success")
	return redirect("/")

@login_manager.user_loader
def load_user(id):
	return authenticationService.admin()
