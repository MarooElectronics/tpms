# -*- coding: utf-8 -*-

# # # # # # # # # # # # #
# tpms_main.py          #
# MarooElectronics Inc. #
# # # # # # # # # # # # #

# Import Standard Modules
import threading, time

# Import User Modules
import tpms_ctrl, tpms_db, tpms_glcd
# , tpms_wdt, tpms_tcp, tpms_telnet, tpms_log, tpms_console


# Main Program Run
if __name__ == "__main__":

    # tpms_log.info("Program Start")

    # # # Thread Settings # # #

    # SBC Control Setting
    th_ctrl = threading.Thread(target=tpms_ctrl.run)
    th_ctrl.daemon = True
    th_ctrl.start()

    # GLCD Setting
    th_glcd = threading.Thread(target=tpms_glcd.run)
    th_glcd.daemon = True
    th_glcd.start()

    # TCP LISTEN Setting
    # th_tcp = threading.Thread(target=tpms_tcp.run)
    # th_tcp.daemon = True
    # th_tcp.start()

    # TELNET LISTEN Setting
    # th_telnet = threading.Thread(target=tpms_telnet.run)
    # th_telnet.daemon = True
    # th_telnet.start()

    # Watchdog Setting
    # th_watchdog = threading.Thread(target=tpms_wdt.run)
    # th_watchdog.daemon = True
    # th_watchdog.start()

    # Console Setting
    # th_cs = threading.Thread(target=tpms_console.run)
    # th_cs.daemon = True
    # th_cs.start()

    # tpms_tcp.send('(ION,%s)' % tpms_sbc.ip_read())


    # # # Main Program # # #

    # DB Init
    tpms_db.init_record()

    cnt = 0

    while True:
        time.sleep(1)

        try:
            if cnt > 5:
                cnt = 0
                try:
                    buf = tpms_ctrl.send('(AL)')
                    if '(AL' in buf:
                        list_buf = buf.split('AL,')[1].split(')')[0].split(',')
                        tpms_db.send_now(list_buf)
                        tpms_db.send_record(list_buf)
                    else:
                        tpms_db.send_now_err('!MCU Disconnected')


                except Exception as e:
                    print(e)
            else:
                cnt += 1

            # try:
            #     db_buf = tpms_db.read_event()
            #
            #     for line in db_buf:
            #
            #         if '(s_cs' in line:
            #             tpms_db.del_event(line)
            #             cs_num = line.split('(s_cs')[1].split(';')[0]
            #             cs_data = line.split(';')[1].split(')')[0]
            #
            #             cs_recv = 0
            #             # cs_recv = tpms_console.send(cs_num, cs_data.encode())
            #
            #             tpms_db.send_event("(cs%s;%s)" % (cs_num, cs_recv))
            #
            #         elif '(OP' in line:
            #             tpms_db.del_event(line)
            #             buf = tpms_ctrl.send(line.encode())
            #             if '(AL' in buf:
            #                 list_buf = buf.split('AL,')[1].split(')')[0].split(',')
            #                 tpms_db.send_now(list_buf)
            #                 tpms_db.send_record(list_buf)
            #
            #         elif '(AU)' in db_buf:
            #             tpms_db.del_event(line)
            #             buf = tpms_ctrl.send(line.encode())
            #             if '(AL' in buf:
            #                 list_buf = buf.split('AL,')[1].split(')')[0].split(',')
            #                 tpms_db.send_now(list_buf)
            #                 tpms_db.send_record(list_buf)
            #
            # except Exception as e:
            #     pass
            #     # tpms_log.warning("Main Program : %s" % e)

        except Exception as e:
            pass
            # tpms_log.warning("Program Stop : %s" % e)
