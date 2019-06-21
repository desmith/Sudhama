#!/usr/bin/env zsh

items=(
   boot.py
   main.py
   board.py
   src
   include
   lib
)
port=/dev/cu.SLAB_USBtoUART
micropython_binary=./bin/esp32-20190618-v1.11-47-g1a51fc9dd.bin
chipset=esp32


if [ "$1" = "erase" ]; then
    echo "erasing device..."
    esptool.py --chip $chipset --port $port erase_flash

elif [ "$1" = "flash" ]; then
    echo "flashing device with micropython..."
    esptool.py --chip $chipset --port $port --baud 460800 write_flash -z 0x1000 $micropython_binary

elif [ "$1" = "boot" ]; then
    echo "copying boot.py to device..."
    ampy --port $port put boot.py

elif [ "$1" = "main" ]; then
    echo "copying main.py to device..."
    ampy --port $port put main.py

elif [ "$1" = "src" ]; then
    echo "copying src directory to device..."
    ampy --port $port put src

elif [ "$1" = "include" ]; then
    echo "copying include directory to device..."
    ampy --port $port put include

elif [ "$1" = "lib" ]; then
    echo "copying lib directory to device..."
    ampy --port $port put lib

else
    for i ($items)
    do
        echo "copying $i to device..."
        ampy --port $port put $i
    done

fi
