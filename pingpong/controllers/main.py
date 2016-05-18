from pingpong import app
from flask import render_template, request

@app.route("/")
def main_index():
	return render_template("main/index.html")
