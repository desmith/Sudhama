from machine import Pin, Signal

valve_pin = Pin(22, Pin.OUT)
valve = Signal(valve_pin, invert=False)


def open():
    valve.on()


def close():
    valve.off()
