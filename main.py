import machine
from time import sleep

from include.secrets import _ssid, _pass
from src.ota_updater import OTAUpdater
from src.garuda import Garuda


DEVMODE = True

GITHUB_REPO = 'https://github.com/desmith/sudhama'
# Possible TODO: read this from a config file
MEASUREMENT_INTERVAL = 60 * 10 # in seconds

# 1000 = 1 sec
# 10000 = 10 secs...
deepsleep_min = 1000 * 60
deepsleep_hr = deepsleep_min * 60
deepsleep_time = deepsleep_min * 10


def download_and_install_update_if_available():
    print('checking for updates...')
    ota = OTAUpdater(GITHUB_REPO)
    ota.download_and_install_update_if_available(_ssid, _pass)

def start():
    print('Hare Krishna')

    carrier = Garuda()
    (moisture, temperature, humidity, rawdata) = carrier.measure()
    carrier.send(moisture, temperature, humidity, rawdata)

    if not DEVMODE:
        print('going to sleep for a while...')
        machine.deepsleep(deepsleep_time)

        '''
        Calling deepsleep() without an argument will put the device to sleep indefinitely
        '''

def boot():
    # check if the device woke from a deep sleep
    # (A software reset does not change the reset cause)
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        print('woke from a deep sleep')

    download_and_install_update_if_available()
    start()


boot()
