## Kóði fyrir raspberrypi 
takaá móti gögnum frá arduino via serial og senda á Adafruit
```python
#! /bin/env python
import serial
import RPi.GPIO as GPIO
import time
# import Adafruit IO
from Adafruit_IO import *

# Set to your Adafruit IO key.
ADAFRUIT_IO_KEY = ''

# Set to your Adafruit IO username.
ADAFRUIT_IO_USERNAME = ''

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

ser=serial.Serial("/dev/ttyACM0",9600)
ser.baudrate=9600


while True:
	read_ser=ser.readline()
	msg = read_ser.decode('utf-8')
	print(msg)
	time.sleep(100)
	aio.send("myanalog",msg)# ath myanalog er feed hjá mér í Adafruit
```
