# -*- coding: utf-8 -*-

# # # # # # # # # # # # #
# tpms_sbc.py           #
# MarooElectronics Inc. #
# # # # # # # # # # # # #

# Import Standard Modules
import os, time

# Import User Modules
# import tpms_log

# Module Variables
version = '1.0.20180908'

# Module Function
def ver_read():
    return version


def systime():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def interfaces_read(index):
    # interfaces 파일 읽기
    try:
        with open("/etc/network/interfaces", 'r') as f:
            f_list = f.readlines()

        for line in f_list:
            if index in line:
                return line.split(' ')[1].splitlines()[0]
    except Exception as e:
        pass
        # tpms_log.warning(e)


def interfaces_write(index, value):
    # interfaces 파일 쓰기
    with open("/etc/network/interfaces", 'r') as f:
        f_list = f.readlines()

    for i, line in enumerate(f_list):
        if index in line:
            f_list[i] = '%s %s\r\n' % (index, value)

    try:
        with open("/etc/network/interfaces", 'w') as f:
            for line in f_list:
                f.write(line)
    except Exception as e:
        pass
        # tpms_log.warning(e)


def ip_read():
    try:
        with open("/etc/network/interfaces", 'r') as f:
            f_list = f.readlines()

        for line in f_list:
            if 'address' in line:
                return line.split(' ')[1].splitlines()[0]

    except Exception as e:
        # tpms_log.warning(e)
        return '0.0.0.0'


def svip_read():
    try:
        with open("/etc/network/interfaces", 'r') as f:
            f_list = f.readlines()

        for line in f_list:
            if 'SVIP' in line:
                return line.split(' ')[1].splitlines()[0]

    except Exception as e:
        # tpms_log.warning(e)
        return '0.0.0.0'


def conf_read(index):
    # 설정 파일 읽기
    with open(os.getcwd()+'/files/conf.ini', 'r') as f:
        f_list = f.readlines()

    for line in f_list:
        if index in line:
            return line.split('=')[1].splitlines()[0]


def conf_write(index, value):
    # 설정 파일 쓰기
    with open(os.getcwd()+'/files/conf.ini', 'r') as f:
        f_list = f.readlines()

    flag = 0

    for i, line in enumerate(f_list):
        if index in line:
            f_list[i] = '%s=%s\r\n' % (index, value)
            flag = 1

    # 설정값이 없으면 추가
    if flag == 0:
        try:
            with open(os.getcwd() + '/files/conf.ini', 'a') as f:
                    f.write('%s=%s\r\n' % (index, value))
        except Exception as e:
            pass
            # tpms_log.warning(e)

    # 설정값이 있으면 덮어쓰기
    else:
        try:
            with open(os.getcwd() + '/files/conf.ini', 'w') as f:
                for line in f_list:
                    f.write(line)
        except Exception as e:
            pass
            # tpms_log.warning(e)


def help_read():
    # 도움말 파일 읽기
    with open(os.getcwd() + '/files/help.txt', 'r') as f:
        f_list = f.readlines()
    return f_list
