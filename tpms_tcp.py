# -*- coding: utf-8 -*-

# # # # # # # # # # # # #
# tpms_tcp.py           #
# MarooElectronics Inc. #
# # # # # # # # # # # # #

# Import Standard Modules
import time, socket

# Import User Modules
import tpms_ctrl, tpms_sbc, tpms_log


# Module Function
def eco(read_data):
    try:
        if '(AT' in read_data:
            return '(AT)'
        else:
            return tpms_ctrl.send(read_data)

    except Exception as e:
        tpms_log.warning('TCP Eco Module - %s' % e)


# Module Run
def run():
    BUFSIZE = 1024

    while True:
        time.sleep(1)

        try:
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverSocket.bind(('', 3000))
            serverSocket.listen(3)
            tpms_log.info('Socket Listen...')

        except Exception as e:
            serverSocket = ''
            tpms_log.info('Socket Listen Failed... Restart...')

        while serverSocket:
            time.sleep(0.1)

            clientSocket, addr_info = serverSocket.accept()
            clientSocket.settimeout(3)

            try:
                data = clientSocket.recv(1024)

                if data:
                    tpms_log.info('[%s] RECV : %s' % (addr_info[0], data.splitlines()[0]))

                    send = eco(data)
                    clientSocket.send(send)
                    clientSocket.close()

                    tpms_log.info('[%s] SEND : %s' % (addr_info[0], send.splitlines()[0]))

            except socket.timeout:
                clientSocket.close()

            except Exception as e:
                clientSocket.close()
                tpms_log.warning('mars_tcp:%s' %e)


def send(value):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.settimeout(3)

    try:
        clientSocket.connect((tpms_sbc.interfaces_read('#SVIP'), int(tpms_sbc.interfaces_read('#SVPT'))))
        clientSocket.send(value)
        clientSocket.close()

    except socket.timeout:
        clientSocket.close()

    except Exception as e:
        tpms_log.warning("TCP Send Module - %s" % e)
        clientSocket.close()


