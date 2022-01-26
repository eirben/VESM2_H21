## Verkefni 6.2
### Raspberrypi zero með takka, led og adafruit_io
```python

#! /bin/env python
from gpiozero import LED, Button
import time
from Adafruit_IO import *

led = LED(17)
button1 = Button(22)

# Set to your Adafruit IO key.
ADAFRUIT_IO_KEY = ''

# Set to your Adafruit IO username.
ADAFRUIT_IO_USERNAME = ''

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
button = 0

while True:
        if button1.is_pressed:
                button=1
                print("button on")
                led.on()
        else:
                button=0
                print("button off")
                led.off()
        aio.send("button", button)
        time.sleep(1)

```
