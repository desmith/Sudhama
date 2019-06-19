from .main.ota_updater import OTAUpdater
from .include.secrets import _ssid, _pass
#import .main.thingspeak
from .main.thingspeak import main as ts
from .main.moisture import readSoilMoisture
#import moisture

from .main.humidtemp import main as ht


# led = Pin(2, Pin.OUT)

def download_and_install_update_if_available():
     o = OTAUpdater('url-to-your-github-project')
     o.download_and_install_update_if_available(_ssid, _pass)


def start():
    wetness = readSoilMoisture()
    ht()
    ts()


def boot():
     download_and_install_update_if_available()
     start()


boot()
