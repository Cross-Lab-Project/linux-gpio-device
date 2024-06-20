#!/bin/bash

if [ $(whoami) != "root" ]; then
	echo "Please run as root!"
fi

pip uninstall -r requirements.txt -y

systemctl disable crosslab-virtual-gpio.service

rm -f /usr/local/sbin/crosslab-virtual-gpio
rm -f /etc/systemd/system/crosslab-virtual-gpio.service

