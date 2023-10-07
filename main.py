import network
import socket
import time
import struct
import machine
import array
from machine import Pin
from ota import OTAUpdater
from WIFI_CONFIG import SSID, PASSWORD
#from maps import RINGMAP,MODEMAPS #will uncomment on next release
import rp2

#configure settings:
firmware_url = "https://raw.githubusercontent.com/momentumv/moonPhaseBitClock/main/"
tz_offset_hrs = -4 # deal with daylight savings another time
tz_offset = tz_offset_hrs * 60 * 60
# wifi password configured in WIFI_CONFIG.py

# Configure the number of WS2812 LEDs.
NUM_LEDS = 64
COL = 8 #used for clearer indexing math
PIN_NUM = 22  #gpio used for Neopixel grid
brightness = 0.1 # helps with power consumption as well
# each pixel can pull almost 60 mA at full power.
# marginal usb power supply will cause issues.

#PIO neopixel driver
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()

# Create the StateMachine with the ws2812 program, outputting on pin
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))

# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(NUM_LEDS)])
def pixels_show():
    dimmer_ar = array.array("I", [0 for _ in range(NUM_LEDS)])
    for i,c in enumerate(ar):
        r = int(((c >> 8) & 0xFF) * brightness)
        g = int(((c >> 16) & 0xFF) * brightness)
        b = int((c & 0xFF) * brightness)
        dimmer_ar[i] = (g<<16) + (r<<8) + b
    sm.put(dimmer_ar, 8)
    time.sleep_ms(12)

def pixels_set(i, color):
    ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]
 
#lunar phase constants
BASE = 1610514000  # 2021 Jan 13 5:00 UTC new moon
PERIOD = 2551443  # average lunation length in seconds
RINGMAP = [60,59,61,58,62,57,63,56,55,48,47,40,39,32,31,24,23,16,15,8,7,0,6,1,5,2,4,3]


def moonpixels(t = time.time()): # no tz offset for lunar phase; use UTC
    numerator = (t - BASE) % PERIOD  # seconds into current moon phase
    phase = numerator / PERIOD  # fractional phase 0-1
    nleds= 28 # outer ring of 8x8 matrix
    # since we'll sweep across twice each lunation
    # (once for waxing and once for waning)
    # we need to scale our 0-1 phase up
    whole = (numerator * 2 * nleds) // PERIOD
    #fractional leds will fade in/out
    fraction = ((numerator * 2 * nleds) % PERIOD) / PERIOD
    
    #the active led will always be fractional (fading)
    if whole//nleds:
        waxing = False
        ring = [BLACK if i<whole % nleds else MOON for i in range(nleds)]
        fraction = 1-fraction # waning updates are 'increasing dimming' so we subtract from 1 for brightness
    else:
        waxing = True
        ring = [MOON if i<whole else BLACK for i in range(nleds)]
    value = (int(MOON[0]*fraction),\
             int(MOON[1]*fraction),\
             int(MOON[2]*fraction)  )
    active_led_index = whole % nleds
#     print(active_led_index, whole)
    ring[active_led_index] = value
    return ring

#color definitions
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN  = (0, 255, 0)
CYAN   = (0, 255, 255)
BLUE   = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE  = (255, 255, 255)
MOON   = (127,127,127)
COLORS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)


NTP_DELTA = 2208988800  #  keep utc, adjust before display +4*60*60
host = "pool.ntp.org"
led = machine.Pin("LED", machine.Pin.OUT)

def set_time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    except OSError as exc:
        if exc.args[0] == 110: # ETIMEDOUT
            time.sleep(2)
            pass
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    t = val - NTP_DELTA    
    tm = time.gmtime(t)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

led.on()
set_time()
print(time.localtime())
ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main.py")
ota_updater2 = OTAUpdater(SSID, PASSWORD, firmware_url, "maps.py")
ota_updater.download_and_install_update_if_available()
ota_updater2.download_and_install_update_if_available()
led.off()
while True:
    t=time.localtime(time.time()+tz_offset)
    s=f'{t[5]:06b}'
    m=f'{t[4]:06b}'
    h=f'{t[3]:06b}'
    d=f'{t[2]:06b}'
    M=f'{t[1]:06b}'
    for i in range(6):
        pixels_set(i+1+1*COL,[BLACK,BLUE][int(s[i])])
        pixels_set(i+1+2*COL,[BLACK,GREEN][int(m[i])])
        pixels_set(i+1+3*COL,[BLACK,RED][int(h[i])])
        pixels_set(i+1+5*COL,[BLACK,YELLOW][int(d[i])])
        pixels_set(i+1+6*COL,[BLACK,CYAN][int(M[i])])
    ring_values = moonpixels(time.time()) # no tz offset for moon phase
    for i in range(len(RINGMAP)):
        pixels_set(RINGMAP[i],ring_values[i])
    pixels_show()
    time.sleep_ms(200)