# moonPhaseBitClock
A binary clock that also shows the current moon phase. Uses a 8x8 neopixel (ws2812) RGB grid, and a Raspberry Pi Pico W. Sets the time from ntp and supports OTA updates

OTA update code from https://github.com/kevinmcaleer/ota

Set your wifi credentials in WIFI_CONFIG.py

# How the moon phase is displayed:
There's approximately 1 LED change per every 12 hours for the Moon phase.

<iframe src="https://docs.google.com/spreadsheets/d/e/2PACX-1vSBAbLICryW-UTT_7OwHbRlJCfbNjle9r8l-Votz0u1gCDcwYpMo_h5XaTcRV6ItElYIqPimeQAn60w/pubhtml?gid=2054537010&amp;single=true&amp;widget=true&amp;headers=false"></iframe>