from ota_updater import OTAUpdater
#from include.secrets import _ssid, _pass
#from .main.thingspeak import main as ts
#from .main.moisture import readSoilMoisture
#from .main.humidtemp import main as ht



# led = Pin(2, Pin.OUT)

def download_and_install_update_if_available():
     o = OTAUpdater('https://github.com/desmith/sudhama')
     o.download_and_install_update_if_available(_ssid, _pass)


def start():

    import main.thingspeak
    import main.moisture
    import main.humidtemp
    wetness = moisture.readSoilMoisture()
    print("wetness: ", wetness)
    humidtemp.main()
    thingspeak.main()


def boot():
     download_and_install_update_if_available()
     start()


boot()
