# -*- coding: utf-8 -*-

# # # # # # # # # # # # #
# tpms_wdt.py           #
# MarooElectronics Inc. #
# # # # # # # # # # # # #

# Import Standard Modules
import time, os

# Import User Modules
import tpms_sbc, tpms_log


# Module Run
def run():
    reset_cnt = 0

    while True:
        time.sleep(1.0)

        result = os.popen('ping -c 1 -W 10 %s' % tpms_sbc.svip_read())
        for line in result.readlines():
            if ' 0%' in line:
                reset_cnt = 0
        if reset_cnt:
            print('RESET_COUNT = %d' % reset_cnt)

        if reset_cnt >= 60:
            tpms_log.warning("Network Error Reboot")
            os.popen('sudo reboot')
        else:
            reset_cnt += 1


