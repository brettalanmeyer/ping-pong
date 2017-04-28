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

Get code coverage
`python -m unittest discover -s tests/`

`coverage run -m unittest discover -s tests/`

Open coverage report
`coverage report -m`

Open coverage report
`coverage html`
browse and open `html_cov/index.html`


## Raspberry pi

* run script `/home/pi/ping-pong/ping-pong-controls.py`

TODO

Fix doubles opponent stats
move generate data to another file and route only in debug mode
put getMatchType() somewhere shared
try to put skype stuff in this app if possible
Put ELO on match score board?

Finish Tests - try to revert all data entered from a certain point
create a default admin dashboard

Login redirect, for post requests, try to be able to configure it where to redirect, such as /players instead of /players/3/delete

Make method names consistent: deleteByMatch(match) or deleteByMatchId(id)

add numbers in order to elo on leaderboard (Cole is 1, Matt is 2, Dave is 13, etc)

make matchesController.matches_delete prettier

generate screenshots for greg
Put "login" in top right except for game boards
Add admin section for deleting players, isms, and matches. Players button is disabled until matches have been deleted.
Copy data from remote database to dev database only if config values exist this way it only works in dev

Add selectApproved() to isms so we have something to select all

Report of avg time people play per day

Report of ELO with variability of initial rank and k value


manual entry of scores due to connection lost or otherwise


Add Dave Thomas


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
