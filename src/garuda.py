from time import sleep
from src.thingspeak import main as ts
from src.moisture import readSoilMoisture
#from src.humidtemp import main as ht


class Garuda:
    def __init__(self, *args, **kwargs):
        super(Garuda, self).__init__(*args, **kwargs)

    def measure(self):
        print('Garuda is fetching moisture data...')

        cnt = 0
        while cnt < 6:
            cnt += 1
            (moisture_percentage, sensor_data) = readSoilMoisture()
            print('moisture_percentage: ', moisture_percentage, '\n')
            sleep(2)

        print('Garuda is fetching temperature data...')
        temperature = ''.join([str(108.96), ' [dummy data]'])
        print('temperature: ', temperature, '\n')

        print('Garuda is fetching humidity data...')
        humidity = ''.join([str(86.54), ' [dummy_data]'])
        print('humidity: ', humidity, '\n')

        # ht()

        return (moisture_percentage, temperature, humidity, sensor_data)

    def send(self, m, t, h, s):
        print('Garuda in flight!')
        ts(m, t, h, s)
