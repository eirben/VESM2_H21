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

// uncomment the following line if you are using airlift
//#define USE_AIRLIFT

// uncomment the following line if you are using winc1500
// #define USE_WINC1500

// comment out the following lines if you are using fona or ethernet
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
/******************************* FONA **************************************/

// the AdafruitIO_FONA client will work with the following boards:
//   - Feather 32u4 FONA -> https://www.adafruit.com/product/3027

// uncomment the following two lines for 32u4 FONA,
// and comment out the AdafruitIO_WiFi client in the WIFI section
// #include "AdafruitIO_FONA.h"
// AdafruitIO_FONA io(IO_USERNAME, IO_KEY);

/**************************** ETHERNET ************************************/

// the AdafruitIO_Ethernet client will work with the following boards:
//   - Ethernet FeatherWing -> https://www.adafruit.com/products/3201

// uncomment the following two lines for ethernet,
// and comment out the AdafruitIO_WiFi client in the WIFI section
// #include "AdafruitIO_Ethernet.h"
// AdafruitIO_Ethernet io(IO_USERNAME, IO_KEY);
```
