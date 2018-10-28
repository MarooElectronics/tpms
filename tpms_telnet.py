# -*- coding: utf-8 -*-

# # # # # # # # # # # # #
# tpms_telnet.py        #
# MarooElectronics Inc. #
# # # # # # # # # # # # #

# Import Standard Modules
import time, os, socket

# Import User Modules
import tpms_sbc, tpms_log, tpms_ctrl


# Module Run
def run():
    buf_list = []

    while True:
        time.sleep(1)

        try:
            telnetSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            telnetSocket.bind(('', 23))
            telnetSocket.listen(1)
            tpms_log.info('Telnet Listen...')

        except Exception as e:
            telnetSocket = ''
            tpms_log.warning('Telnet Listen Failed... Restart...')

        while telnetSocket:
            time.sleep(0.1)

            telnetClient, telnet_addr = telnetSocket.accept()

            tpms_log.info('Telnet Connected from : %s' % telnet_addr[0])

            buf_data = ''
            buf_index = -1

            if telnetClient:
                telnetClient.send('\r\nGL_HAMS> ')

                while telnetClient:
                    time.sleep(1)

                    print(telnetClient)

                    try:
                        data = telnetClient.recv(1)

                        if data:
                            #print ord(data)

                            if data == '\b':
                                if len(buf_data):
                                    telnetClient.send(' \b')
                                    buf_data = buf_data[0:(len(buf_data)-1)]
                                else:
                                    telnetClient.send(' ')

                            else:
                                buf_data += data

                        if '\r\n' in buf_data:

                            #mars_tcp.tcpSend('(IT,'+buf_data+')'+tpms_sbc.ip_read())

                            if 'help' in buf_data:
                                for line in tpms_sbc.help_read():
                                    telnetClient.send(line)

                            #Show Commands
                            elif 'show status' in buf_data:
                                telnetClient.send('Type : GL-HAMS\r\n')
                                telnetClient.send('Ver  : ' + tpms_sbc.version() + '\r\n')
                                telnetClient.send('Time : ' + tpms_sbc.systime() + '\r\n')

                            elif 'show ip' in buf_data:
                                telnetClient.send('EQ_IP : '+tpms_sbc.interfaces_read('address')+'\r\n')
                                telnetClient.send('EQ_SM : '+tpms_sbc.interfaces_read('netmask')+'\r\n')
                                telnetClient.send('EQ_GW : '+tpms_sbc.interfaces_read('gateway')+'\r\n')
                                telnetClient.send('EQ_PT : '+tpms_sbc.interfaces_read('#EQPT')+'\r\n')
                                telnetClient.send('SV_IP : '+tpms_sbc.interfaces_read('#SVIP')+'\r\n')
                                telnetClient.send('SV_PT : '+tpms_sbc.interfaces_read('#SVPT')+'\r\n')

                            elif 'show time' in buf_data:
                                telnetClient.send('Time : ' + tpms_sbc.systime() + '\r\n')


                            #Setting Commands
                            elif 'set ip ' in buf_data:
                                tpms_sbc.interfaces_write('address', buf_data.split('set ip ')[1].splitlines()[0])
                                telnetClient.send('\r\nset ip : ' + tpms_sbc.interfaces_read('address') + '\r\n')

                            elif 'set sm ' in buf_data:
                                tpms_sbc.interfaces_write('netmask', buf_data.split('set sm ')[1].splitlines()[0])
                                telnetClient.send('\r\nset sm : ' + tpms_sbc.interfaces_read('netmask') + '\r\n')

                            elif 'set gw ' in buf_data:
                                tpms_sbc.interfaces_write('gateway', buf_data.split('set gw ')[1].splitlines()[0])
                                tpms_sbc.interfaces_write('broadcast', buf_data.split('set gw ')[1].splitlines()[0])
                                telnetClient.send('\r\nset gw : ' + tpms_sbc.interfaces_read('gateway') + '\r\n')

                            elif 'set port ' in buf_data:
                                tpms_sbc.interfaces_write('#EQPT', buf_data.split('set port ')[1].splitlines()[0])
                                telnetClient.send('\r\nset port : ' + tpms_sbc.interfaces_read('#EQPT') + '\r\n')

                            elif 'set svr ip ' in buf_data:
                                tpms_sbc.interfaces_write('#SVIP', buf_data.split('set svr ip ')[1].splitlines()[0])
                                telnetClient.send('\r\nset svr ip : ' + tpms_sbc.interfaces_read('#SVIP') + '\r\n')

                            elif 'set svr port ' in buf_data:
                                tpms_sbc.interfaces_write('#SVPT', buf_data.split('set svr port ')[1].splitlines()[0])
                                telnetClient.send('\r\nset svr port : ' + tpms_sbc.interfaces_read('#SVPT') + '\r\n')


                            #Control Commands
                            elif 'power' in buf_data:
                                num = int(buf_data.split('power')[1].split(' ')[0]) - 1
                                if 'on' == buf_data.split(' ')[1].splitlines()[0]:
                                    value = 1
                                else:
                                    value = 0
                                tpms_ctrl.power(num, value)

                            elif 'door' in buf_data:
                                num = int(buf_data.split('door')[1].split(' ')[0])
                                if 'lock' == buf_data.split(' ')[1].splitlines()[0]:
                                    value = 1
                                else:
                                    value = 2
                                tpms_ctrl.door(num, value)


                            #System Commands
                            elif 'reboot' in buf_data:
                                telnetClient.send('System Rebooting!!!\r\n')
                                os.system('sudo reboot')
                            elif 'exit' in buf_data:
                                telnetClient.close()
                                telnetClient = ''
                                break

                            else:
                                telnetClient.send('?\r\n')


                            if buf_data != '\r\n':
                                buf_list.append(buf_data.split('\r\n')[0])

                            if len(buf_list) > 10:
                                del(buf_list[0])

                            # print(buf_list)

                            telnetClient.send('\r\nGL_HAMS> ')
                            buf_data = ''
                            buf_index = -1


                        if '%c%c%c' %(27, 91, 65) in buf_data:
                            buf_data = buf_data[0:len(buf_data)-3]

                            if buf_index < len(buf_list):
                                buf_index += 1

                                for i in range(len(buf_data)):
                                    telnetClient.send('\b \b')

                                buf_data = buf_list[len(buf_list) - (buf_index+1)]

                                telnetClient.send(buf_data)


                        elif '%c%c%c' % (27, 91, 66) in buf_data:
                            buf_data = buf_data[0:len(buf_data) - 3]

                            if buf_index > 0:
                                buf_index -= 1

                                for i in range(len(buf_data)):
                                    telnetClient.send('\b \b')

                                buf_data = buf_list[len(buf_list) - (buf_index+1)]

                                telnetClient.send(buf_data)

                            elif buf_index == 0:
                                for i in range(len(buf_data)):
                                    telnetClient.send('\b \b')
                                buf_data = ''

                    except socket.timeout:
                        telnetClient.close()
                        telnetClient = ''

                    except Exception as e:
                        telnetClient.close()
                        telnetClient = ''
                        tpms_log.warning('telnet: %s' % e)

                tpms_log.info('Telnet Disconnected from : %s' % telnet_addr[0])

        telnetSocket.close()
