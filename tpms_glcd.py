# -*- coding: utf-8 -*-

# # # # # # # # # # # # #
# tpms_glcd.py          #
# MarooElectronics Inc. #
# # # # # # # # # # # # #

# Import Standard Modules
import os, time

# Import User Modules
from lib import LG12864F, logo
import tpms_ctrl, tpms_sbc  #, tpms_distance, tpms_log

# Module Variables
layer = 0


# Module Function
def change_layer(value):
    global layer
    layer = value


# Module Run
def run():
    global layer

    # GLCD Module - Init
    while True:
        time.sleep(3)

        try:
            lcd = LG12864F.lcd(0x20)
            # tpms_log.info('GLCD Module Init')
            break

        except Exception as e:
            pass
            # tpms_log.warning("GLCD Module Init - %s" % e)



    # GLCD Module - Logo
    try:
        # 회사 로고
        lcd.lcd_bitmap(logo.data)
    except Exception as e:
        pass
        # tpms_log.warning("GLCD Module Logo - %s" % e)

    # GLCD Module - Run
    while True:
        time.sleep(3)

        if layer == 0:
            try:
                buf = tpms_ctrl.send('(AL)')

                if buf:
                    list_buf = buf.split('AL,')[1].split(')')[0].split(',')

                    lcd.lcd_string(0, 'T:%2.1fc  H:%2.1f%%' % (
                        float(list_buf[15]), float(list_buf[16])))
                    lcd.lcd_string(1, '1:%4dW  2:%4dW' % (
                        int(float(list_buf[0]) * float(list_buf[1])), int(float(list_buf[3]) * float(list_buf[4]))))
                    lcd.lcd_string(2, '3:%4dW  4:%4dW' % (
                        int(float(list_buf[6]) * float(list_buf[7])), int(float(list_buf[9]) * float(list_buf[10]))))
                    lcd.lcd_string(3, '5:%4dW  S>%s' % (
                        int(float(list_buf[12]) * float(list_buf[13])), time.strftime('%H:%M')))
                    # lcd.lcd_string(3, '5:%4dW  %d %s' % (
                    #     int(float(list_buf[12]) * float(list_buf[13])), tpms_distance.read(), time.strftime('%H:%M')))

                else:
                    # GLCD Module - Logo
                    try:
                        # 회사 로고
                        lcd.lcd_bitmap(logo.data)
                    except Exception as e:
                        pass
                        # tpms_log.warning("GLCD Module Logo - %s" % e)

            except Exception as e:
                pass
                # tpms_log.warning("GLCD Module Run - %s" % e)


        elif layer == 1:
            try:
                lcd.lcd_string(0, 'IP: %s' % (tpms_sbc.interfaces_read('address')))
                lcd.lcd_string(1, 'SW: %s' % (tpms_sbc.interfaces_read('netmask')))
                lcd.lcd_string(2, 'GW: %s' % (tpms_sbc.interfaces_read('gateway')))
                lcd.lcd_string(3, 'SB: %s' % (tpms_sbc.interfaces_read('#SVIP')))

                layer = 0

            except Exception as e:
                pass
                # tpms_log.warning("GLCD Module Run - %s" % e)
