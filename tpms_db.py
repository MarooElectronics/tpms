# -*- coding: utf-8 -*-

# # # # # # # # # # # # #
# tpms_ctrl.py          #
# MarooElectronics Inc. #
# # # # # # # # # # # # #

# Import Standard Modules
import os, _mysql

# Import User Modules


# Module Variables


# Module Initialization
try:
    for line in open('/root/tpms/files/conf.ini', 'r').read().splitlines():
        if 'db_host' in line:
            db_host = line.split('=')[1]
        if 'db_ID' in line:
            db_ID = line.split('=')[1]
        if 'db_PW' in line:
            db_PW = line.split('=')[1]
        if 'db_table_data' in line:
            db_table_data = line.split('=')[1]
        if 'db_table_record' in line:
            db_table_record = line.split('=')[1]
        if 'db_char' in line:
            db_char = line.split('=')[1]
        if 'eq_ip' in line:
            eq_ip = line.split('=')[1]
            table_name = '_' + line.split('.')[0].split('=')[1] + '_' + line.split('.')[1] + \
                         '_' + line.split('.')[2] + '_' + line.split('.')[3]
except Exception as e:
    print("[Don't init] DB Module - %s" % e)


# Module Function
def query(db_table, query):
    conn = _mysql.connect(host=db_host, user=db_ID, passwd=db_PW, db=db_table, connect_timeout=3)
    conn.query(query)

    # SQL문 실행
    # curs.execute(query)
    # conn.commit()

    # 데이타 Fetch
    rdata = conn.use_result()
    conn.close()

    return rdata


def init_record():
    record_table_column = '''
    date TIMESTAMP NOT NULL,
    volt_1 VARCHAR(200) NOT NULL DEFAULT "",
    curr_1 VARCHAR(200) NOT NULL DEFAULT "",
    state_1 VARCHAR(200) NOT NULL DEFAULT "",
    volt_2 VARCHAR(200) NOT NULL DEFAULT "",
    curr_2 VARCHAR(200) NOT NULL DEFAULT "",
    state_2 VARCHAR(200) NOT NULL DEFAULT "",
    volt_3 VARCHAR(200) NOT NULL DEFAULT "",
    curr_3 VARCHAR(200) NOT NULL DEFAULT "",
    state_3 VARCHAR(200) NOT NULL DEFAULT "",
    volt_4 VARCHAR(200) NOT NULL DEFAULT "",
    curr_4 VARCHAR(200) NOT NULL DEFAULT "",
    state_4 VARCHAR(200) NOT NULL DEFAULT "",
    volt_5 VARCHAR(200) NOT NULL DEFAULT "",
    curr_5 VARCHAR(200) NOT NULL DEFAULT "",
    state_5 VARCHAR(200) NOT NULL DEFAULT "",
    temp VARCHAR(200) NOT NULL DEFAULT "",
    humi VARCHAR(200) NOT NULL DEFAULT "",
    note VARCHAR(200) NOT NULL DEFAULT ""
    '''

    # Check Table
    try:
        recv = query(db_table_record, "SHOW TABLES LIKE '{}'".format(table_name))[0][0]
    except Exception as e:
        recv = ''

    try:
        if not table_name in recv:
            # Create Table
            query(db_table_record, "create table {}({})".format(table_name, record_table_column))

        # query(db_table_record, "insert into note values {}", table_name)
    except Exception as e:
        print(e)


def send_record(value):
    str = "null"
    for line in value:
        str += ", '{}'".format(line)
    str += ", ''"

    query(db_table_record, "insert into {} values({})".format(table_name, str))


def read_event():
    buf = []
    try:
        for line in query(db_table_data, "select * from {} where {} = '{}'".format('event_data', 'IP', eq_ip)):
            buf.append(line[1])
    except Exception as e:
        print(e)
    return buf


def send_event(value):
    query(db_table_data, "insert into {} values('{}', '{}')".format('event_data', eq_ip, value))


def del_event(value):
    buf = ''
    try:
        query(db_table_data, "delete from {} where {} = '{}' and  {} = '{}'".format('event_data', 'IP', eq_ip, 'content', value))
    except Exception as e:
        print(e)

    return buf


def send_now(value):
    str = "IP = '{}', ".format(eq_ip)
    str += "volt_1 = '{}', ".format(value[0])
    str += "curr_1 = '{}', ".format(value[1])
    str += "state_1 = '{}', ".format(value[2])
    str += "volt_2 = '{}', ".format(value[3])
    str += "curr_2 = '{}', ".format(value[4])
    str += "state_2 = '{}', ".format(value[5])
    str += "volt_3 = '{}', ".format(value[6])
    str += "curr_3 = '{}', ".format(value[7])
    str += "state_3 = '{}', ".format(value[8])
    str += "volt_4 = '{}', ".format(value[9])
    str += "curr_4 = '{}', ".format(value[10])
    str += "state_4 = '{}', ".format(value[11])
    str += "volt_5 = '{}', ".format(value[12])
    str += "curr_5 = '{}', ".format(value[13])
    str += "state_5 = '{}', ".format(value[14])
    str += "temp = '{}', ".format(value[15])
    str += "humi = '{}'".format(value[16])
    str += "note = '{}'".format('OK')

    print("update {} set {} where IP = '{}'".format('now_data', str, eq_ip))
    query(db_table_data, "update {} set {} where IP = '{}'".format('now_data', str, eq_ip))

def send_now_err(value):
    str = "IP = '{}', ".format(eq_ip)
    str += "note = '{}'".format(value)

    print("update {} set {} where IP = '{}'".format('now_data', str, eq_ip))
    query(db_table_data, "update {} set {} where IP = '{}'".format('now_data', str, eq_ip))

# Module Run


