"""The DHT driver is implemented in software and works on all pins:"""
from machine import Pin
import dht


def main():
    print("humidtemp.main()")
    '''
    d = dht.DHT11(Pin(4))
    d.measure()
    d.temperature()  # eg. 23 (°C)
    d.humidity()     # eg. 41 (% RH)
    '''

    d = dht.DHT22(Pin(4))
    d.measure()
    d.temperature()  # eg. 23.6 (°C)
    d.humidity()     # eg. 41.3 (% RH)


print("humidtemp imported")
