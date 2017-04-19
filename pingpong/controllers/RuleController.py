from flask import Blueprint
from flask import render_template
from pingpong.utils.cache import cache

ruleController = Blueprint("ruleController", __name__)

@ruleController.route("/rules", methods = ["GET"])
@cache.cached(timeout = 60)
def rules():
	return render_template("rules/index.html")
