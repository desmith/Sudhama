import utime
import ntptime
from machine import (DEEPSLEEP_RESET,
                     RTC,
                     deepsleep,
                     reset_cause
                     )

from time import sleep
from include.secrets import _ssid, _pass
from src.ota_updater import OTAUpdater
from src.garuda import Garuda

ntptime.settime()
DEVMODE = True

GITHUB_REPO = 'https://github.com/desmith/sudhama'
# Possible TODO: read this from a config file
MEASUREMENT_INTERVAL = 60 * 10 # in seconds

rtc = RTC()
ota = OTAUpdater(GITHUB_REPO)
VERSION = ota.get_version(directory='src', version_file_name='.version')

# 1000 = 1 sec
# 10000 = 10 secs...
deepsleep_min = 1000 * 60
deepsleep_hr = deepsleep_min * 60
deepsleep_time = deepsleep_min * 10


def download_and_install_update_if_available():
    print('checking for updates...')
    ota.download_and_install_update_if_available(_ssid, _pass)

def start():
    print('Hare Krishna')

    carrier = Garuda()
    (moisture, temperature, humidity, rawdata) = carrier.measure()
    (y, m, d, h, m, s, dow, doy) = utime.localtime()
    date_time_stamp = ''.join(['GMT: ',
                              str(y),'-', str(m), '-', str(d),
                              ' ',
                              str(h), ':', str(m), ':', str(s)
                              ])
    print("date_time_stamp: ", date_time_stamp)

    status_msg = ''.join([date_time_stamp,
                         ' Current Version: ',
                         VERSION,

                         ])
    carrier.send(moisture, temperature, humidity, rawdata, status_msg)

    if not DEVMODE:
        print('going to sleep for a while...')
        deepsleep(deepsleep_time)

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
