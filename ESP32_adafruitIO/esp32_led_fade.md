### Stjótna led með analog
``` C
#include "config.h"

int led1 = 2;           // the PWM pin the LED is attached to
int brightness = 0;    // how bright the LED is

AdafruitIO_Feed *led = io.feed("led-one");

void setup() {
  Serial.begin(9600);
  pinMode(led1, OUTPUT);
    // connect to io.adafruit.com
  io.connect();
  led->onMessage(handleMessage);
    // wait for a connection
  while(io.status() < AIO_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println(io.statusText());
  led->get();
}

// the loop routine runs over and over again forever:
void loop() {
  io.run();
  analogWrite(led1, brightness);
}

void handleMessage(AdafruitIO_Data *data) {
  Serial.print("received <- ");
  Serial.print(data->value());
  brightness = atoi(data->value());
}
```
