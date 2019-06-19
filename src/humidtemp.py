"""The DHT driver is implemented in software and works on all pins:"""

import machine
import dht


def main():
    print("humidtemp.main()")
    '''
    d = dht.DHT11(machine.Pin(4))
    d.measure()
    d.temperature()  # eg. 23 (°C)
    d.humidity()     # eg. 41 (% RH)
    '''

    d = dht.DHT22(machine.Pin(4))
    d.measure()
    d.temperature()  # eg. 23.6 (°C)
    d.humidity()     # eg. 41.3 (% RH)


'''
Calling deepsleep() without an argument will put the device to sleep indefinitely

A software reset does not change the reset cause
'''

print("humidtemp imported")
