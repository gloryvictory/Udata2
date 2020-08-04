#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#   Author          :   Viacheslav Zamaraev
#   email           :   zamaraev@gmail.com
#   Script Name     : 01_csv_to_pg.py
#   Created         : 03 August 2020
#   Last Modified	: 03 August 2020
#   Version		    : 1.0
#   PIP             : pip install tqdm peewee
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
import sys
# import time
from sys import platform as _platform
# from time import strftime  # Load just the strftime Module from Time
from datetime import datetime
import csv
# import codecs
import logging
from itertools import (takewhile, repeat)
#import codecs

# non standard packages
try:
    from tqdm import tqdm
except Exception as e:
    print("Exception occurred " + str(e))
    print("try: pip install tqdm")

# non standard packages
try:
    import peewee
except Exception as e:
    print("Exception occurred " + str(e))
    print("try: pip install peewee")

import cfg  # some global configurations


def get_input_directory_from_cfg():
    directory_in = str(os.getcwd())
    if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
        if os.path.isdir(cfg.folder_in_linux):
            print('Input directory from a config file: ' + cfg.folder_in_linux)
            return cfg.folder_in_linux
        else:
            print(
                'Input directories from config wrong: ' + cfg.folder_in_linux + ' Using current directory: ' + directory_in)
            return directory_in
    if _platform == "win32" or _platform == "win64":  # Windows or Windows 64-bit
        if os.path.isdir(cfg.folder_in_win):
            print('Input directory from a config file: ' + cfg.folder_in_win)
            return cfg.folder_in_win
        else:
            print(
                'Input directories from config wrong: ' + cfg.folder_in_win + ' Using current directory: ' + directory_in)
            return directory_in
    return directory_in


def get_input_directory():
    # get from config
    directory_in = str(os.getcwd())
    # if only run the script (1 argument)
    if len(sys.argv) == 1:  # there is no arguments in command line
        return get_input_directory_from_cfg()

    if len(sys.argv) == 2:  # there is only one argument in command line
        directory_in = str(sys.argv[1:][0])
        if os.path.isdir(directory_in):
            return directory_in
        else:
            return get_input_directory_from_cfg()

    if len(sys.argv) > 2:  # there is only one argument in command line
        print("Arguments much more than 1! Please use only path as an argument. (Script.py /mnt/some_path) ")
        print(sys.argv, len(sys.argv))
        exit(1)
    return directory_in


def get_output_directory():
    dir_out = str(os.getcwd())
    # Linux platform
    if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
        dir_out = cfg.folder_out_linux
        print('Output directory from config file: ' + dir_out)
        if os.path.exists(dir_out) and os.path.isdir(dir_out):
            return dir_out
    if _platform == "win32" or _platform == "win64":  # Windows or Windows 64-bit
        dir_out = cfg.folder_win_out
        print('Output directory from config file' + dir_out)
        if os.path.exists(dir_out) and os.path.isdir(dir_out):
            return dir_out
    else:
        print(
            'Output directories from config wrong: ' + cfg.folder_out_win + ' or ' + cfg.folder_out_linux + ' Using current directory: ' + dir_out)
    print('Using Output directory: ' + dir_out)
    return dir_out


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
    file_csv = str(os.path.join(get_output_directory(), cfg.file_csv))  # from cfg.file
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
    Do many csv files and make one csv file big
'''


def csv_file_to_pg(filename_with_path=''):
    csv_dict = cfg.csv_dict
    dir_out = get_output_directory()
    file_csv = str(os.path.join(dir_out, cfg.file_csv))

# db = SqliteDatabase('zsniigg.db')

    db = PostgresqlDatabase(cfg.database, host=cfg.host, port=None, user=cfg.user, password=cfg.user_password,
                            autocommit=True, autorollback=True)  # )

    # db = PostgresqlDatabase(cfg.database, user=cfg.user, password=cfg.user_password)   # host=cfg.host )
    # db.autorollback = True

    # Model for our entry table
    class Udata(Model):
        compname = CharField(max_length=250, default="")
        disk = CharField(max_length=1, default="")
        fullname = TextField(default="") #CharField(max_length=250, default="")
        size = BigIntegerField(default=0) # Length - in csv;
        ctime = DateTimeField(default=datetime.now)
        mtime = DateTimeField(default=datetime.now)
        atime = DateTimeField(default=datetime.now)
        filename_long = CharField(max_length=250, default="") # name in CSV File
        ext_long = CharField(max_length=250, default="")
        ext_shot = CharField(max_length=250, default="") # extension in CSV File
        date = CharField(max_length=10, default="")
        year = IntegerField()
        month = IntegerField()
        fio = CharField(max_length=250, default="")
        otdel = CharField(max_length=250, default="")
        textfull = TextField(default="")
        textless = TextField(default="")
        MD5FULLNAME = CharField(max_length=50, default="")
        MD5FILE = CharField(max_length=50, default="")
        lastupdate = DateTimeField(default=datetime.now)

        class Meta:
            database = db
            # indexes = (
            #     # create a unique on ...
            #     (('compname'), True),)
    db.connect()
    #db.drop_tables([Udata])
    db.create_tables([Udata], safe=True)



def do_multithreading(dir_input=''):
    list_csv = get_list_csv_dir(dir_input)
    dir_out = get_output_directory()
    # for f in list_csv:
    #     csv_file_to_pg(f)
     csv_file_to_pg(list_csv[1])
    # csv_file_to_pg(list_csv[2])
    # csv_file_to_pg(list_csv[5])
    # csv_file_to_pg(list_csv[6])
    # csv_file_to_pg(list_csv[27])
    # csv_file_to_pg(list_csv[28])


def do_log_file():
    for handler in logging.root.handlers[:]:  # Remove all handlers associated with the root logger object.
        logging.root.removeHandler(handler)
    dir_out = get_output_directory()
    file_log = str(os.path.join(dir_out, cfg.file_log))  # from cfg.file
    if os.path.isfile(file_log):  # Если выходной LOG файл существует - удаляем его
        os.remove(file_log)
    logging.basicConfig(filename=file_log, format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG,
                        filemode='w')  #
    logging.info(file_log)


# ---------------- do main --------------------------------
def main():
    time1 = datetime.now()
    print('Starting at :' + str(time1))

    dir_input = get_input_directory()
    csv_file_out_create()
    do_log_file()

    do_multithreading(dir_input)

    time2 = datetime.now()
    print('Finishing at :' + str(time2))
    print('Total time : ' + str(time2 - time1))
    print('DONE !!!!')


if __name__ == '__main__':
    main()
