#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#   Author          :   Viacheslav Zamaraev
#   email           :   zamaraev@gmail.com
#   Script Name     : 01_csv_to_pg.py
#   Created         : 03 August 2020
#   Last Modified	: 03 August 2020
#   Version		    : 1.0
#   PIP             : pip install tqdm peewee psycopg2 psycopg2-binary
#   RESULT          : csv file with columns: FILENAME;...LASTACCESS
# Modifications	: 1.1 -
#               : 1.2 -
#
# Description   : get lines in each csv fle in folder and put to PG
# In PSQL:
# create database udatadb2;
# create user udatauser2 with encrypted password 'secret_password';
# grant all privileges on database udatadb2 to udatauser2;

import os  # Load the Library Module
import os.path
from datetime import datetime
import csv
import logging
from itertools import (takewhile, repeat)

try:
    from tqdm import tqdm
except Exception as e:
    print("Exception occurred " + str(e))
    print("try: pip install tqdm")

# non standard packages
try:
    from peewee import *
except Exception as e:
    print("Exception occurred " + str(e))
    print("try: pip install peewee")


#from . import cfg  # some global configurations
#from . import gfiletools  # some global configurations
import cfg
import gfiletools
import models

#from src.models import Udata





def get_extension(filename=''):
    basename = os.path.basename(filename)  # os independent
    ffile = filename.split('\\').pop().split('/').pop()
    ext = '.'.join(ffile.split('.')[1:])

    if len(ext):
        return '.' + ext if ext else None
    else:
        return ''


def get_file_name_with_extension(path=''):
    # ext = get_extension(path)
    return os.path.split(path)[1]
    # if len(ext):
    #     return path.split('\\').pop().split('/')[0]
    # else:
    #     return path.split('\\').pop().split('/').pop()

    # return path.split('\\').pop().split('/')[0]        #  path.split('\\').pop().split('/').pop().rsplit('.', 1)[0]


def get_file_name_without_extension(path=''):
    ext = get_extension(path)
    if len(ext):
        return path.split('\\').pop().split('/').pop().rsplit(ext, 1)[0]
    else:
        return path.split('\\').pop().split('/').pop()
    # return path.split('\\').pop().split('/').pop().rsplit(get_extension(path), 1)[0]


def file_rows_count(filename):
    rowcount = 0
    try:
        f = open(filename, 'rb')
        bufgen = takewhile(lambda x: x, (f.raw.read(1024 * 1024) for _ in repeat(None)))
        rowcount = sum(buf.count(b'\n') for buf in bufgen)
        return rowcount
    except Exception as e:
        ss = "Exception occurred file_rows_count" + str(e)
        print(ss)
        logging.error(ss)
    return rowcount


def csv_file_out_create():
    csv_dict = cfg.csv_dict
    file_csv = str(os.path.join(gfiletools.get_output_directory(), cfg.file_csv))  # from cfg.file
    # Если выходной CSV файл существует - удаляем его
    if os.path.isfile(file_csv):
        os.remove(file_csv)
    with open(file_csv, 'w', newline='', encoding='utf-8') as csv_file:  # Just use 'w' mode in 3.x
        csv_file_open = csv.DictWriter(csv_file, csv_dict.keys(), delimiter=cfg.csv_delimiter)
        csv_file_open.writeheader()


def get_list_csv_dir(dir_input=''):
    listdir = []
    try:
        for root, subdirs, files in os.walk(dir_input):
            for file in os.listdir(root):
                file_path = str(os.path.join(root, file))
                # .lower() - под линуксом есть разница!!!
                ext = '.'.join(file.split('.')[1:]).lower()
                file_name = file.lower()
                if os.path.isfile(file_path) and file_name.endswith('.csv'):  # ext == "csv":
                    # print(file_path)
                    listdir.append(file_path)
    except Exception as e:
        ss = "Exception occurred get_list_csv_dir" + str(e)
        print(ss)
        logging.error(ss)
    return listdir


'''
    PG Create tables
'''
def pg_create_tables():
    pass
    # # db = SqliteDatabase('zsniigg.db')
    # db = peewee.PostgresqlDatabase(cfg.database, host=cfg.host, port='5432', user=cfg.user, password=cfg.user_password,
    #                         autocommit=True, autorollback=True)  # )
    # # db = PostgresqlDatabase(cfg.database, user=cfg.user, password=cfg.user_password)   # host=cfg.host )
    # # db.autorollback = True
    # db.connect()
    # try:
    #     db.create_tables([models.Udata], safe=True)
    # except peewee.InternalError as px:
    #     print(str(px))

    # db.drop_tables([Udata])



'''
    Do many csv files and make one csv file big
'''
def csv_file_to_pg(filename_with_path=''):
    csv_dict = cfg.csv_dict
    dir_out = gfiletools.get_output_directory()
    file_csv = str(os.path.join(dir_out, cfg.file_csv))
    # db = PostgresqlDatabase(cfg.database, host=cfg.host, port=None, user=cfg.user, password=cfg.user_password,
    #                         autocommit=True, autorollback=True)  # )
    # db.connect()







def do_multithreading(dir_input=''):
    list_csv = get_list_csv_dir(dir_input)
    dir_out = gfiletools.get_output_directory()
    # for f in list_csv:
    #     csv_file_to_pg(f)
    csv_file_to_pg(list_csv[1])
    # csv_file_to_pg(list_csv[2])
    # csv_file_to_pg(list_csv[5])
    # csv_file_to_pg(list_csv[6])
    # csv_file_to_pg(list_csv[27])
    # csv_file_to_pg(list_csv[28])



# ---------------- do main --------------------------------
def main():
    time1 = datetime.now()
    print('Starting at :' + str(time1))

    dir_input = gfiletools.get_input_directory()
    csv_file_out_create()
    gfiletools.do_log_file()
    pg_create_tables()

    do_multithreading(dir_input)

    time2 = datetime.now()
    print('Finishing at :' + str(time2))
    print('Total time : ' + str(time2 - time1))
    print('DONE !!!!')


if __name__ == '__main__':
    main()
