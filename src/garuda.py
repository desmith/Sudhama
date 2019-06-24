from time import sleep
from src.thingspeak import main as ts
from src.moisture import readSoilMoisture
#from src.humidtemp import main as ht


class Garuda:
    def __init__(self, *args, **kwargs):
        super(Garuda, self).__init__(*args, **kwargs)

    def measure(self):
        print('Garuda is fetching moisture data...')

        while True:
            (sensor_value, wetness) = readSoilMoisture()
            print('wetness: ', wetness, '\n')
            sleep(2)

        print('Garuda is fetching temperature data...')
        temperature = ''.join([str(108.96), ' [dummy data]'])
        print('temperature: ', temperature, '\n')

        print('Garuda is fetching humidity data...')
        humidity = ''.join([str(86.54), ' [dummy_data]'])
        print('humidity: ', humidity, '\n')

        # ht()

        return (wetness, temperature, humidity, sensor_value)

    def send(self, m, t, h, s):
        print('Garuda in flight!')
        ts(m, t, h, s)
