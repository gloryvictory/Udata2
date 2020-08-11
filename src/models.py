from datetime import datetime

# non standard packages
try:
    from peewee import *
except Exception as e:
    print("Exception occurred " + str(e))
    print("try: pip install peewee")

import cfg  # some global configurations

# https://github.com/sinscary/Flask-Social-Networking
# good example of peewee using

db = PostgresqlDatabase(cfg.database, host=cfg.host, port='5432', user=cfg.user, password=cfg.user_password,
                        autocommit=True, autorollback=True)
db.connect()

# Model for our entry table
class Udata(Model):
    compname = CharField(max_length=250, default="")
    disk = CharField(max_length=1, default="")
    fullname = TextField(default="")  # CharField(max_length=250, default="")
    size = BigIntegerField(default=0)  # Length - in csv;
    ctime = DateTimeField(default=datetime.now)
    mtime = DateTimeField(default=datetime.now)
    atime = DateTimeField(default=datetime.now)
    filename_long = CharField(max_length=250, default="")  # name in CSV File
    ext_long = CharField(max_length=250, default="")
    ext_shot = CharField(max_length=250, default="")  # extension in CSV File
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
        db_table = "UDATA"
        # indexes = (
        #     # create a unique on ...
        #     (('compname'), True),)

        # order_by = ('created_at',)