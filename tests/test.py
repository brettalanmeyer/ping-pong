import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pingpong.app import app
from pingpong.utils import database as db

from controllers.TestAdminController import TestAdminController
from controllers.TestApiButtonController import TestApiButtonController
from controllers.TestApiController import TestApiController
from controllers.TestAuthenticationController import TestAuthenticationController
from controllers.TestErrorController import TestErrorController
from controllers.TestIsmController import TestIsmController
from controllers.TestLeaderboardController import TestLeaderboardController
from controllers.TestMainController import TestMainController
from controllers.TestMatchController import TestMatchController
from controllers.TestOfficeController import TestOfficeController
from controllers.TestPlayerController import TestPlayerController

from services.TestGameService import TestGameService
from services.TestIsmService import TestIsmService
from services.TestMatchService import TestMatchService
from services.TestOfficeService import TestOfficeService
from services.TestPagingService import TestPagingService
from services.TestPlayerService import TestPlayerService
from services.TestScoreService import TestScoreService
from services.TestTeamService import TestTeamService

from matchtypes.TestDoubles import TestDoubles
from matchtypes.TestNines import TestNines
from matchtypes.TestSingles import TestSingles

from forms.TestFeedbackForm import TestFeedbackForm
from forms.TestIsmForm import TestIsmForm
from forms.TestOfficeForm import TestOfficeForm
from forms.TestPlayerForm import TestPlayerForm

from utils.TestUtil import TestUtil

import unittest

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding("UTF8")

	unittest.main()

# rv.response
# rv.headers
# rv.status_code
# rv.direct_passthrough
# rv.charset
# rv.data
# rv.default_mimetype
# rv.location