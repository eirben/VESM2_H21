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
### h skrá
``` C
#define IO_USERNAME ""
#define IO_KEY ""

#define WIFI_SSID ""
#define WIFI_PASS ""

#include "AdafruitIO_WiFi.h"

#if defined(USE_AIRLIFT) || defined(ADAFRUIT_METRO_M4_AIRLIFT_LITE) ||         \
    defined(ADAFRUIT_PYPORTAL)
// Configure the pins used for the ESP32 connection
#if !defined(SPIWIFI_SS) // if the wifi definition isnt in the board variant
// Don't change the names of these #define's! they match the variant ones
#define SPIWIFI SPI
#define SPIWIFI_SS 10  // Chip select pin
#define SPIWIFI_ACK 9  // a.k.a BUSY or READY pin
#define ESP32_RESETN 6 // Reset pin
#define ESP32_GPIO0 -1 // Not connected
#endif
AdafruitIO_WiFi io(IO_USERNAME, IO_KEY, WIFI_SSID, WIFI_PASS, SPIWIFI_SS,
                   SPIWIFI_ACK, ESP32_RESETN, ESP32_GPIO0, &SPIWIFI);
#else
AdafruitIO_WiFi io(IO_USERNAME, IO_KEY, WIFI_SSID, WIFI_PASS);
#endif
```
