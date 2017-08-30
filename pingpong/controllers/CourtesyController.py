from flask import abort
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from flask import session
from flask import url_for
from flask_login import current_user
from pingpong.decorators.LoginRequired import loginRequired
from pingpong.forms.CourtesyForm import CourtesyForm
from pingpong.services.CourtesyService import CourtesyService

courtesyController = Blueprint("courtesyController", __name__)

courtesyService = CourtesyService()
courtesyForm = CourtesyForm()

@courtesyController.route("/courtesies", methods = ["GET"])
def index():
	if current_user.is_authenticated:
		courtesies = courtesyService.select(session["office"]["id"])
	else:
		courtesies = courtesyService.selectApproved(session["office"]["id"])

	return render_template("courtesies/index.html", courtesies = courtesies)

@courtesyController.route("/courtesies.json", methods = ["GET"])
def index_json():
	if current_user.is_authenticated:
		courtesies = courtesyService.select(session["office"]["id"])
	else:
		courtesies = courtesyService.selectApproved(session["office"]["id"])

	return Response(courtesyService.serialize(courtesies), status = 200, mimetype = "application/json")

@courtesyController.route("/courtesies/new", methods = ["GET"])
def new():
	courtesy = courtesyService.new()
	return render_template("courtesies/new.html", courtesy = courtesy)

@courtesyController.route("/courtesies", methods = ["POST"])
def create():
	hasErrors = courtesyForm.validate(request.form)

	if hasErrors:
		courtesy = courtesyService.new()
		courtesyForm.load(courtesy, request.form)
		return render_template("courtesies/new.html", courtesy = courtesy), 400
	else:
		courtesy = courtesyService.create(session["office"]["id"], request.form)
		flash("Courtesy '{}' has been successfully created.".format(courtesy.text), "success")
		return redirect(url_for("courtesyController.index"))

@courtesyController.route("/courtesies/<int:id>/edit", methods = ["GET"])
def edit(id):
	courtesy = courtesyService.selectById(id)

	if courtesy == None:
		abort(404)

	return render_template("courtesies/edit.html", courtesy = courtesy)

@courtesyController.route("/courtesies/<int:id>", methods = ["POST"])
def update(id):
	courtesy = courtesyService.selectById(id)

	if courtesy == None:
		abort(404)

	hasErrors = courtesyForm.validate(request.form)

	if hasErrors:
		courtesyForm.load(courtesy, request.form)
		return render_template("courtesies/edit.html", courtesy = courtesy), 400

	else:
		courtesy = courtesyService.update(id, request.form)
		flash("Courtesy '{}' has been successfully updated.".format(courtesy.text), "success")
		return redirect(url_for("courtesyController.index"))

@courtesyController.route("/courtesies/<int:id>/approve", methods = ["POST"])
@loginRequired("courtesyController.index")
def approve(id):
	courtesy = courtesyService.selectById(id)

	if courtesy == None:
		abort(404)

	courtesyService.approve(courtesy)

	flash("Courtesy '{}' has been approved.".format(courtesy.text), "success")

	return redirect(url_for("courtesyController.index"))

@courtesyController.route("/courtesies/<int:id>/reject", methods = ["POST"])
@loginRequired("courtesyController.index")
def reject(id):
	courtesy = courtesyService.selectById(id)

	if courtesy == None:
		abort(404)

	courtesyService.reject(courtesy)

	flash("Courtesy '{}' has been rejected.".format(courtesy.text), "success")

	return redirect(url_for("courtesyController.index"))

@courtesyController.route("/courtesies/<int:id>/delete", methods = ["POST"])
@loginRequired("courtesyController.index")
def delete(id):
	courtesy = courtesyService.selectById(id)

	if courtesy == None:
		abort(404)

	courtesy, success = courtesyService.delete(courtesy)

	if success:
		flash("Courtesy '{}' has been successfully deleted.".format(courtesy.text), "success")
	else:
		flash("Courtesy '{}' could not be deleted.".format(courtesy.text), "warning")

	return redirect(url_for("courtesyController.index"))
