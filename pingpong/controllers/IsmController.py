from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from pingpong.services.IsmService import IsmService

ismController = Blueprint("ismController", __name__)

ismService = IsmService()

@ismController.route("/isms", methods = ["GET"])
def isms():
	return render_template("isms/index.html", isms = ismService.select())

@ismController.route("/isms.json", methods = ["GET"])
def isms_json():
	isms = ismService.select()
	return Response(ismService.serialize(isms), status = 200, mimetype = "application/json")

@ismController.route("/isms/new", methods = ["GET"])
def isms_new():
	ism = ismService.new()
	return render_template("isms/new.html", ism = ism)

@ismController.route("/isms", methods = ["POST"])
def isms_create():
	ism = ismService.create(request.form)
	flash("Ism '{}' has been successfully created.".format(ism.saying), "success")
	return redirect("/isms")

@ismController.route("/isms/<int:id>/edit", methods = ["GET"])
def isms_edit(id):
	ism = ismService.selectById(id)

	if ism == None:
		flash("Ism {} does not exist.".format(id), "warning")
		return redirect("/isms")

	return render_template("isms/edit.html", ism = ism)

@ismController.route("/isms/<int:id>", methods = ["POST"])
def isms_update(id):
	ism = ismService.update(id, request.form)
	flash("Ism '{}' has been successfully updated.".format(ism.saying), "success")
	return redirect("/isms")

@ismController.route("/isms/<int:id>/delete", methods = ["POST"])
def isms_delete(id):
	ism = ismService.delete(id)
	flash("Ism '{}' has been successfully deleted.".format(ism.saying), "success")
	return redirect("/isms")