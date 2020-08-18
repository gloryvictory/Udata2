#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#   Author          :   Viacheslav Zamaraev
#   email           :   zamaraev@gmail.com
#   Script Name     : 01_csv_to_csvdetailed.py
#   Created         : 25th December 2019
#   Last Modified	: 25th December 2019
#   Version		    : 1.0
#   PIP             : pip install pewee, psycopg2
#   RESULT          : csv file with columns: FILENAME;...LASTACCESS
# Modifications	: 1.1 -
#               : 1.2 -
#
# Description   : This script will search some *.csv files in the given directory and makes CSV file with some information
# create database udatadb2;
# create user udatauser2 with encrypted password 'secret_password';
# grant all privileges on database udatadb2 to udatauser2;
# CREATE SCHEMA IF NOT EXISTS udataschema2  AUTHORIZATION udatauser2;
# CREATE EXTENSION postgis;

import os  # Load the Library Module
import os.path
import sys
import time
from sys import platform as _platform
from time import strftime  # Load just the strftime Module from Time
from datetime import datetime
import csv
import codecs
import logging
from itertools import (takewhile, repeat)

from peewee import *
from tqdm import tqdm
from tqdm import trange

# non standard packages

# try:
#     import peewee
# except Exception as e:
#     print("Exception occurred " + str(e), exc_info=True)
#     print("try: pip install peewee")


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
        #print('Output directory from config file: ' + dir_out)
        if os.path.exists(dir_out) and os.path.isdir(dir_out):
            return dir_out
    if _platform == "win32" or _platform == "win64":  # Windows or Windows 64-bit
        dir_out = cfg.folder_out_win
        #print('Output directory from config file' + dir_out)
        if os.path.exists(dir_out) and os.path.isdir(dir_out):
            return dir_out
    else:
        print(
            'Output directories from config wrong: ' + cfg.folder_out_win + ' or ' + cfg.folder_out_linux + ' Using current directory: ' + dir_out)
    print('Using Output directory: ' + dir_out)
    return dir_out


def get_file_name_with_extension(path=''):
    ext = get_extension(path)
    if len(ext):
        return path.split('\\').pop().split('/')[0]
    else:
        return path.split('\\').pop().split('/').pop()

    # return path.split('\\').pop().split('/')[0]        #  path.split('\\').pop().split('/').pop().rsplit('.', 1)[0]


def get_file_name_without_extension(path=''):
    ext = get_extension(path)
    if len(ext):
        return path.split('\\').pop().split('/').pop().rsplit(ext, 1)[0]
    else:
        return path.split('\\').pop().split('/').pop()
    # return path.split('\\').pop().split('/').pop().rsplit(get_extension(path), 1)[0]


def get_extension(filename=''):
    basename = os.path.basename(filename)  # os independent
    ffile = filename.split('\\').pop().split('/').pop()
    ext = '.'.join(ffile.split('.')[1:])

    if len(ext):
        return '.' + ext if ext else None
    else:
        return ''


def get_list_csv_dir(dir_input=''):
    listdir = []
    # Если выходной CSV файл существует - удаляем его
    file_csv = str(os.path.join(get_output_directory(), cfg.file_csv))  # from cfg.file
    if os.path.isfile(file_csv):
        os.remove(file_csv)

    with open(file_csv, 'w', newline='', encoding='utf-8') as csv_file:  # Just use 'w' mode in 3.x
        csv_file_open = csv.DictWriter(csv_file, cfg.csv_dict.keys(), delimiter=cfg.csv_delimiter)
        csv_file_open.writeheader()
    try:
        for root, subdirs, files in os.walk(dir_input):
            for file in os.listdir(root):
                file_path = str(os.path.join(root, file))
                # .lower() - под линуксом есть разница!!!
                ext = '.'.join(file.split('.')[1:]).lower()
                if os.path.isfile(file_path) and file_path.endswith('csv'):  # ext == "csv":
                    listdir.append(file_path)
    except Exception as e:
        print("Exception occurred get_list_csv_dir" + str(e))

    return listdir



def text_clear(str_input=''):
    ss = str_input.lower().strip()
    ss = ss.replace(":", " ")
    ss = ss.replace("\\", " ")
    ss = ss.replace(",", " ")
    ss = ss.replace(".", " ")
    ss = ss.replace("-", " ")
    ss = ss.replace(";", " ")
    ss = ss.replace("\"", "")
    ss = ss.replace("_", "")
    ss = ss.replace("\'", "")
    return ss


def file_get_row_count(filename):
    rowcount = 0
    try:
        f = open(filename, 'rb')
        bufgen = takewhile(lambda x: x, (f.raw.read(1024 * 1024) for _ in repeat(None)))
        rowcount = sum(buf.count(b'\n') for buf in bufgen)
        return rowcount
    except Exception as e:
        print("Exception occurred " + str(e))  # , exc_info=True
    return rowcount

'''
    Do many csv files and load to Database
'''


