### Esp32 með tengingu við AdafruitIO og fimm feed
Þessi feed er led, takki, rakamælir, hitamælir og ljósmælir. Feedin heita hér 'led-one' 'button', 'humid', 'temp' og light.
Adafruit sendir skilaboð að kveykja á led í stjórnborði, öll feedin eru í stjórnborði með viðeigangi viðmóti (Block)
### kóði
``` c
#include "config.h"
#include "DHT.h"
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_TSL2591.h"
#define DHTPIN 4  // Pin connected to the DHT sensor
#define DHTTYPE DHT22  // DHT11 or DHT22
DHT dht(DHTPIN, DHTTYPE);

// Button Pin
#define BUTTON_PIN 0

// LED Pin
#define LED_PIN 2

Adafruit_TSL2591 tsl = Adafruit_TSL2591(2591); 
bool btn_state = false;
bool prv_btn_state = false;
int counter = 0;

AdafruitIO_Feed *light = io.feed("lightsensor");
AdafruitIO_Feed *led = io.feed("led-one");
AdafruitIO_Feed *button = io.feed("button");
AdafruitIO_Feed *humid = io.feed("humid");
AdafruitIO_Feed *temp = io.feed("temp");

void configureSensor(void)
{
  tsl.setGain(TSL2591_GAIN_MED);      // 25x gain
  tsl.setTiming(TSL2591_INTEGRATIONTIME_300MS);
  Serial.println(F("------------------------------------"));
  Serial.print  (F("Gain:         "));
  tsl2591Gain_t gain = tsl.getGain();
}

void setup() {
  // set button pin as an input
  pinMode(BUTTON_PIN, INPUT);

  // set LED pin as an output
  pinMode(LED_PIN, OUTPUT);

  // start the serial connection
  Serial.begin(115200);

  // wait for serial monitor to open
  while(! Serial);

  Serial.print("Connecting to Adafruit IO");

  // connect to io.adafruit.com
  io.connect();
  led->onMessage(handleMessage);

  // wait for a connection
  while(io.status() < AIO_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  // we are connected
  Serial.println();
  Serial.println(io.statusText());
  led->get();
  dht.begin();
}

void loop() {

  io.run();
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  uint16_t x = tsl.getLuminosity(TSL2591_VISIBLE);
  // grab the btn_state state of the button.
  if(digitalRead(BUTTON_PIN) == LOW)
    btn_state = false;
  else
    btn_state = true;
  
  if(counter == 100){
    button->save(btn_state);
    humid->save(h);
    Serial.println(h);
    delay(500);
    temp->save(t);
    Serial.println(t);
    delay(500);
    light->save(x);
    Serial.println(x);
    delay(500);
    counter = 0;
  }

  // store last button state
  prv_btn_state = btn_state;
  counter++;
  Serial.println(counter);

}

void handleMessage(AdafruitIO_Data *data) {
  Serial.print("received <- ");

  if(data->toPinLevel() == HIGH)
    Serial.println("HIGH");
  else
    Serial.println("LOW");

  digitalWrite(LED_PIN, data->toPinLevel());
}
```
### Kóði h.skrá
``` c
#define IO_USERNAME ""
#define IO_KEY ""
#define WIFI_SSID "Taekniskolinn"
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
