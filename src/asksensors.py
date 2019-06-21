from include.secrets import ASKSENSORS_API_KEY

import ussl as ssl

try:
    import usocket as socket
except:
    import socket

ASK_HOST = 'api.asksensors.com'
ASK_PORT = 443


def http_get(url, port):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s = ssl.wrap_socket(s, server_hostname=host)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()


def main(moisture, temperature, humidity):
    print("AskSensors.main()...")

    global ASKSENSORS_API_KEY
    if not ASKSENSORS_API_KEY:
        print('no ThingSpeak key specified, skip sending data')
        return

    print('sending data to AskSensors')

    url = ''.join(['https://', ASK_HOST, '/write/'])
    url += ASKSENSORS_API_KEY
    url += '?module1='
    url += str(moisture)
    url += '&module2='
    url += str(temperature)
    url += '&module3='
    url += str(humidity)

    print('url: ', url)
    http_get(url, ASK_PORT)


print("AskSensors imported...")
