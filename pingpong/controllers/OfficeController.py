from flask import abort
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from pingpong.decorators.LoginRequired import loginRequired
from pingpong.forms.OfficeForm import OfficeForm
from pingpong.services.OfficeService import OfficeService
from pingpong.utils import util

officeController = Blueprint("officeController", __name__)

officeService = OfficeService()
officeForm = OfficeForm()

@officeController.route("/offices/select", methods = ["GET"])
def select():
	session["offices"] = officeService.load()
	return render_template("offices/select.html")

@officeController.route("/offices/set", methods = ["POST"])
def set():
	officeId = util.paramForm("officeId", None, "int")
	office = officeService.selectById(officeId)

	if office == None:
		flash("Please select a valid office", "danger")
		return render_template("offices/select.html"), 400

	session["office"] = {
		"id": int(office.id),
		"city": office.city,
		"state": office.state,
		"key": office.key
	}

	return redirect(util.paramForm("next", "/"))

@officeController.route("/offices/clear", methods = ["GET"])
def clear():
	session.clear()
	return redirect(url_for('officeController.select'))

@officeController.route("/offices", methods = ["GET"])
@loginRequired("officeController.index")
def index():
	offices = officeService.select()
	return render_template("offices/index.html", offices = offices)

@officeController.route("/offices/new", methods = ["GET"])
@loginRequired("officeController.index")
def new():
	office = officeService.new()
	return render_template("offices/new.html", office = office)

@officeController.route("/offices", methods = ["POST"])
@loginRequired("officeController.index")
def create():
	hasErrors = officeForm.validate(request.form)

	if hasErrors:
		office = officeService.new()
		officeForm.load(office, request.form)
		return render_template("offices/new.html", office = office), 400
	else:
		office = officeService.create(request.form)
		flash("Office '{}, {}' has been successfully created.".format(office.city, office.state), "success")
		return redirect(url_for("officeController.index"))

@officeController.route("/offices/<int:id>/edit", methods = ["GET"])
@loginRequired("officeController.index")
def edit(id):
	office = officeService.selectById(id)

	if office == None:
		abort(404)

	return render_template("offices/edit.html", office = office)

@officeController.route("/offices/<int:id>", methods = ["POST"])
@loginRequired("officeController.index")
def update(id):
	office = officeService.selectById(id)

	if office == None:
		abort(404)

	hasErrors = officeForm.validate(request.form)

	if hasErrors:
		officeForm.load(office, request.form)
		return render_template("offices/edit.html", office = office), 400

	else:
		office = officeService.update(id, request.form)
		flash("Office '{}, {}' has been successfully updated.".format(office.city, office.state), "success")
		return redirect(url_for("officeController.index"))

@officeController.route("/offices/<int:id>/enable", methods = ["POST"])
@loginRequired("officeController.index")
def enable(id):
	office = officeService.selectById(id)

	if office == None:
		abort(404)

	officeService.enable(office)

	flash("Office '{}, {}' has been enabled.".format(office.city, office.state), "success")

	return redirect(url_for("officeController.index"))

@officeController.route("/offices/<int:id>/disable", methods = ["POST"])
@loginRequired("officeController.index")
def disable(id):
	office = officeService.selectById(id)

	if office == None:
		abort(404)

	officeService.disable(office)

	flash("Office '{}, {}' has been disabled.".format(office.city, office.state), "success")

	return redirect(url_for("officeController.index"))

@officeController.route("/offices/<int:id>/delete", methods = ["POST"])
@loginRequired("officeController.index")
def delete(id):
	office = officeService.selectById(id)

	if office == None:
		abort(404)

	office, success = officeService.delete(office)

	if success:
		flash("Office '{}, {}' has been successfully deleted.".format(office.city, office.state), "success")
	else:
		flash("Office '{}, {}' could not be deleted.".format(office.city, office.state), "warning")

	return redirect(url_for("officeController.index"))
