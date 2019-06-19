import random
from secrets import asksensors_api_key


ask_host = "api.asksensors.com"
httpPort = 80

url = "http://api.asksensors.com/write/"
url += asksensors_api_key
url += "?module1="
url += random(10, 100)
url += "&module2="
url += random(10, 100)
