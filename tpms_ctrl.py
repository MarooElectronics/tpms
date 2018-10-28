# -*- coding: utf-8 -*-

# # # # # # # # # # # # #
# tpms_ctrl.py          #
# MarooElectronics Inc. #
# # # # # # # # # # # # #

# Import Standard Modules
import time, serial, onionGpio

# Import User Modules
import tpms_glcd

# Module Variables
KEY = onionGpio.OnionGpio(16)
RESET = onionGpio.OnionGpio(17)
YLED = onionGpio.OnionGpio(18)
GLED = onionGpio.OnionGpio(19)


# Module Initialization
while True:
    time.sleep(3)

    try:
        mcu = serial.Serial('/dev/ttyS1', 9600, timeout=1)
        print('[Init OK] CTRL Module')
        break

    except Exception as e:
        print("[Don't init] CTRL Module - %s" % e)




# Module Function
def send(value):
    mcu.write(value)
    time.sleep(0.1)
    return mcu.readline()


# Module Run
def run():
    # Gpio Setting
    KEY.setInputDirection()
    RESET.setOutpuDirection()
    YLED.setOutpuDirection()
    GLED.setOutpuDirection()

    # ATmega Reset
    RESET.setValue(0)
    time.sleep(0.1)
    RESET.setValue(1)

    while True:
        YLED.setValue(0)
        time.sleep(0.1)
        YLED.setValue(1)

        try:
            if KEY.getValue():
                tpms_glcd.change_layer(1)

        except Exception as e:
            print(e)



