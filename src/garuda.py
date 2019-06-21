from src.thingspeak import main as ts
#from src.asksensors import main as ask
#from src.moisture import readSoilMoisture
#from src.humidtemp import main as ht

# led = Pin(2, Pin.OUT)


class Garuda:
    def __init__(self, *args, **kwargs):
        super(Garuda, self).__init__(*args, **kwargs)

    def measure(self):
        #wetness = readSoilMoisture()
        #print("wetness: ", wetness)
        #ht()
        m = 88
        t = 108.96
        h = 86.54
        r = 964

        return (m, t, h, r,)


    def send(self, m, t, h, r):
        print('Garuda in flight!')
        ts(m, t, h, r)
        #ask(m, t, h)
