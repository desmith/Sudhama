import network
import utime
import ntptime

from machine import deepsleep
from time import sleep

from src.lib.umqtt import robust as umqtt
from src.lib.itertools import cycle

from src.thingspeak import main as ts
from src.moisture import readSoilMoisture
from src import water
from src.humidtemp import main as ht

from src.include.secrets import (AIO_CLIENT_ID,
                                 AIO_SERVER,
                                 AIO_PORT,
                                 AIO_USER,
                                 AIO_KEY,
                                 AIO_FEEDS
                                 )


ntptime.settime()

### TODO: read these from a config file
# 1000 = 1 sec
# 10000 = 10 secs...
DEEPSLEEP_MIN = 1000 * 60
DEEPSLEEP_TIME = DEEPSLEEP_MIN * 10

SLEEPTIME_FLOWING = 60 * 80  # in seconds
SLEEPTIME_STOPPED = 60 * 20  # in seconds

WATCHDOG_TIMEOUT = 1000 * 60 * 3 # 3 minutes

AIO_FEEDS_KEYS = list(AIO_FEEDS.keys())

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
        hr = h - 4  # convert to Eastern Time
        et = utime.mktime((y, mo, d, hr, min, s, dow, doy))
        y, mo, d, h, min, s, dow, doy = utime.localtime(et)
        self.timestamp = ''.join([str(y), '-', str(mo), '-', str(d),
                                  ' ',
                                  str(h), ':', str(min), ':', str(s),
                                  ' (GMT -4)'
                                  ])

        print('timestamp: ', self.timestamp)

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
        #  self.temperature, self.humidity = 108.6, 45.56  # for debugging

        return

    def sendTS(self):
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

    def sendAIO(self):
        print('Sending data to Adafruit IO...')

        # Use the MQTT protocol to connect to Adafruit IO
        client = umqtt.MQTTClient(AIO_CLIENT_ID,
                                  AIO_SERVER,
                                  AIO_PORT,
                                  AIO_USER,
                                  AIO_KEY
                                  )

        client.connect()        # Connects to Adafruit IO using MQTT
        client.check_msg()      # Action a message if one is received. Non-blocking.

        moist_sent = False
        temp_sent = False
        humi_sent = False

        toggle = cycle(AIO_FEEDS_KEYS).__next__

        while True:
            feed = toggle()

            try:

                if feed == 'moisture':
                    client.publish(topic=AIO_FEEDS['moisture'], msg=str(self.moisture))
                    print("Moisture sent")
                    moist_sent = True

                elif feed == 'temperature':
                    client.publish(topic=AIO_FEEDS['temperature'], msg=str(self.temperature))
                    print("Temperature sent")
                    temp_sent = True

                elif feed == 'humidity':
                    client.publish(topic=AIO_FEEDS['humidity'], msg=str(self.humidity))
                    print("Humidity sent")
                    humi_sent = True

            except Exception as e:
                print("Sending data to Adafruit FAILED!")
                print(e)

            sleep(3)
            if moist_sent and temp_sent and humi_sent:
                break

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

        self.sendAIO()
        self.sendTS()

        print('going to sleep...')
        sleep(SLEEPTIME)

        print('going to DEEP sleep')
        deepsleep(DEEPSLEEP_TIME)
        '''
        Calling deepsleep() without an argument will put the device to sleep indefinitely
        '''
