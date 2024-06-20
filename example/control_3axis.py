import gpio as GPIO
import time

START_GOLDI_GPIO = 578

buttons = {
        "ButtonRight":   531,
        "ButtonLeft":    537,
        "ButtonUp":      538,
        "ButtonDown":    536,
        }

sensors = {
        "LimitXLeft":  START_GOLDI_GPIO,
        "LimitXRight": START_GOLDI_GPIO + 1,
        "LimitYBack":  START_GOLDI_GPIO + 2,
        "LimitYFront": START_GOLDI_GPIO + 3,
        "LimitZBottom":START_GOLDI_GPIO + 4,
        "LimitZTop":   START_GOLDI_GPIO + 5,
        "Proximity":   START_GOLDI_GPIO + 6,
        }

actuators = {
        "XmotorLeft":  START_GOLDI_GPIO + 7,
        "XmotorRight": START_GOLDI_GPIO + 8,
        "YmotorBack":  START_GOLDI_GPIO + 9,
        "YmotorFront": START_GOLDI_GPIO + 10,
        "ZmotorBottom":START_GOLDI_GPIO + 11,
        "ZmotorTop":   START_GOLDI_GPIO + 12,
        "Magnet":      START_GOLDI_GPIO + 13,
    }

for s in sensors:
    GPIO.setup(sensors[s], GPIO.IN)

for b in buttons:
    GPIO.setup(buttons[b], GPIO.IN)

for a in actuators:
    GPIO.setup(actuators[a], GPIO.OUT)

while True:
    for b in buttons:
        if GPIO.input(buttons["ButtonRight"]) == GPIO.LOW and \
                GPIO.input(sensors["LimitXRight"]) == GPIO.LOW:
            GPIO.output(actuators["XmotorRight"], GPIO.HIGH)
        else:
            GPIO.output(actuators["XmotorRight"], GPIO.LOW)
        if GPIO.input(buttons["ButtonLeft"]) == GPIO.LOW and \
                GPIO.input(sensors["LimitXLeft"]) == GPIO.LOW:
            GPIO.output(actuators["XmotorLeft"], GPIO.HIGH)
        else:
            GPIO.output(actuators["XmotorLeft"], GPIO.LOW)