def do_csv_file_in_dir_out_to_db(filename_with_path=''):
    # db = SqliteDatabase('test.db')

    db = PostgresqlDatabase(cfg.database, host=cfg.host, port=5432, user=cfg.user, password=cfg.user_password,
                            autocommit=True, autorollback=True)  # )

    # db = PostgresqlDatabase(cfg.database, user=cfg.user, password=cfg.user_password)   # host=cfg.host )
    # db.autorollback = True

    # Model for our entry table
    class Udata2(Model):
        compname = CharField(max_length=250, default="")
        disk = CharField(max_length=2, default="")
        folder = TextField(default="")
        size = BigIntegerField(default=0)
        ctime = DateTimeField(default=datetime.now)
        atime = DateTimeField(default=datetime.now)
        mtime = DateTimeField(default=datetime.now)
        filename = CharField(max_length=250, default="")
        ext = CharField(max_length=10, default="")
        md5 = CharField(max_length=50, default="")

        is_profile = BooleanField(default=False)
        # filename_shot = CharField(max_length=250, default="")
        # ext_long = CharField(max_length=250, default="")

        # fullname = TextField(default="")
        # date = CharField(max_length=250, default="")
        # year = IntegerField()
        # month = IntegerField()
        # creationtime = DateTimeField(default=datetime.now)
        # fio = CharField(max_length=250, default="")
        # otdel = CharField(max_length=250, default="")
        # textfull = TextField(default="")
        # textless = TextField(default="")
        lastupdate = DateTimeField(default=datetime.now)

        class Meta:
            database = db
            # indexes = (
            #     # create a unique on ...
            #     (('compname'), True),)

    try:
        #db.connect(reuse_if_open=True)
        db.connect()
        db.create_tables([Udata2], safe=True)

    except InternalError as px:
        str_error = 'Exception! DB connect failed!  ' + str(px)
        print(str_error)
        logging.error(str_error)
    # db.drop_tables([Udata])

    file_csv = str(os.path.join(get_output_directory(), cfg.file_csv))  # from cfg.file
    print(file_csv)

    file_name = filename_with_path.split('.')[0]
    csv_dict = cfg.csv_dict
    for key in csv_dict:
        csv_dict[key] = ''

    with open(file_csv, 'a', newline='', encoding='utf-8') as csv_file:  # Just use 'w' mode in 3.x
        csv_file_open = csv.DictWriter(csv_file, cfg.csv_dict.keys(), delimiter=cfg.csv_delimiter)

        logging.info(file_csv)
        str_tmp = 'PID is: ' + str(os.getpid())
        print(str_tmp)
        logging.info(str_tmp)

        file_row_count = file_get_row_count(filename_with_path)
        if file_row_count > 2:

            f = codecs.open(filename_with_path, 'r', 'UTF-8')
            try:
                # get Headers from file (first line of file)

                for line in f:
                    len_current_line = len(str(line))
                    if len_current_line > 2:
                        ss = line.strip()
                        headers = ss.split(',')
                        headers2 = []
                        for header in headers:
                            ss = header.strip('\"')
                            headers2.append(ss)
                        str_tmp = 'Columns from csv_file: ' + str(len(headers)) + ' in File: ' + filename_with_path
                        #print(str_tmp)
                        logging.info(str_tmp)
                        column_names_in = cfg.csv_fieldnames_in
                        str_tmp = 'Columns from cfg: ' + str(len(column_names_in))
                        # print(str_tmp)
                        logging.info(str_tmp)
                        tt = [x for x in headers2 if x in column_names_in]  # [x for x in a if x in b]
                        str_tmp = 'Сolumns matched: ' + str(len(tt)) + ' Columns: ' + str(tt)
                        # print(str_tmp)
                        logging.info(str_tmp)
                        # do all lines in csv file
                        next(f)  # skip first line
                        break  # break here
                    else:
                        break  # break here
                if len_current_line > 2:
                    pbar = tqdm(total=file_row_count)
                    for line in f:
                        pbar.update(1)
                        data = str(line)
                        delimeters_in_row_count = data.count(cfg.csv_delimiter)
                        column_count = len(column_names_in) - 1

                        if delimeters_in_row_count != column_count:
                            _error = 'in current line there are some troubles in columns: ' + data
                            print(_error)
                            logging.error(_error)
                            _error = 'delimeters in row count: ' + str(delimeters_in_row_count) + ' but columns count ' + str(column_count)
                            print(_error)
                            logging.error(_error)
                        else:

                            try:

                                _UDATA = Udata2()
                                current_line = str(line).split(cfg.csv_delimiter)
                                compname = current_line[0].strip("\"")
                                file_full_path_name = current_line[1].strip("\"")
                                #print(file_full_path_name)
                                folder = file_full_path_name
                                disk = file_full_path_name.split(":")[0]
                                #_UDATA.get(_UDATA.username == 'Charlie')
                                # qq = _UDATA.select().where(
                                #     (_UDATA.compname == compname) and (_UDATA.disk == disk)).count()

                                size = current_line[2].strip("\"")
                                ctime = current_line[3].strip()
                                mtime = current_line[4].strip()
                                atime = current_line[5].strip()

                                filename = current_line[6].strip()
                                str_ext = current_line[7].strip()
                                ext = str_ext.replace(".", "")
                                str_md5  = current_line[8].strip().lower()
                                md5 = ''
                                if str_md5.find('nomd5') > -1:
                                    md5 = ''
                                else:
                                    md5 = str_md5

                                _folder = folder.lower().split(':')[1]
                                is_profile = False
                                if _folder.startswith("\\users"):
                                    is_profile = True


                                _UDATA.compname = compname
                                _UDATA.disk = disk
                                _UDATA.folder = folder
                                _UDATA.size = size
                                _UDATA.ctime = ctime
                                _UDATA.mtime = mtime
                                _UDATA.atime = atime
                                _UDATA.filename = filename
                                _UDATA.ext = ext
                                _UDATA.md5 = md5
                                _UDATA.is_profile = is_profile
                                #_UDATA.save(force_insert=True)
                                _UDATA.save()




                                # tmpstr = current_line[3].replace(",", "")
                                # tmpstr = tmpstr.replace("\"", "")
                                # creation_time = tmpstr.strip()
                                #
                                # _UDATA.compname = compname
                                # _UDATA.disk = file_full_path_name.split(":")[0]
                                # _folder = str(os.path.dirname(os.path.abspath(file_full_path_name)))
                                # _UDATA.folder = _folder
                                # _folder = _folder.lower()
                                # _is_profile = False
                                # if _folder.startswith("c:\\users"):
                                #     _is_profile = True
                                #
                                # _UDATA.is_profile = _is_profile
                                # _UDATA.filename_long = get_file_name_with_extension(file_full_path_name)
                                # _UDATA.filename_shot = get_file_name_without_extension(file_full_path_name)
                                # _ext_long = get_extension(file_full_path_name)
                                # _UDATA.ext_long = _ext_long
                                # _UDATA.ext_shot = _ext_long.split(".")[-1].lower()
                                # _UDATA.size = length
                                # _UDATA.fullname = file_full_path_name
                                # _date = creation_time.split()[0]
                                # _UDATA.date = _date
                                # _UDATA.year = _date.split(".")[-1]
                                # _UDATA.month = creation_time.split(".")[1]
                                # _UDATA.creationtime = creation_time
                                # _UDATA.fio = ''
                                # _UDATA.otdel = ''
                                #
                                # _UDATA.textfull = text_clear(file_full_path_name)
                                # _UDATA.textless = text_clear(file_full_path_name)  # need to tranformate
                                # _UDATA.lastupdate = str(datetime.now())

                                # logging.info(csv_dict['FILENAME_LONG'])

                                # print(line)
                                # _UDATA.save()


                                #
                                # csv_file_open.writerow(csv_dict)
                            except Exception as e:
                                # print("Exception occurred do_csv_file_in_dir_out_to_db - UDATA.SAVE" + str(e))  # , exc_info=True
                                pass  # пропускаем

                            except IntegrityError:
                                # Person.get(Person.uid == iid)
                                _error = "IntegrityError Exception!!!: "
                                print(_error)
                                logging.error(_error)
                    pbar.close()
            except Exception as e:
                print("Exception occurred do_csv_file_in_dir_out_to_db" + str(e))  # , exc_info=True
            f.close()

        else:
            _error = 'Row count: ' + str(file_row_count) + ' in file ' + filename_with_path
            print(_error)
            logging.info(_error)



