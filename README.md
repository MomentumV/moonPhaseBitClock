# moonPhaseBitClock
A binary clock that also shows the current moon phase. Uses a 8x8 neopixel (ws2812) RGB grid, and a Raspberry Pi Pico W. Sets the time from ntp and supports OTA updates

OTA update code from https://github.com/kevinmcaleer/ota

Moon phase emphemeris adapted from https://github.com/pedrokkrause/fourier_ephem
The data arrays for the longitude were converted to simple lists in a dictionary, and the computation of the dot product was done in pure python to avoid the need for numpy (which is not readily available in micropython).

Set your wifi credentials in WIFI_CONFIG.py

# How the moon phase is displayed:
There's approximately 1 LED change per every 12 hours for the Moon phase.

<table>
  <tr>
    <td style="background-color:#ffffff; color:#000000;"></td>
    <td style="background-color:#b7b7b7; color:#ff9900; text-align:center;">⬤</td>
    <td style="background-color:#b7b7b7; color:#ff9900; text-align:center;">⬤</td>
    <td style="background-color:#b7b7b7; color:#ff9900; text-align:center;">⬤</td>
    <td style="background-color:#b7b7b7; color:#ff9900; text-align:center;"></td>
    <td style="background-color:#b7b7b7; color:#ff9900; text-align:center;"></td>
    <td style="background-color:#b7b7b7; color:#ff9900; text-align:center;">⬤</td>
    <td style="background-color:#b7b7b7; color:#ff9900; text-align:center;">⬤</td>
  </tr>
  <tr>
    <td style="background-color:#ffffff; color:#000000;"></td>
    <td style="background-color:#b7b7b7; color:#4a86e8; text-align:center;">⌾</td>
    <td style="background-color:#b7b7b7; color:#4a86e8; text-align:center;">⌾</td>
    <td style="background-color:#b7b7b7; color:#ff9900; text-align:center;">⬤</td>
    <td style="background-color:#b7b7b7; color:#000000; text-align:center;"></td>
    <td style="background-color:#b7b7b7; color:#00ff00; text-align:center;">⌾</td>
    <td style="background-color:#b7b7b7; color:#ff9900; text-align:center;">⬤</td>
    <td style="background-color:#b7b7b7; color:#000000; text-align:center;"></td>
  </tr>
  <tr>
    <td style="background-color:#ffffff; color:#000000;"></td>
    <td style="background-color:#b7b7b7; color:#00ffff; text-align:center;">⌾</td>
    <td style="background-color:#b7b7b7; color:#00ff00; text-align:center;">⌾</td>
    <td style="background-color:#b7b7b7; color:#ff0000; text-align:center;">⌾</td>
    <td style="background-color:#b7b7b7; color:#ff9900; text-align:center;">⬤</td>
    <td style="background-color:#b7b7b7; color:#000000; text-align:center;">🡂</td>
    <td style="background-color:#b7b7b7; color:#ff0000; text-align:center;">⌾</td>
    <td style="background-color:#b7b7b7; color:#000000; text-align:center;"></td>
  </tr>
  <tr>
    <td style="background-color:#ffffff; color:#000000;"></td>
    <td style="background-color:#b7b7b7; color:#00ff00; text-align:center;">⌾</td>
    <td style="background-color:#b7b7b7; color:#000000; text-align:center;">M</td>
    <td style="background-color:#b7b7b7; color:#000000; text-align:center;">D</td>
    <td style="background-color:#ffffff; color:#000000;"></td>
    <td style="background-color:#b7b7b7; color:#000000; text-align:center;">h</td>
    <td style="background-color:#b7b7b7; color:#000000; text-align:center;">m</td>
    <td style="background-color:#b7b7b7; color:#ff9900; text-align:center;">⬤</td>
  </tr>
  <tr>
    <td style="background-color:#ffffff; color:#000000;"></td>
    <td style="background-color:#b7b7b7; color:#4a86e8; text-align:center;">⌾</td>
    <td style="background-color:#b7b7b7; color:#00ff00; text-align:center;">⌾</td>
    <td style="background-color:#b7b7b7; color:#ff9900; text-align:center;">⬤</td>
    <td style="background-color:#b7b7b7; color:#ffffff; text-align:center;"></td>
    <td style="background-color:#b7b7b7; color:#00ff00; text-align:center;">⌾</td>
    <td style="background-color:#b7b7b7; color:#ff0000; text-align:center;">⌾</td>
    <td style="background-color:#b7b7b7; color:#000000; text-align:center;"></td>
  </tr>
  <tr>
    <td style="background-color:#ffffff; color:#000000;"></td>
    <td style="background-color:#b7b7b7; color:#00ff00; text-align:center;">⌾</td>
    <td style="background-color:#b7b7b7; color:#000000; text-align:center;"></td>
    <td style="background-color:#b7b7b7; color:#4a86e8; text-align:center;">⬤</td>
    <td style="background-color:#b7b7b7; color:#ff0000; text-align:center;"></td>
    <td style="background-color:#b7b7b7; color:#000000; text-align:center;"></td>
    <td style="background-color:#b7b7b7; color:#ff9900; text-align:center;">⬤</td>
    <td style="background-color:#b7b7b7; color:#000000; text-align:center;"></td>
  </tr>
  <tr>
    <td style="background-color:#ffffff; color:#000000;"></td>
    <td style="background-color:#b7b7b7; color:#ff9900; text-align:center;"></td>
    <td style="background-color:#b7b7b7; color:#000000; text-align:center;"></td>
    <td style="background-color:#b7b7b7; color:#ff9900; text-align:center;">⬤</td>
    <td style="background-color:#ffffff; color:#000000;"></td>
    <td style="background-color:#b7b7b7; color:#4a86e8; text-align:center;"></td>
    <td style="background-color:#b7b7b7; color:#4a86e8; text-align:center;">⬤</td>
    <td style="background-color:#b7b7b7; color:#ff9900; text-align:center;">⬤</td>
  </tr>
</table>
