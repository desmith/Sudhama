from machine import ADC, Pin
from time import sleep


led = Pin(2, Pin.OUT)
vPin = ADC(Pin(39))
# 11dB attenuation, gives a maximum input voltage of approximately 3.6v
vPin.atten(ADC.ATTN_11DB)

sensor_range              = 1024
sensor_max_voltage        = 3.3

curve_data = {
    .6: 5,
    1.1: 10,
    1.3: 15,
    1.4: 20,
    1.5: 25,
    1.6: 30,
    1.7: 35,
    1.8: 40,
    2.0: 45,
    2.2: 50
}


def get_vwc(k):
    k = float(k)
    return curve_data[max(key for key in map(float, curve_data.keys()) if key <= k)]


def readSoilMoisture():

    led.value(1)
    print('reading moisture...\n')
    # Serial port returns measurement data

    sensor_value = vPin.read()
    sensor_voltage = sensor_value / 1000

    # Volumetric Water Content is a piecewise function
    # of the voltage from the sensor

    soil_vwc = get_vwc(sensor_voltage)
    moisture_percentage = 100.00 * (sensor_voltage / 3.3)

    sensor_data = {
        'value': sensor_value,
        'voltage': sensor_voltage,
        'vwc': soil_vwc
    }

    print('sensor_value: ', sensor_value)
    print('sensor_voltage: ', sensor_voltage)
    print('soil_vwc: ', soil_vwc)
    print('moisture_percentage: ', moisture_percentage)

    sleep(2)
    led.value(0)
    return (moisture_percentage, sensor_data)
