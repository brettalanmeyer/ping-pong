import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pingpong import create_app
from pingpong.utils import database as db

from controllers.TestButtonController import TestButtonController
from controllers.TestIsmController import TestIsmController
from controllers.TestLeaderboardController import TestLeaderboardController
from controllers.TestMainController import TestMainController
from controllers.TestMatchController import TestMatchController
from controllers.TestPlayerController import TestPlayerController

import unittest

if __name__ == "__main__":
	unittest.main()

'''
@buttonController.route("/buttons/<path:button>/delete-scores", methods = ["POST"])
@buttonController.route("/buttons/<path:button>/score", methods = ["POST"])
@buttonController.route("/buttons/<path:button>/undo", methods = ["POST"])
@ismController.route("/isms", methods = ["POST"])
@ismController.route("/isms/<int:id>", methods = ["POST"])
@ismController.route("/isms/<int:id>/delete", methods = ["POST"])
@mainController.after_app_request
@mainController.app_errorhandler(404)
@mainController.app_errorhandler(500)
@mainController.before_app_request
@mainController.route("/favicon.ico")
@matchController.route("/matches", methods = ["POST"])
@matchController.route("/matches/<int:id>/num-of-games", methods = ["POST"])
@matchController.route("/matches/<int:id>/play-again", methods = ["POST"])
@matchController.route("/matches/<int:id>/players", methods = ["POST"])
@matchController.route("/matches/<int:id>/undo", methods = ["POST"])
@playerController.route("/players", methods = ["POST"], defaults = { "matchId": None })
@playerController.route("/players/<int:id>", methods = ["POST"])
@playerController.route("/players/matches/<int:matchId>", methods = ["POST"])

'''