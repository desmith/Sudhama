#!/usr/bin/env zsh

items=(
       boot.py
       main.py
       src
       include
)


for i ($items)
do
    echo "copying $i to device..."
    ampy --port /dev/cu.SLAB_USBtoUART put $i
done
