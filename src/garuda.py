import network
import utime
import ntptime
from machine import deepsleep
from time import sleep

from src.thingspeak import main as ts
from src.moisture import readSoilMoisture
from src import water
from src.humidtemp import main as ht


ntptime.settime()


### TODO: read these from a config file
# 1000 = 1 sec
# 10000 = 10 secs...
DEEPSLEEP_MIN = 1000 * 60
DEEPSLEEP_TIME = DEEPSLEEP_MIN * 30

SLEEPTIME = 60 * 60  # in seconds

# deepsleep(DEEPSLEEP_TIME)
'''
Calling deepsleep() without an argument will put the device to sleep indefinitely
'''


class Garuda:
    def __init__(self, board, version):
        self.BOARD = board
        self.VERSION = version

        print('Garuda Awake!')
        print('Board: ', self.BOARD)
        print('Version: ', self.VERSION)

        (y, mo, d, h, min, s, dow, doy) = utime.localtime()
        self.timestamp = ''.join([str(y), '-', str(mo), '-', str(d),
                                  ' ',
                                  str(h), ':', str(min), ':', str(s),
                                  ' (GMT)'
                                  ])

        sta_if = network.WLAN(network.STA_IF)
        self.ipaddress = sta_if.ifconfig()[0]

    def measure(self):
        print('Garuda is fetching moisture data...')

        cnt = 0
        values = []
        while cnt < 6:
            cnt += 1
            (moisture_percentage, sensor_data) = readSoilMoisture()
            values.append(moisture_percentage)
            sleep(2)

        average = sum(values) / float(len(values))
        moisture = round(average, 2)

        print('\nmoisture average: ', moisture, '\n')

        if moisture <= 40:
            print('opening valve...')
            water.open()
        else:
            print('closing valve...')
            water.close()

        print('Garuda is fetching temperature and humidity data...')
        (temperature, humidity) = ht()

        self.moisture = moisture
        self.temperature = temperature
        self.humidity = humidity
        self.sensor_data = sensor_data

    def send(self):
        print('Garuda in flight!')
        status_msg = ' | '.join([self.timestamp,
                              'Board: ' + self.BOARD,
                              'Version: ' + self.VERSION,
                              'water: ' + water.status(),
                              'sensor_data: ' + str(self.sensor_data),
                              'ipaddress: ' + self.ipaddress
                              ])

        #self.status_msg += 'sensor_data: ' + str(sensor_data)

        print('sending data to Thingspeak: ', status_msg)

        ts(self.moisture, self.temperature, self.humidity, status_msg)

    def arise(self):
        print('Garuda Rising!')
        self.measure()
        self.send()
        sleep(SLEEPTIME)
        deepsleep(DEEPSLEEP_TIME)
        '''
        Calling deepsleep() without an argument will put the device to sleep indefinitely
        '''
