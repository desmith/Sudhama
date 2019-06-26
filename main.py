import utime
import ntptime
from machine import (DEEPSLEEP_RESET,
                     RTC,
                     deepsleep,
                     reset_cause
                     )

from include.secrets import _ssid, _pass
from src.ota_updater import OTAUpdater
from src.garuda import Garuda
from src import water

# led = Pin(2, Pin.OUT)

ntptime.settime()

# 1000 = 1 sec
# 10000 = 10 secs...
DEEPSLEEP_MIN = 1000 * 60

# TODO: read these from a config file
DEEPSLEEP_TIME = DEEPSLEEP_MIN * 3
GITHUB_REPO = 'https://github.com/desmith/Sudhama_esp32_mpy'

rtc = RTC()
ota = OTAUpdater(GITHUB_REPO)


(y, m, d, h, m, s, dow, doy) = utime.localtime()
date_time_stamp = ''.join([str(y), '-', str(m), '-', str(d),
                          ' ',
                          str(h), ':', str(m), ':', str(s),
                          ' (GMT)  '
                          ])

VERSION = ota.get_version(directory='src', version_file_name='.version')
f = open('board.py')
BOARD = f.readline().rstrip('\n')
f.close()


def download_and_install_update_if_available():
    print('checking for updates...')
    ota.download_and_install_update_if_available(_ssid, _pass)


def start():
    print('Hare Krishna')
    print('Board: ', BOARD)
    print('Version: ', VERSION)

    carrier = Garuda()
    (moisture, temperature, humidity, sensor_data) = carrier.measure()
    status_msg = ' '.join([date_time_stamp,
                         'Board: ', BOARD,
                         'Version:', VERSION,
                         'sensor_data:', str(sensor_data.items())
                         ])

    print('moisture average: ', moisture, '\n')

    if moisture <= 40:
        water.open()
    else:
        water.close()

    status_msg = ''.join([status_msg, ' water: ', water.status()])
    carrier.send(moisture, temperature, humidity, status_msg)

    print('going to sleep for a while...')
    deepsleep(DEEPSLEEP_TIME)

    '''
    Calling deepsleep() without an argument will put the device to sleep indefinitely
    '''


def boot():
    # check if the device woke from a deep sleep
    # (A software reset does not change the reset cause)
    if reset_cause() == DEEPSLEEP_RESET:
        print('woke from a deep sleep')

    download_and_install_update_if_available()
    start()


boot()
