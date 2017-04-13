from flask import Blueprint
from flask import render_template

ruleController = Blueprint("ruleController", __name__)

@ruleController.route("/rules", methods = ["GET"])
def rules():
	return render_template("rules/index.html")