##let try multithreading
def do_multithreading(dir_input=''):
    list_csv = get_list_csv_dir(dir_input)
    # do_csv_file_in_dir_out_to_db(list_csv[0])
    # # do_csv_file_in_dir_out_to_db(list_csv[1])
    # # do_csv_file_in_dir_out_to_db(list_csv[10])
    # # do_csv_file_in_dir_out_to_db(list_csv[11])
    # ll = []
    # ll.append(list_csv[0])
    # ll.append(list_csv[1])
    # ll.append(list_csv[2])
    # ll.append(list_csv[3])
    # ll.append(list_csv[4])

    # for i in trange(len(list_csv), file=sys.stdout, leave=False, unit_scale=True, desc='File '):
    #     do_csv_file_in_dir_out_to_db(list_csv[i])


    try:
        from multiprocessing import Pool
    except Exception as e:
        print("Exception occurred do_multithreading" + str(e))

    try:
        # кол-во потоков
        with Pool(2) as p:
             #p.map(do_csv_file_in_dir_out_to_db, list_csv)
             p.map(do_csv_file_in_dir_out_to_db, list_csv)
    except Exception as e:
        print("Exception occurred do_multithreading" + str(e))

    # #map(save_file_html_by_url, url_list)


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

    do_log_file()
    # Creating SQLIte DB

    # global _UDATA
    # nrows = _UDATA.delete().execute()

    do_multithreading(dir_input)

    # csv2xls()

    time2 = datetime.now()
    print('Finishing at :' + str(time2))
    print('Total time : ' + str(time2 - time1))
    print('DONE !!!!')


if __name__ == '__main__':
    main()
