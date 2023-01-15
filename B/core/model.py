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

class UserTopics(DynamicDocument):
    id_ = StringField(default=str(uuid1(random.getrandbits(48) | 0x010000000000)))
    date_created = DateTimeField(default=datetime.datetime.utcnow)

def update_transactions_db(dict_data):
    """A function to update db
    :param dict_data: text data to push to db
    :type dict_data: dict
    """
    dict_data_orig = dict_data
    keys_values = dict_data.items()
    dict_data = {str(key): str(value) for key, value in keys_values}
    transactions = Transactions() 
    field_keys = dict_data.keys()
    for item in field_keys:
        field_value = str(dict_data[item])
        item = str(item)
        transactions.__setattr__(item, field_value )
    transactions.__setattr__("record_data", dict_data_orig )
    id_ = str(uuid1(random.getrandbits(48) | 0x010000000000))
    transactions.__setattr__("id_", str(id_))
    transactions.save()
    return True

def update_topics_db(dict_data):
    """A function to update db
    :param dict_data: text data to push to db
    :type dict_data: dict
    """
    dict_data_orig = dict_data
    keys_values = dict_data.items()
    dict_data = {str(key): str(value) for key, value in keys_values}
    userTopics = UserTopics() 
    field_keys = dict_data.keys()
    for item in field_keys:
        field_value = str(dict_data[item])
        item = str(item)
        userTopics.__setattr__(item, field_value )
    userTopics.__setattr__("record_data", dict_data_orig )
    id_ = str(uuid1(random.getrandbits(48) | 0x010000000000))
    userTopics.__setattr__("id_", str(id_))
    userTopics.save()

    return True
