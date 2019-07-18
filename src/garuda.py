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
DEEPSLEEP_TIME = DEEPSLEEP_MIN * 10

SLEEPTIME_FLOWING = 60 * 80  # in seconds
SLEEPTIME_STOPPED = 60 * 20  # in seconds

WATCHDOG_TIMEOUT = 1000 * 60  # 60 seconds

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

        y, mo, d, h, min, s, dow, doy = utime.localtime()
        et = utime.mktime((y, mo, d, h + 4, min, s, dow, doy))
        y, mo, d, h, min, s, dow, doy = utime.localtime(et)
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
        voltages = []
        vwcs = []
        while cnt < 6:
            cnt += 1
            sensor_value, sensor_voltage, soil_vwc = readSoilMoisture()
            values.append(sensor_value)
            voltages.append(sensor_voltage)
            vwcs.append(soil_vwc)
            sleep(2)

        average_value = sum(values) / float(len(values))
        moisture = round(average_value, 2)

        average_voltage = sum(voltages) / float(len(voltages))
        voltage = round(average_voltage, 2)

        average_vwc = sum(vwcs) / float(len(vwcs))
        soil_vwc = round(average_vwc, 2)

        moisture_percentage = soil_vwc * 2

        print('\nmoisture: ', moisture)
        print('moisture_percentage: ', moisture_percentage, '\n')

        self.moisture = moisture_percentage
        self.sensor_data = {
            'value': moisture,
            'percentage': moisture_percentage,
            'voltage': voltage,
            'vwc': soil_vwc
        }

        print('Garuda is fetching temperature and humidity data...')
        self.temperature, self.humidity = ht()
        # temperature, humidity = 108.6, 45.56  # for debugging

        return

    def send(self):
        print('Garuda in flight!')
        status_msg = ' | '.join([self.timestamp,
                              'Board: ' + self.BOARD,
                              'Version: ' + self.VERSION,
                              'water: ' + water.status(),
                              'sensor_data: ' + str(self.sensor_data),
                              'ipaddress: ' + self.ipaddress
                              ])

        print('sending data to Thingspeak: ', status_msg)
        ts(self.moisture, self.temperature, self.humidity, status_msg)

        return

    def arise(self):
        print('Garuda Rising!')
        self.measure()

        if self.moisture < 40:
            print('opening valve...')
            water.open()
            SLEEPTIME = SLEEPTIME_FLOWING
        else:
            print('closing valve...')
            water.close()
            SLEEPTIME = SLEEPTIME_STOPPED

        self.send()

        print('going to sleep...')
        sleep(SLEEPTIME)

        print('going to DEEP sleep')
        deepsleep(DEEPSLEEP_TIME)
        '''
        Calling deepsleep() without an argument will put the device to sleep indefinitely
        '''
