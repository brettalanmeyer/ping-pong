# Ping Pong

## Installation

Update Server

`sudo apt-get update`

Install git

`sudo apt-get install git`

Install mysql

`sudo apt-get install mysql-server`

`sudo nano /etc/mysql/my.cnf`

```bind-address = LOCALMACHINEIP```


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
```
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
SEASON_START_YEAR = 2000
SEASON_START_MONTH = 1
ADMIN_USERNAME = ''
ADMIN_PASSWORD = ''
```

create dbconfig.cfg

```
[db]
mysql_username =
mysql_password =
mysql_host =
mysql_database =
pool_recycle = 3600
autocommit = False
autoflush = False
```

## Testing

Run tests
`python tests/test.py`

Run coverage
`coverage run --source=pingpong tests/test.py`

Generate coverage report
`coverage report -m`

Generate html coverage report
`coverage html`

Run single class
`cd test/
`python -m unittest matchtypes.TestSingles`


## Raspberry pi

* run script `/home/pi/ping-pong/ping-pong-controls.py`

## TODO

* Switch avatars when switching sides for singles
* add link to leaderboard for each matchtype to notifications when a matches end
* avatars on doubles score board
* put getMatchType() somewhere shared
* Finish Tests - try to create sqlite engine for testing db
* Fix doubles opponent stats
* Make method names consistent: deleteByMatch(match) or deleteByMatchId(id)
* manual entry of scores due to connection lost or otherwise
* Put ELO on match score board?
* Report of avg time people play per day
* Report of ELO with variability of initial rank and k value
* smack talk AI
* Dave Thomas
* try to put skype stuff in this app if possible
* win streak
* loss streak
* remove points on nines
* possibly remove 0 stat players from main leaderboard, or at least put them in rows below footer


Delegate Python Process
	screen python run.py
	Ctrl-a then d
List Screen Processes
	screen -ls
Kill Screen Process
	screen -X -S PID quit

Raspberry pi resolution
1184x624
