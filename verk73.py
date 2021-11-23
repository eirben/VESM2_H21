import time
import board
import adafruit_tsl2591
from gpiozero import LED, Button
from Adafruit_IO import *
# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# Set to your Adafruit IO key.
ADAFRUIT_IO_KEY = 'aio_gWeG51X0EhIummCzIWTc0Dsqvq79'

# Set to your Adafruit IO username.
ADAFRUIT_IO_USERNAME = 'eirben'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
# Initialize the sensor.
sensor = adafruit_tsl2591.TSL2591(i2c)

while True:
    # Read and calculate the light level in lux.
    lux = sensor.lux
    print("Total light: {0}lux".format(lux))
    aio.send("lightsensor", lux)
    time.sleep(5)
