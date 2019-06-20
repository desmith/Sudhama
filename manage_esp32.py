#!/usr/bin/env python

import argparse
import subprocess
from subprocess import Popen, PIPE, STDOUT

esp_port = '/dev/cu.SLAB_USBtoUART'
files = ['boot.py', 'main.py',  'src', 'include']
micropython_binary = './bin/esp32-20190618-v1.11-47-g1a51fc9dd.bin'

parser = argparse.ArgumentParser(description="Manage EP32 device - Erase/Write Flash, load code, etc.")
parser.add_argument("--erase", type=bool, default=False, nargs="?", const=True, help="Erase Flash")
parser.add_argument("--flash", type=bool, default=False, nargs="?", const=True, help="Flash device")
parser.add_argument("--load", type=bool, default=False, nargs="?", const=True, help="Copy file to device")
parser.add_argument("--src", type=bool, default=False, nargs="?", const=True, help="Load source code to device")
parser.add_argument("-d", dest="DEBUG", default=False, nargs="?",  const=True, help="debug mode")

args = parser.parse_args()

if args.DEBUG:
  print ("args: %s" % args)


def _load_source(source_code):
    subprocess.run(["ampy", "--port", esp_port, "put", source_code], capture_output=True)

    return result

def main():
    if args.erase:
        print("Erasing Flash from device")
        subprocess.run(["esptool.py", "--chip", "esp32", "--port", esp_port, "erase_flash"], capture_output=True)
        print(subprocess.CompletedProcess.stdout())

    elif args.flash:
        print("Flashing micropython to device")
        #subprocess.run(["esptool.py", "--chip", "esp32", "--port", esp_port, "--baud", "460800", "write_flash", "-z", "0x1000", micropython_binary], capture_output=True)
        s = subprocess.check_output(["esptool.py", "--chip", "esp32", "--port", esp_port, "--baud", "460800", "write_flash", "-z", "0x1000", micropython_binary])
        print (s)


    elif args.src:
        print("Copying src directory to device")
        source_code = 'src'
        _load_source(source_code)

    elif args.load:
        for f in files:
            print('Copying ', f, ' to device')
            _load_source(f)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
    #main(sys.argv[1:])
