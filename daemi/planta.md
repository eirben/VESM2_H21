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
## Kóði fyrir Arduino með rakamæli
```c++

const int AirValue = 620;  
const int WaterValue = 310; 
int soilMoistureValue = 0;
int soilmoisturepercent=0;
void setup() {
  Serial.begin(9600);
}
void loop() {
soilMoistureValue = analogRead(A0);  
//Serial.println(soilMoistureValue);
soilmoisturepercent = map(soilMoistureValue, AirValue, WaterValue, 0, 100);
if(soilmoisturepercent >= 100)
{
  Serial.println("100");
}
else if(soilmoisturepercent <=0)
{
  Serial.println("0");
}
else if(soilmoisturepercent >0 && soilmoisturepercent < 100)
{
  Serial.println(soilmoisturepercent+20);//leiðrétting hjá mér til að fá raka tölu sem næst 100 í vatni má breyta :-)
  
}
  delay(100);
}
```
## Einfaldur kóði til að kveikja og slokkva á dælu
```c++
#define MOTOR 3
void setup() {
  // put your setup code here, to run once:
pinMode(MOTOR,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(MOTOR,HIGH);
  delay(1000);
  digitalWrite(MOTOR,LOW);
  delay(1000);

}
```
