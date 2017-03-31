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

Instead of a team winning and losing, just make it so that win is true or false
display winner better
after completion, select play again option, best of 1,3,5 with keep teams option

Delegate Python Process
	screen python run.py
	Ctrl-a then d
List Screen Processes
	screen -ls
Kill Screen Process
	screen -X -S PID quit
