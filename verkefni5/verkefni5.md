## Lausn á verkefni 5.2
### Kóði publischer
```python

import json
import time
import paho.mqtt.client as mqtt

id = 'd454db61-7ddb-44ee-922b-777973d899c4' # einstakt id fengið t.d hér https://www.uuidgenerator.net/

client_telemetry_topic = id + '/telemetry' # default áskrift en gæti verið t.d /telementary/lightsensor
server_command_topic = id + '/commands' # áskrift command til að kveikja á led annari tölvu
client_name = id + 'nightlight_server' # getur verið hvað sem er sem er lýsandi :-) hvað client er að gera

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()
# fall sem tekur á móti og sendir skilaboð eða skipanir
def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)
    command = { 'led_on' : payload['light'] < 400000}# gildi sem kemur frá TSl2591 lightsensor (hágildi :-)
    print("Sending message:", command)
    client.publish(server_command_topic, json.dumps(command))


mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(2)# sendir og tekur á móti boðum á 2 sek fresti
 
 ```
### Kóði raspberrypi zero
```python
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
	visible = sensor.visible
	telemetry = json.dumps({'light' : visible})
	print("Sending telemetry " , telemetry)
	mqtt_client.publish(client_telemetry_topic, telemetry)
	time.sleep(5)
```
