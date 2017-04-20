# Ping Pong

## Installation

Update Server

	`sudo apt-get update`

Install git

	`sudo apt-get install git`

Install mysql

	`sudo apt-get install mysql-server`
	`sudo nano /etc/mysql/my.cnf`
		bind-address = LOCALMACHINEIP


Virtual Box
	`sudo apt-get install virtualbox-guest-dkms`
	`sudo gpasswd -a <linux-username> vboxsf`

Install pip

	`sudo apt-get install python-pip python-dev build-essential`
	`sudo pip install --upgrade pip`
	`sudo pip install --upgrade virtualenv`
	`sudo apt-get install libmysqlclient-dev`

Install app dependencies by running `sudo pip install -r requirements.txt`

## Configuration

	create config.cfg

		DEBUG = True
		DEBUG_TOOLS = True
		ASSETS_DEBUG = False
		HOST = '0.0.0.0'
		PORT = 5010
		SECRET_KEY = ''
		LOG_FILE_APPLICATION = 'logs/app.log'
		LOG_FILE_ACCESS = 'logs/access.log'
		LOG_ACCESS_FORMAT = '%(asctime)s %(process)d %(message)s'
		LOG_APP_FORMAT = '%(asctime)s %(levelname)s %(process)d %(message)s %(pathname)s:%(lineno)d:%(funcName)s()'
		LOG_WHEN = 'midnight'
		LOG_INTERVAL = 1
		LOG_BACKUP_COUNT = 14
		SKYPE_URL = ''
		ELO_K_VALUE = 32
		ELO_PERFORMANCE_RATING = 1500

	create dbconfig.cfg

		[db]
		mysql_username =
		mysql_password =
		mysql_host =
		mysql_database =
		pool_recycle = 3600
		autocommit = False
		autoflush = False


## Raspberry pi

* run script `/home/pi/ping-pong/ping-pong-controls.py`

TODO

Make UNDO a global button on the app - also bind to "U" button

merge models/Base.py and utils/database.py
Fix doubles opponent stats
move generate data to another file and route only in debug mode
put getMatchType() somewhere shared
try to put skype stuff in this app if possible
ELO previous rank, +-

Leaderboard:
	current win/loss streak
	current point streak
	highest win/lost streak
	highest point streak

Delegate Python Process
	screen python run.py
	Ctrl-a then d
List Screen Processes
	screen -ls
Kill Screen Process
	screen -X -S PID quit

Raspberry pi resolution
1184x624