from lib.thingspeak import Channel
from include.secrets import THINGSPEAK_WRITE_KEYS, THINGSPEAK_CHANNEL_IDS


channel_esp8266 = 'Sudhama'
channel_esp32_D = 'Sridama'
channel_esp32_P = 'Gauranga'
active_channel = channel_esp32_D

field_moisture = 'Moisture'
field_temperature = 'Temperature'
field_humidity = 'Humidity'
field_moisture_raw = 'Raw Data [Moisture]'

channels = [
    Channel(channel_esp8266, THINGSPEAK_WRITE_KEYS[channel_esp8266],
            [
            field_temperature,
            field_humidity
            ]
            ),
    Channel(channel_esp32_D, THINGSPEAK_WRITE_KEYS[channel_esp32_D],
            [
            field_moisture,
            field_temperature,
            field_humidity,
            field_moisture_raw
            ]
            ),
    Channel(channel_esp32_P, THINGSPEAK_WRITE_KEYS[channel_esp32_P],
            [
            field_moisture,
            field_temperature,
            field_humidity,
            field_moisture_raw
            ]
            )

]
