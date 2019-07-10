from machine import ADC, Pin, Signal
import dht


#adc.width(ADC.WIDTH_9BIT)   # set 9 bit return values (returned range 0-511)

dht22 = dht.DHT22(Pin(21))

led = Pin(2, Pin.OUT)
vPin = ADC(Pin(34))
vPin.atten(ADC.ATTN_11DB)
# 11DB attenuation allows for a maximum input voltage
#  of approximately 3.6v (default is 0-1.0v)

valve_pin = Pin(22, Pin.OUT)
valve = Signal(valve_pin, invert=False)
