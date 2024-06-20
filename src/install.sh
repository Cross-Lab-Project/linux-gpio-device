#!/bin/bash

if [ $(whoami) != "root" ]; then
	echo "Please run as root!"
fi

if ! grep gpio-sim /etc/modules >/dev/null; then
	modprobe gpio-sim
	echo gpio-sim >> /etc/modules
fi

pip install -r requirements.txt
cp ./crosslab-virtual-gpio /usr/local/sbin
cp ./crosslab-virtual-gpio.service /etc/systemd/system/

systemctl enable crosslab-virtual-gpio.service

