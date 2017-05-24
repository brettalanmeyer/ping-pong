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
MYSQL_REMOTE_USERNAME = ''
MYSQL_REMOTE_PASSWORD = ''
MYSQL_REMOTE_HOST = ''
MYSQL_REMOTE_DATABASE = ''
UNDO_ALLOWED_ADDRESS = ''
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_FROM_NAME = ''
MAIL_FROM_EMAIL = ''
MAIL_RECIPIENTS = ['']
SESSION_TYPE = 'filesystem'
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

* Add title attributes to skype messages
* Multiple offices - generate an unexposed api key for each office that can only be given out by admin
* Changelog page - add link to main page
* Maybe say how many points winner of nines had left
* Add avatars to skype messages as base 64 encoded
* avatars on doubles score board
* Fix doubles opponent stats
* Make method names consistent: deleteByMatch(match) or deleteByMatchId(id)
* manual entry of scores due to connection lost or otherwise

Delegate Python Process
	screen python run.py
	Ctrl-a then d
List Screen Processes
	screen -ls
Kill Screen Process
	screen -X -S PID quit

Raspberry pi resolution
1184x624


SELECT players.name, DATE(matches.createdAt) as date, SEC_TO_TIME(SUM(TIME_TO_SEC(matches.completedAt) - TIME_TO_SEC(matches.createdAt))) AS timediff, group_concat(matches.id) as matches
FROM matches
LEFT JOIN teams ON matches.id = teams.matchId
LEFT JOIN teams_players ON teams.id = teams_players.teamId
LEFT JOIN players ON teams_players.playerId = players.id
WHERE matches.complete = 1 and matches.matchType = 'nines'
GROUP BY YEAR(matches.createdAt), MONTH(matches.createdAt), Day(matches.createdAt), players.id
ORDER BY date, players.name