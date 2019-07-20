#!/usr/bin/env zsh

items=(
   boot.py
   main.py
   board.py
   include
   src
)

# latest binaries: https://micropython.org/download
port=/dev/cu.SLAB_USBtoUART
mpy_binary=./bin/esp32-20190717-v1.11-163.bin
chipset=esp32

if [ "$1" = "erase" ]; then
    echo "erasing device..."
    esptool.py --chip $chipset --port $port erase_flash

elif [ "$1" = "flash" ]; then
    echo "flashing device with micropython..."
    esptool.py --chip $chipset --port $port --baud 460800 write_flash -z 0x1000 $mpy_binary

elif [ "$1" = "board" ]; then
    echo "copying board.py to device..."
    ampy --port $port put board.py

elif [ "$1" = "boot" ]; then
    echo "copying boot.py to device..."
    ampy --port $port put boot.py

elif [ "$1" = "main" ]; then
    echo "copying main.py to device..."
    ampy --port $port put main.py

elif [ "$1" = "include" ]; then
    echo "copying include directory to device..."
    ampy --port $port put include

elif [ "$1" = "src" ]; then
    echo "copying src directory to device..."
    ampy --port $port put src

else
    for i ($items)
    do
        echo "copying $i to device..."
        ampy --port $port put $i
    done

fi
