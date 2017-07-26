# RaspberryPi Configuration

### Set resolution to 1920x1080

Backup and modify config file
`/boot/config.txt`
`disable_overscan=1`
`hdmi_group=1`
`hdmi_mode=34`

### Connect to wifi

Backup files and copy configs from this directory
`/etc/wpa_supplicant/wpa_supplicant.conf`
`/etc/network/interfaces`

### Button script

Copy python script to local directory
Edit rc.local and add
`python DIRECTORY/ping-pong-controls.py`

### Configuration

create config.cfg
```
[api]
key = apikey
```