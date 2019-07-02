# main.py

from time import sleep
from machine import (DEEPSLEEP_RESET,
                     RTC,
                     deepsleep,
                     reset_cause
                     )

from include.secrets import _ssid, _pass
from src.ota_updater import OTAUpdater
from src.garuda import Garuda


### TODO: read these from a config file
# 1000 = 1 sec
# 10000 = 10 secs...
DEEPSLEEP_MIN = 1000 * 60

DEEPSLEEP_TIME = DEEPSLEEP_MIN * 30
SLEEPTIME = 60 * 60  # in seconds
GITHUB_REPO = 'https://github.com/desmith/Sudhama_esp32_mpy'

rtc = RTC()
ota = OTAUpdater(GITHUB_REPO)

VERSION = ota.get_version(directory='src', version_file_name='.version')

f = open('board.py')
BOARD = f.readline().rstrip('\n')
f.close()


def download_and_install_update_if_available():
    print('checking for updates...')
    ota.download_and_install_update_if_available(_ssid, _pass)


def start():
    print('Hare Krishna')

    carrier = Garuda(board=BOARD, version=VERSION)
    carrier.arise()

    print('going to sleep for a while (but not deep sleep)...')
    sleep(SLEEPTIME)


def boot():
    # check if the device woke from a deep sleep
    # (A software reset does not change the reset cause)
    if reset_cause() == DEEPSLEEP_RESET:
        print('woke from a deep sleep')

    download_and_install_update_if_available()

    while True:
        start()
        deepsleep(DEEPSLEEP_TIME)
        '''
        Calling deepsleep() without an argument will put the device to sleep indefinitely
        '''


boot()
