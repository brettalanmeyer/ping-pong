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
LOG_FILE_APPLICATION = 'storage/logs/app.log'
LOG_FILE_ACCESS = 'storage/logs/access.log'
LOG_ACCESS_FORMAT = '%(asctime)s %(process)d %(message)s'
LOG_APP_FORMAT = '%(asctime)s %(levelname)s %(process)d %(message)s %(pathname)s:%(lineno)d:%(funcName)s()'
LOG_WHEN = 'midnight'
LOG_INTERVAL = 1
LOG_BACKUP_COUNT = 14
SKYPE_URL = ''
ELO_K_VALUE = 32
ELO_PERFORMANCE_RATING = 1500
ADMIN_USERNAME = ''
ADMIN_PASSWORD = ''
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_FROM_NAME = ''
MAIL_FROM_EMAIL = ''
MAIL_RECIPIENTS = ['']
SESSION_TYPE = 'filesystem'
SESSION_FILE_DIR = 'pingpong/storage/sessions'
SESSION_FILE_THRESHOLD = 500
PERMANENT_SESSION_LIFETIME = 31536000
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


## Raspberry pi

* run script `/home/pi/ping-pong/ping-pong-controls.py`

## TODO

* avatars on doubles score board
* Fix doubles opponent stats
* Make method names consistent: deleteByMatch(match) or deleteByMatchId(id)
* manual entry of scores due to connection lost or otherwise

Raspberry pi resolution: 1184x624

sudo systemctl restart|stop|enable|disable|start darts|ping-pong|skype-messenger
