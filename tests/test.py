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
