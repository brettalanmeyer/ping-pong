# Ping Pong

## Installation

Install dependencies by running `sudo pip install -r requirements.txt`

## Configuration

	create config.cfg

		DEBUG = False
		ASSETS_DEBUG = False
		HOST = '0.0.0.0'
		PORT = 5000
		SECRET_KEY = ''
		MYSQL_USERNAME = ''
		MYSQL_PASSWORD = ''
		MYSQL_HOST = ''
		MYSQL_DATABASE = ''
		LOG_FILE_APPLICATION = 'logs/app.log'
		LOG_FILE_ACCESS = 'logs/access.log'
		LOG_FORMAT = '%(asctime)s %(levelname)s %(process)d %(message)s %(pathname)s:%(lineno)d:%(funcName)s()'
		LOG_WHEN = 'midnight'
		LOG_INTERVAL = 1
		LOG_BACKUP_COUNT = 14


## Raspberry pi

* run script `/home/pi/ping-pong/ping-pong-controls.py`

TODO

Remove audio
ELO rating system
Fix doubles opponent stats

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
