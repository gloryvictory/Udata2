from peewee import *

# https://github.com/sinscary/Flask-Social-Networking
# good example of peewee using

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
        # indexes = (
        #     # create a unique on ...
        #     (('compname'), True),)
