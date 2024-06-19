#!/bin/bash

# Initialises GPIO pins that are necessary for executing example experiment
#
# Running once should be fine

for i in 531; do 
	echo $i > /sys/class/gpio/export
done

for i in $(seq 578 591); do 
	echo $i > /sys/class/gpio/export
done
