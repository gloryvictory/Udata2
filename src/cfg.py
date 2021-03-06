#import time
from time import strftime   # Load just the strftime Module from Time

file_csv = str(strftime("%Y-%m-%d") + "01_csv_to_pg" + ".csv")
file_log = str(strftime("%Y-%m-%d") + "01_csv_to_pg" + ".log")

folder_in_win = 'E:\\Temp\\csv_test'
#folder_win_in = 'E:\\Temp\\geodex_test'
folder_in_linux = '/Users/glory/projects/CSV_ALL'

folder_out_win = 'E:\\TEMP\\csv_test'
folder_out_linux = '/Users/glory/projects/out'


host = '10.57.10.45'
schema = 'udataschema'
user = 'udatauser2'
user_password = 'udatauser2pwd'
database = 'udatadb2'
# postgresql://udatauser2:udatauser2pwd@localhost:5432/udatadb2

csv_delimiter = ';'

csv_fieldnames_in = ['compname','FullName','Length','CreationTime', 'ModifiedTime','AccessTime','Name','Extension','MD5']


csv_dict = {'COMPNAME': '',
            'DISK': '',
            'FOLDER': '',
            'IS_PROFILE': '',
            'FILENAME_LONG': '',
            'FILENAME_SHOT': '',
            'EXT_LONG': '',
            'EXT_SHOT': '',
            'SIZE': '',
            'FULLNAME': '',
            'DATE': '',
            'YEAR': '',
            'MONTH': '',
            'CREATIONTIME': '',
            'FIO': '',
            'OTDEL': '',
            'TEXTFULL': '',
            'TEXTLESS': '',
            'LASTUPDATE': ''}
