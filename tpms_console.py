# -*- coding: utf-8 -*-

# # # # # # # # # # # # #
# tpms_console.py       #
# MarooElectronics Inc. #
# # # # # # # # # # # # #

# Import Standard Modules
import time, serial

# Import User Modules
import tpms_gpio

# Module Variables
str_buf = ''
MUX_A0 = 12
MUX_A1 = 13
MUX_A2 = 14

# Module Initialization
while True:
    time.sleep(3)

    try:
        console = serial.Serial('/dev/ttyS2', 9600, timeout=1)
        print('[Init OK] Console Module')
        break

    except Exception as e:
        print("[Don't init] Console Module - %s" % e)




# Module Function
def send(num, value):
    if num == '1':
        tpms_gpio.GPIO_WRITE(MUX_A0, 0)
        tpms_gpio.GPIO_WRITE(MUX_A1, 0)
        tpms_gpio.GPIO_WRITE(MUX_A2, 0)

    elif num == '2':
        tpms_gpio.GPIO_WRITE(MUX_A0, 1)
        tpms_gpio.GPIO_WRITE(MUX_A1, 0)
        tpms_gpio.GPIO_WRITE(MUX_A2, 0)

    elif num == '3':
        tpms_gpio.GPIO_WRITE(MUX_A0, 0)
        tpms_gpio.GPIO_WRITE(MUX_A1, 1)
        tpms_gpio.GPIO_WRITE(MUX_A2, 0)

    elif num == '4':
        tpms_gpio.GPIO_WRITE(MUX_A0, 1)
        tpms_gpio.GPIO_WRITE(MUX_A1, 1)
        tpms_gpio.GPIO_WRITE(MUX_A2, 0)

    elif num == '5':
        tpms_gpio.GPIO_WRITE(MUX_A0, 0)
        tpms_gpio.GPIO_WRITE(MUX_A1, 0)
        tpms_gpio.GPIO_WRITE(MUX_A2, 1)

    global str_buf

    console.write("{}\r".format(value))
    time.sleep(3)

    str_buf += console.readline()
    ret_buf = str_buf

    str_buf = ''

    print(ret_buf)

    console.write("\r")

    return ret_buf


# Module Run
def run():
    global str_buf

    tpms_gpio.GPIO_DIR(MUX_A0, 'out')
    tpms_gpio.GPIO_DIR(MUX_A1, 'out')
    tpms_gpio.GPIO_DIR(MUX_A2, 'out')
    tpms_gpio.GPIO_WRITE(MUX_A0, 0)
    tpms_gpio.GPIO_WRITE(MUX_A1, 0)
    tpms_gpio.GPIO_WRITE(MUX_A2, 0)
    print("[Initial] Console Module")

    while True:
        time.sleep(0.1)

        try:
            str_buf += console.readline()

        except Exception as e:
            print("[Run Error] Console Module - %s" % e)
