import json
import time
import paho.mqtt.client as mqtt
import board
import busio

import adafruit_tsl2591

from gpiozero import LED

i2c = busio.I2C(board.SCL, board.SDA)

# Initialize the sensor.
sensor = adafruit_tsl2591.TSL2591(i2c)

led = LED(17)
id ='d454db61-7ddb-44ee-922b-777973d899c4'
client_name = id + 'nightlight_client'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    if payload['led_on']:
       led.on()
    else:
       led.off()

mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_command
mqtt_client.loop_start()

print("MQTT connected!")
while True:
	# Read and calculate the light level in lux.
	# lux = sensor.lux
	# print("Total light: {0}lux".format(lux))
	# You can also read the raw infrared and visible light levels.
	# These are unsigned, the higher the number the more light of that type.
	# There are no units like lux.
	# Infrared levels range from 0-65535 (16-bit)
	# infrared = sensor.infrared
	# print("Infrared light: {0}".format(infrared))
	# Visible-only levels range from 0-2147483647 (32-bit)
	visible = sensor.visible
	telemetry = json.dumps({'light' : visible})
	print("Sending telemetry " , telemetry)
	mqtt_client.publish(client_telemetry_topic, telemetry)
	time.sleep(5)
	# if(visible <  600000):
	#	led.on()
	# else:
	#	led.off()
	# print("Visible light: {0}".format(visible))
	# Full spectrum (visible + IR) also range from 0-2147483647 (32-bit)
	# full_spectrum = sensor.full_spectrum
	# print("Full spectrum (IR + visible) light: {0}".format(full_spectrum))
	# print('Light level: ', visible)
	# print("Visible light: {0}".format(visible))
	# time.sleep(1)
