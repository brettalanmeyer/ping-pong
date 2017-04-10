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

ELO rating system
Fix doubles opponent stats
Be able to undo after match
move generate data to another file and route only in debug mode

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
