#!/bin/bash


for i in 531 536 537 538; do 
	echo $i > /sys/class/gpio/export
done

for i in $(seq 578 591); do 
	echo $i > /sys/class/gpio/export
done
