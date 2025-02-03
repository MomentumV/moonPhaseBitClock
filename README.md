# moonPhaseBitClock
A binary clock that also shows the current moon phase. Uses a 8x8 neopixel (ws2812) RGB grid, and a Raspberry Pi Pico W. Sets the time from ntp and supports OTA updates

OTA update code from https://github.com/kevinmcaleer/ota

Moon phase emphemeris adapted from https://github.com/pedrokkrause/fourier_ephem
The data arrays for the longitude were converted to simple lists in a dictionary, and the computation of the dot product was done in pure python to avoid the need for numpy (which is not readily available in micropython).

Set your wifi credentials in WIFI_CONFIG.py

# How the moon phase is displayed:
There's approximately 1 LED change per every 12 hours for the Moon phase.

|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   | ⬤ |   |   |   |   |   |   | ⬤ | ⬤ | ⬤ | ⬤ |   |   |   |   | ⬤ | ⬤ | ⬤ | ⬤ |
|   |   |   |   |   |   | ⌾ | ⌾ |   |   |   |   |   |   | ⌾ | ⌾ | ⬤ |   |   |   |   |   |   | ⌾ | ⌾ | ⬤ |
|   |   | ⌾ | ⌾ |   | ⌾ | ⌾ | ⌾ |   |   |   |   | ⌾ | ⌾ | ⌾ | ⬤ |   |   |   |   |   | ⌾ | ⌾ | ⌾ | ⬤ |
|   |   | ⌾ | ⌾ |   | ⌾ | ⌾ | ⌾ | ⌾ | 🡂 |   | ⌾ | ⌾ | ⌾ | ⌾ | ⌾ | ⬤ | 🡂 |   | ⌾ | ⌾ | ⌾ | ⌾ | ⬤ |
|   |   | M | D |   | h | m | s |   |   | M | D |   | h | m | s | ⬤ |   | M | D |   | h | m | s | ⬤ |
|   |   | ⌾ | ⌾ |   | ⌾ | ⌾ | ⌾ |   |   |   | ⌾ | ⌾ | ⌾ | ⌾ | ⬤ |   |   |   | ⌾ | ⌾ | ⌾ | ⬤ |
|   |   | ⌾ | ⌾ |   | ⌾ | ⌾ | ⌾ |   |   |   | ⌾ | ⌾ | ⌾ | ⌾ | ⬤ |   |   | ⌾ | ⌾ | ⌾ | ⬤ |
|   |   |   |   |   |   |   |   |   |   |   |   |   |   | ⬤ |   | ⬤ | ⬤ | ⬤ |   |   |   |   | ⬤ |
| New Moon; Every 28.5 days |   | Waxing Crescent; about 4 days |   | First quarter; about 7 days |
| 🡁 |   | 🡃 |   |   |   |   | ⬤ |   |   |   | ⬤ | ⬤ | ⬤ | ⬤ | ⬤ | ⬤ |   |
|   | ⌾ | ⌾ |   | ⌾ | ⌾ |   | ⌾ | ⌾ |   | ⌾ |   |   | ⌾ |   | ⬤ |   |   |   | ⌾ | ⌾ | ⌾ | ⬤ |
|   | ⌾ | ⌾ |   | ⌾ | ⌾ | ⌾ |   |   |   | ⌾ | ⌾ | ⌾ | ⌾ | ⬤ |   |   | ⌾ | ⌾ | ⌾ | ⬤ |
|   | ⬤ | ⌾ | ⌾ |   | ⌾ | ⌾ | ⌾ |   |   |   | ⌾ | ⌾ | ⌾ | ⌾ | ⬤ |
|   | ⬤ | M | D |   | h | m | s | ⬤ |   |   |   | M | D |   | h | m | s | ⬤ |
|   | ⬤ | ⌾ | ⌾ |   | ⌾ | ⌾ | ⌾ |   | ⌾ |   |   | ⌾ |   | ⬤ |   |   | ⌾ | ⌾ | ⌾ | ⬤ |
|   | ⌾ | ⌾ |   | ⌾ | ⌾ | ⌾ |   |   |   | ⌾ | ⌾ | ⌾ | ⌾ | ⬤ |
|   |   |   |   |   |   |   |   |   |   |   |   |   |   | ⬤ | ⬤ | ⬤ |   |   | ⬤ |
| Waning Cresent; about 27 days |   | Waxing Gibbous; About 8.5 days |
| 🡁 |   | 🡃 |   |   |   |   | ⬤ |   |   | ⬤ | ⬤ | ⬤ | ⬤ | ⬤ | ⬤ | ⬤ |   |
| ⬤ | ⬤ | ⬤ | ⬤ |   |   |   | ⬤ | ⬤ | ⬤ | ⬤ | ⬤ | ⬤ | ⬤ |
| ⬤ |   | ⌾ |   | ⌾ | ⌾ | ⌾ |   | ⬤ |   | ⌾ |   | ⌾ | ⌾ | ⌾ | ⬤ |
| ⬤ |   | ⌾ |   | ⌾ | ⌾ | ⌾ |   | ⬤ |   | ⌾ | ⌾ | ⌾ | ⬤ |
| ⬤ |   | ⌾ |   | ⌾ | ⌾ | ⌾ | ⌾ | 🡀 | ⬤ |   | ⌾ | ⌾ | ⌾ | ⬤ |
| ⬤ | M | D |   | h | m | s | ⬤ |   | ⌾ |   | M | D |   | h | m | s | ⬤ |
| ⬤ | ⌾ | ⌾ |   | ⌾ | ⌾ | ⌾ |   | ⬤ |   | ⌾ | ⌾ | ⌾ | ⬤ |
| ⬤ | ⌾ | ⌾ |   | ⌾ | ⌾ | ⌾ | ⬤ |   | ⌾ |   | ⌾ | ⬤ | ⌾ | ⌾ | ⬤ |
| ⬤ | ⬤ | ⬤ | ⬤ |   |   |   | ⬤ | ⬤ | ⬤ | ⬤ | ⬤ | ⬤ | ⬤ |
| Third Quarter; about 21 days |   | Waning Gibbous; about 16 days | Full; about 14 days |
