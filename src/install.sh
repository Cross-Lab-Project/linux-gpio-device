#!/bin/bash

if [ $(whoami) != "root" ]; then
	echo "Please run as root!"
fi

pip install -r requirements.txt
cp ./crosslab-virtual-gpio /usr/local/sbin
cp ./crosslab-virtual-gpio.service /etc/systemd/system/

systemctl enable crosslab-virtual-gpio.service

