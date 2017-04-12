from flask import Blueprint, render_template, Response, redirect, request
from pingpong.services import IsmService

ismController = Blueprint("ismController", __name__)
ismService = IsmService.IsmService()

@ismController.route("/isms", methods = ["GET"])
def isms():
	isms = ismService.select()
	return render_template("isms/index.html", isms = isms)

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
	ismService.create(request.form)
	return redirect("/isms")

@ismController.route("/isms/<int:id>/edit", methods = ["GET"])
def isms_edit(id):
	ism = ismService.selectById(id)
	return render_template("isms/edit.html", ism = ism)

@ismController.route("/isms/<int:id>", methods = ["POST"])
def isms_update(id):
	ismService.update(id, request.form)
	return redirect("/isms")

@ismController.route("/isms/<int:id>/delete", methods = ["POST"])
def isms_delete(id):
	ismService.delete(id)
	return redirect("/isms")
