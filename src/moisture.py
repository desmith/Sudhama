from machine import ADC, Pin

led = Pin(2, Pin.OUT)
vPin = ADC(Pin(39))
# 11DB attenuation allows for a maximum input voltage
#  of approximately 3.6v (default is 0-1.0v)
vPin.atten(ADC.ATTN_11DB)

curve_data = {
    0: 0,
    .6: 5,
    1.1: 10,
    1.3: 15,
    1.4: 20,
    1.5: 25,
    1.6: 30,
    1.7: 35,
    1.8: 40,
    2.0: 45,
    2.2: 50,
    3.3: 50
}

# Volumetric Water Content is a piecewise function
# of the voltage from the sensor
# this function returns the closest vwc value (below)
# the current sensor reading


def get_vwc(sensor_voltage):
    sensor_voltage = float(sensor_voltage)
    if not sensor_voltage:
        return 0
    return curve_data[max(key for key in map(float, curve_data.keys()) if key <= sensor_voltage)]


def readSoilMoisture():
    led.value(1)
    print('reading moisture...\n')
    # Serial port returns measurement data

    sensor_value = vPin.read()
    sensor_voltage = sensor_value / 1000  # convert digital value to decimal
    soil_vwc = get_vwc(sensor_voltage)
    #moisture_percentage = 100.00 * (sensor_voltage / 3.3)
    moisture_percentage = soil_vwc * 2

    sensor_data = {
        'value': sensor_value,
        'voltage': sensor_voltage,
        'vwc': soil_vwc
    }

    print('sensor_value: ', sensor_value)
    print('sensor_voltage: ', sensor_voltage)
    print('soil_vwc: ', soil_vwc)
    print('moisture_percentage: ', moisture_percentage)

    led.value(0)
    return (moisture_percentage, sensor_data)
