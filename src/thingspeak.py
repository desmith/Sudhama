import machine
from time import sleep

from lib.thingspeak import ThingSpeakAPI, ProtoHTTPS
from src.thingspeak_channels import (
                                     channels,
                                     active_channel,
                                     field_moisture,
                                     field_temperature,
                                     field_humidity,
                                     field_moisture_raw
                                     )


ts = ThingSpeakAPI(channels, protocol_class=ProtoHTTPS, log=True)

THINGSPEAK_HOST = 'api.thingspeak.com'
THINGSPEAK_PORT = 443
THINGSPEAK_DELAY = 15


def main(moisture=None, temperature=None, humidity=None, rawdata=None):

    ts.send(active_channel, {
        field_moisture: moisture,
        field_temperature: temperature,
        field_humidity: humidity,
        field_moisture_raw: rawdata
    })

    sleep(THINGSPEAK_DELAY)
