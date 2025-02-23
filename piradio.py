# SPDX-FileCopyrightText: 2021 John Furcean
# SPDX-License-Identifier: MIT

"""I2C rotary encoder simple test example."""

import board
import displayio
import adafruit_displayio_ssd1306
import busio
import terminalio
from adafruit_display_text import label

import os
import subprocess

from adafruit_seesaw import seesaw, rotaryio, digitalio

stations_list = [
    ['http://icecast.radiofrance.fr/franceinter-midfi.mp3', 'France Inter'],
    ['http://icecast.radiofrance.fr/franceinfo-midfi.mp3', 'France Info'],
    ['http://stream.live.vc.bbcmedia.co.uk/bbc_world_service', 'BBC World Service'],
    ['https://am820.wnyc.org/wnycam', 'WNYC AM'],
    ['http://direct.franceculture.fr/live/franceculture-midfi.mp3', 'France Culture'],
    ['http://stream-relay-geo.ntslive.net/stream', 'NTS 1'],
    ['http://stream-relay-geo.ntslive.net/stream2', 'NTS 2'],
    ['https://novazz.ice.infomaniak.ch/novazz-128.mp3', 'Nova'],
    ['http://nova-ln.ice.infomaniak.ch/nova-ln-128.mp3', 'Nova la nuit'],
    ['http://nova-vnt.ice.infomaniak.ch:80/nova-vnt-128', 'Nova Vintage'],
    ['http://icecast.radiofrance.fr/fip-midfi.mp3', 'FIP'],
    ['https://stream.radiohelsinki.fi/stream', 'Radio Helsinki'],
    ['http://icecast.radiofrance.fr/francemusique-midfi.mp3', 'France Musique'],
    ['http://stream.klassikradio.de/live/mp3-192/www.klassikradio.de/','Klassik Radio'],
    ['http://stream.klassikradio.de/piano/mp3-192/www.klassikradio.de/', 'Klassik Radio Piano'], 
    ['https://icecast.radiofrance.fr/francemusiquebaroque-midfi.mp3','F. Musique Baroque'],
    ['http://east-mp3-128.streamthejazzgroove.com/', 'Jazz Groove'],
    ['http://tsfjazz.ice.infomaniak.ch/tsfjazz-high.mp3', 'TSF Jazz'],
    ['http://direct.fipradio.fr/live/fip-webradio2.mp3', 'FIP Jazz'],
]

stations = dict(enumerate(stations_list))

#-------- Rotary encoder -------

i2c = board.I2C()  # uses board.SCL and board.SDA
seesaw = seesaw.Seesaw(i2c, addr=0x36)

seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
print("Found product {}".format(seesaw_product))
if seesaw_product != 4991:
    print("Wrong firmware loaded?  Expected 4991")

# Configure seesaw pin used to read knob button presses
# The internal pull up is enabled to prevent floating input
seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
button = digitalio.DigitalIO(seesaw, 24)

button_held = False

encoder = rotaryio.IncrementalEncoder(seesaw)
last_position = None

#-------- OLED display --------
displayio.release_displays()

spi = busio.SPI(board.D21, board.D20)
tft_cs = board.D5
tft_dc = board.D6
tft_reset = board.D13

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_reset, baudrate=1000000)

WIDTH = 128
HEIGHT = 32  # Change to 64 if needed
BORDER = 5

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)
#splash = displayio.Group()
#display.root_group = splash

while True:
    # negate the position to make clockwise rotation positive
    position = -encoder.position

    if position != last_position:
        last_position = position
        print("Position: {}".format(position))
        subprocess.call(['killall', 'mpg123'])
        print("stopped previous track")

        splash = displayio.Group()
        display.root_group = splash

        if stations.get(position):
            station_url = stations.get(position)[0]
            station_name = stations.get(position)[1]
            os.system('mpg123 -f 7000 %s &'%station_url)
            print('playing %s'%station_name)

            text_area = label.Label(terminalio.FONT, text=station_name, color=0xFFFFFF, x=1, y=10)
            splash.append(text_area)
        else:
            print("playing silence")
            text_area = label.Label(terminalio.FONT, text='silence', color=0xFFFFFF, x=1, y=10)
            splash.append(text_area)

    if not button.value and not button_held:
        button_held = True
        print("Button pressed")

    if button.value and button_held:
        button_held = False
        print("Button released")
