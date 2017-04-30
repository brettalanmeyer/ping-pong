from flask import abort
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from flask import url_for
from flask_login import current_user
from pingpong.decorators.LoginRequired import loginRequired
from pingpong.forms.IsmForm import IsmForm
from pingpong.services.IsmService import IsmService

ismController = Blueprint("ismController", __name__)

ismService = IsmService()
ismForm = IsmForm()

@ismController.route("/isms", methods = ["GET"])
def index():
	if current_user.is_authenticated:
		isms = ismService.select()
	else:
		isms = ismService.selectApproved()

	return render_template("isms/index.html", isms = isms)

@ismController.route("/isms.json", methods = ["GET"])
def index_json():
	isms = ismService.select()
	return Response(ismService.serialize(isms), status = 200, mimetype = "application/json")

@ismController.route("/isms/new", methods = ["GET"])
def new():
	ism = ismService.new()
	return render_template("isms/new.html", ism = ism)

@ismController.route("/isms", methods = ["POST"])
def create():
	hasErrors = ismForm.validate(request.form)

	if hasErrors:
		ism = ismService.new()
		ismForm.load(ism, request.form)
		return render_template("isms/new.html", ism = ism), 400
	else:
		ism = ismService.create(request.form)
		flash("Ism '{}' has been successfully created.".format(ism.saying), "success")
		return redirect(url_for("ismController.index"))

@ismController.route("/isms/<int:id>/edit", methods = ["GET"])
def edit(id):
	ism = ismService.selectById(id)

	if ism == None:
		abort(404)

	return render_template("isms/edit.html", ism = ism)

@ismController.route("/isms/<int:id>", methods = ["POST"])
def update(id):
	ism = ismService.selectById(id)

	if ism == None:
		abort(404)

	hasErrors = ismForm.validate(request.form)

	if hasErrors:
		ismForm.load(ism, request.form)
		return render_template("isms/edit.html", ism = ism), 400

	else:
		ism = ismService.update(id, request.form)
		flash("Ism '{}' has been successfully updated.".format(ism.saying), "success")
		return redirect(url_for("ismController.index"))

@ismController.route("/isms/<int:id>/approve", methods = ["POST"])
@loginRequired("ismController.index")
def approve(id):
	ism = ismService.selectById(id)

	if ism == None:
		abort(404)

	ismService.approve(ism)

	flash("Ism '{}' has been approved.".format(ism.saying), "success")

	return redirect(url_for("ismController.index"))

@ismController.route("/isms/<int:id>/reject", methods = ["POST"])
@loginRequired("ismController.index")
def reject(id):
	ism = ismService.selectById(id)

	if ism == None:
		abort(404)

	ismService.reject(ism)

	flash("Ism '{}' has been rejected.".format(ism.saying), "success")

	return redirect(url_for("ismController.index"))

@ismController.route("/isms/<int:id>/delete", methods = ["POST"])
@loginRequired("ismController.index")
def delete(id):
	ism = ismService.selectById(id)

	if ism == None:
		abort(404)

	ism, success = ismService.delete(ism)

	if success:
		flash("Ism '{}' has been successfully deleted.".format(ism.saying), "success")
	else:
		flash("Ism '{}' could not be deleted.".format(ism.saying), "warning")

	return redirect(url_for("ismController.index"))
