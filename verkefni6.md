### Verkefni 6.2
Raspberripi zero með takka tngdan við pinna #12 (D12) þegar ýtt er á takka breytist staða takka í adafruitio í "ON"

```python
"""
'digital_in.py'
==================================
Example of sending button values
to an Adafruit IO feed.

Author(s): Brent Rubell, Todd Treece
"""
# Import standard python modules
import time

# import Adafruit Blinka
import board
import digitalio

# import Adafruit IO REST client.
from Adafruit_IO import Client, Feed, RequestError

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'YOUR_AIO_KEY'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'YOUR_AIO_USERNAME'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try: # if we have a 'digital' feed
    digital = aio.feeds('digital')
except RequestError: # create a digital feed
    feed = Feed(name="digital")
    digital = aio.create_feed(feed)

# button set up
button = digitalio.DigitalInOut(board.D12)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
button_current = 0


while True:
    if not button.value:
        button_current = 1
    else:
        button_current = 0

    print('Button -> ', button_current)
    aio.send(digital.key, button_current)

    # avoid timeout from adafruit io
    time.sleep(1)

```

### Verkefni 6.4
Kóðinn hér fyrir neðan er fyrir ESP 32 með photosellu tengda í Analog 0
kóðin sendir gildi yfir í Adafruit reikning sem birtir gildin í feed
## h skrá
``` c
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
#define SPIWIFI_SS 10 // Chip select pin
#define NINA_ACK 9    // a.k.a BUSY or READY pin
#define NINA_RESETN 6 // Reset pin
#define NINA_GPIO0 -1 // Not connected
#endif
AdafruitIO_WiFi io(IO_USERNAME, IO_KEY, WIFI_SSID, WIFI_PASS, SPIWIFI_SS,
                   NINA_ACK, NINA_RESETN, NINA_GPIO0, &SPIWIFI);
#else
AdafruitIO_WiFi io(IO_USERNAME, IO_KEY, WIFI_SSID, WIFI_PASS);
#endif

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
#define SPIWIFI_SS 10 // Chip select pin
#define NINA_ACK 9    // a.k.a BUSY or READY pin
#define NINA_RESETN 6 // Reset pin
#define NINA_GPIO0 -1 // Not connected
#endif
AdafruitIO_WiFi io(IO_USERNAME, IO_KEY, WIFI_SSID, WIFI_PASS, SPIWIFI_SS,
                   NINA_ACK, NINA_RESETN, NINA_GPIO0, &SPIWIFI);
#else
AdafruitIO_WiFi io(IO_USERNAME, IO_KEY, WIFI_SSID, WIFI_PASS);
#endif
```
### main skrá

``` c

#include "config.h"

#define PHOTOCELL_PIN A0

// photocell state
int current = 0;
int last = -1;

// set up the 'analog' feed
AdafruitIO_Feed *analog = io.feed("myanalog");

void setup() {

  // start the serial connection
  Serial.begin(115200);

  // wait for serial monitor to open
  while(! Serial);

  // connect to io.adafruit.com
  Serial.print("Connecting to Adafruit IO");
  io.connect();

  // wait for a connection
  while(io.status() < AIO_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  // we are connected
  Serial.println();
  Serial.println(io.statusText());

}

void loop() {

  // io.run(); is required for all sketches.
  // it should always be present at the top of your loop
  // function. it keeps the client connected to
  // io.adafruit.com, and processes any incoming data.
  io.run();

  // grab the current state of the photocell
  current = analogRead(PHOTOCELL_PIN);

  // return if the value hasn't changed
  if(current == last)
    return;

  // save the current state to the analog feed
  Serial.print("sending -> ");
  Serial.println(current);
  analog->save(current);

  // store last photocell state
  last = current;

  // wait three seconds (1000 milliseconds == 1 second)
  //
  // because there are no active subscriptions, we can use delay()
  // instead of tracking millis()
  delay(3000);
}
```
