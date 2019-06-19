from machine import Pin
from time import sleep

vPin = Pin(26, Pin.IN)
soilMoistureRaw           = 0  # moisture variable
soilMoistureCalibrated    = 0  # moisture variable
soilMoisture              = 0  # moisture variable
moisture_as_percentage    = 0  # calibrated moisture variable
moisture_as_string        = ""


def readSoilMoisture():
    #Serial port returns measurement data
    soilMoistureRaw = vPin.read()

    # Convert to calibrated display value
    # dryness_as_percentage = 100.00 * (1.00 - ((sensorMoisture - Min Value of Sensor) / (Max value - Min Value of Sensor)));

    soilMoistureCalibrated = vPin.read() * (3.3 / 1024)

    sleep(20)

    # Volumetric Water Content is a piecewise function of the voltage from the sensor

    if soilMoistureCalibrated < 1.1:
        soilMoisture = (10 * soilMoistureCalibrated) - 1

    elif soilMoistureCalibrated < 1.3:
        soilMoisture = (25 * soilMoistureCalibrated) - 17.5

    elif (soilMoistureCalibrated < 1.82):
        soilMoisture = (48.08 * soilMoistureCalibrated) - 47.5

    elif (soilMoistureCalibrated < 2.2):
        soilMoisture = (26.32 * soilMoistureCalibrated) - 7.89

    else:
        soilMoisture = (62.5 * soilMoistureCalibrated) - 87.5

    # Serial.println(Moisture)
    moisture_as_string = soilMoisture

    print("Moisture=", soilMoisture)
    print("MoistureRaw=", soilMoistureRaw)
    print("moisture_as_string", moisture_as_string)

    return soilMoisture
