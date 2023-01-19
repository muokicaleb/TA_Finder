from mongoengine import *
import datetime
from uuid import uuid4, uuid1
import random
import os


hostip = os.getenv("MONGO_DB_URL") 
username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
mongopassword = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

connect('transactiondb', username=username, password=mongopassword, host=hostip,
        port=27017, authentication_source='admin',connect=False)


class Transactions(DynamicDocument):
    id_ = StringField(default=str(uuid1(random.getrandbits(48) | 0x010000000000)))
    date_created = DateTimeField(default=datetime.datetime.utcnow)





    

