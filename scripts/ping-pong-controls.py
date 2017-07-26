import ConfigParser
import requests
import RPi.GPIO as GPIO
import time

config = ConfigParser.ConfigParser()
config.read("config.cfg")

apiKey = config.get("api", "key")
url = config.get("api", "url")

req = requests.session()

buttons = [{
  'color': 'green',
  'pin': 22
}, {
  'color': 'yellow',
  'pin': 24
}, {
  'color': 'red',
  'pin': 27
}, {
  'color': 'blue',
  'pin': 23
}]

def main():
  setup()
  loop()

def setup():
  GPIO.setmode(GPIO.BCM)

  for button in buttons:
    GPIO.setup(button['pin'], GPIO.IN, pull_up_down = GPIO.PUD_UP)

def score(button):
  post('score', button)

def undo(button):
  post('undo', button)

def post(action, button):
  try:
    resource = url.format(button, action)
    req.post(resource, data = { 'key': apiKey })
    print(resource)
  except:
    print('Could not send request')

def input():
  for button in buttons:

    if not GPIO.input(button['pin']):
      seconds = time.time()

      while not GPIO.input(button['pin']):
        pass

      seconds = time.time() - seconds

      if seconds < 0.5:
        score(button['color'])
      else:
        undo(button['color'])
      time.sleep(.250)

def loop():
  while True:
    input()
    time.sleep(.1)

if __name__ == '__main__':
  main()
