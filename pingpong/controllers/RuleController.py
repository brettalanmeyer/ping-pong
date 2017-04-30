from flask import Blueprint
from flask import render_template

ruleController = Blueprint("ruleController", __name__)

@ruleController.route("/rules", methods = ["GET"])
def index():
	return render_template("rules/index.html")
