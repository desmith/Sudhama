import machine
from src.ota_updater import OTAUpdater
from include.secrets import _ssid, _pass
from src.thingspeak import main as ts
#from src.moisture import readSoilMoisture
#from src.humidtemp import main as ht

# led = Pin(2, Pin.OUT)


def download_and_install_update_if_available():
    print('checking for updates...')
    ota = OTAUpdater('https://github.com/desmith/sudhama')
    ota.download_and_install_update_if_available(_ssid, _pass)


def start():
    #wetness = readSoilMoisture()
    #print("wetness: ", wetness)
    #ht()
    ts()
    print('Hare Krishna')

    # put the device to sleep for 10 seconds
    print('going to sleep now...')
    #machine.deepsleep(20000)


def boot():
    # check if the device woke from a deep sleep
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        print('woke from a deep sleep')

    download_and_install_update_if_available()
    start()


boot()
