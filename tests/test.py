import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pingpong.app import app
from pingpong.utils import database as db

from controllers.TestAdminController import TestAdminController
from controllers.TestAuthenticationController import TestAuthenticationController
from controllers.TestButtonController import TestButtonController
from controllers.TestErrorController import TestErrorController
from controllers.TestIsmController import TestIsmController
from controllers.TestLeaderboardController import TestLeaderboardController
from controllers.TestMainController import TestMainController
from controllers.TestMatchController import TestMatchController
from controllers.TestPlayerController import TestPlayerController
from controllers.TestRulesController import TestRulesController

from services.TestIsmService import TestIsmService
from services.TestMatchService import TestMatchService
from services.TestPlayerService import TestPlayerService

import unittest

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding("UTF8")

	unittest.main()
