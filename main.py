#! /usr/bin/env python3

import asyncio
from json import JSONDecoder
from typing import Dict, Optional
import os

from crosslab.api_client.improved_client import APIClient
from crosslab.soa_client.device_handler import DeviceHandler
from crosslab.soa_services.electrical import ElectricalConnectionService
from crosslab.soa_services.electrical.signal_interfaces.gpio import (
    GPIOInterface,
    ConstractableGPIOInterface,
    GPIOSignalChangeEventData
)

gpio_names= [
    *["gpio0",    "gpio1",    "gpio2", "gpio3",    "gpio4",    "gpio5",    "gpio6",    "gpio7"],
    *["gpio8",    "gpio9",    "gpio10",    "gpio11",    "gpio12", "gpio13",   "gpio14",    "gpio15"],
    *["gpio16",    "gpio17",    "gpio18",    "gpio19",    "gpio20",    "gpio21",    "gpio22", "gpio23",],
    *["gpio24",    "gpio25",    "gpio26",    "gpio27",    "gpio28",    "gpio29",    "gpio30",    "gpio31"]
]

dev_name=''
chip_name=''
def create_gpio_sim():
    global dev_name, chip_name
    os.mkdir('/sys/kernel/config/gpio-sim/crosslab')
    os.mkdir('/sys/kernel/config/gpio-sim/crosslab/gpio-bank0')
    with open('/sys/kernel/config/gpio-sim/crosslab/gpio-bank0/num_lines', 'w') as f:
        f.write(str(len(gpio_names)))
    with(open('/sys/kernel/config/gpio-sim/crosslab/live', 'w')) as f:
        f.write('1')
    with(open('/sys/kernel/config/gpio-sim/crosslab/dev_name', 'r')) as f:
        dev_name = f.read().strip()
    with(open('/sys/kernel/config/gpio-sim/crosslab/gpio-bank0/chip_name', 'r')) as f:
        chip_name = f.read().strip()

def remove_gpio_sim():
    try:
        with(open('/sys/kernel/config/gpio-sim/crosslab/live', 'w')) as f:
            f.write('0')
    except:
        pass
    try:
        os.rmdir('/sys/kernel/config/gpio-sim/crosslab/gpio-bank0')
    except:
        pass
    os.rmdir('/sys/kernel/config/gpio-sim/crosslab')

def setGpioValue(gpio: int, value: bool):
    with open(f"/sys/devices/platform/{dev_name}/{chip_name}/sim_gpio{str(gpio)}/pull", "w") as f:
        f.write("pull-up" if value else "pull-down")

def getGpioValue(gpio: int) -> bool:
    with open(f"/sys/devices/platform/{dev_name}/{chip_name}/sim_gpio{str(gpio)}/value", "r") as f:
        return f.read().strip() == "1"


interfaces: Dict[int, GPIOInterface] = dict()
def newInterface(interface):
    global hal
    if isinstance(interface, GPIOInterface):
        name: str = interface.configuration["signals"]["gpio"]
        gpioIndex = gpio_names.index(name)
        interfaces[gpioIndex] = interface

        # Input Direction
        if(interface.configuration["direction"] == "in" or interface.configuration["direction"] == "inout"):
            def onChange(event: GPIOSignalChangeEventData):
                setGpioValue(gpioIndex, event.state == "strongH" or event.state == "weakH")
            interface.on("signalChange", onChange )
            setGpioValue(gpioIndex, interface.signalState == "strongH" or interface.signalState  == "weakH")

        # Output Direction
        if(interface.configuration["direction"] == "out" or interface.configuration["direction"] == "inout"):
            interface.changeDriver("weakH" if getGpioValue(gpioIndex) else "strongL")

async def poll_gpio():
    while True:
        for i in interfaces:
            if(interfaces[i].configuration["direction"] == "out" or interfaces[i].configuration["direction"] == "inout"):
                interfaces[i].changeDriver("strongH" if getGpioValue(i) else "strongL")
        await asyncio.sleep(0.1)

async def main_async():
    auth_token: Optional[str] = None
    device_id: Optional[str] = None
    url: Optional[str] = None

    try:
        with open("config.json") as f:
            data = JSONDecoder().decode(f.read())
        auth_token = data["authToken"]
        device_id = data["deviceId"]
        url = data["url"]
    except FileNotFoundError:
        print(f"Warning: No config file at 'config.json' found.")

    if auth_token is None:
        print("Error: No auth token provided.")
        exit(1)
    if device_id is None:
        print("Error: No device id provided.")
        exit(1)
    if url is None:
        print("Error: No url provided.")
        exit(1)

    remove_gpio_sim()
    create_gpio_sim()

    deviceHandler = DeviceHandler()

    sensor_service = ElectricalConnectionService("gpio")
    sensor_interface = ConstractableGPIOInterface(gpio_names, "inout")
    sensor_service.addInterface(sensor_interface)
    sensor_service.on("newInterface", newInterface)
    deviceHandler.add_service(sensor_service)

    async with APIClient(url) as client:
        client.set_auth_token(auth_token)

        deviceHandlerTask = asyncio.create_task(
            deviceHandler.connect(device_id, client)
        )
        gpioPollingTask = asyncio.create_task(
            poll_gpio()
        )

        await deviceHandlerTask
        await gpioPollingTask
    remove_gpio_sim()

def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
