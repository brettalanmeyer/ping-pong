from flask import Blueprint, render_template

rulesController = Blueprint("rulesController", __name__)

@rulesController.route("/rules", methods = ["GET"])
def rules():
	return render_template("rules/index.html")