import os
import traceback
from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler
from uuid import uuid4 
from .rabbit import add_followers
from .model import Transactions
from collections import Counter
from ast import literal_eval


CONSUMER_KEY=os.getenv('CONSUMER_KEY')
CONSUMER_SECRET=os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN=os.getenv('ACCESS_TOKEN')
ACCESS_SECRET=os.getenv('ACCESS_SECRET')


# initialize the tweepy api
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = API(auth, wait_on_rate_limit=True)

def get_users_followers(twiiter_handle):
    follower_ids = []
    cursor_items = Cursor(api.get_follower_ids,
                      screen_name = twiiter_handle, count = 5000).pages()
    for page in cursor_items:
        follower_ids.extend(page)
    return follower_ids 

def publish_followers(follower_list, transaction_id):
    for item in follower_list:
        add_followers({
            "transaction_id": transaction_id,
            "follower_id": item
        })
        

def run(query):
    target_account = query.twitterUser
    result_recipient = query.email
    try:
        followers_list = get_users_followers(target_account)
        transaction_id = str(uuid4())
        publish_followers(followers_list, transaction_id)
        return {"transaction_id": transaction_id,
                 "result_recipient": result_recipient }
        
    except:
        traceback.print_exc()
        return {"message": "failed to get user details"}

def format_dict(dictdata, len_list):
    result = []
    print(dictdata)
    for x, y in dictdata.items():
        new_dict = {"topic":x, "percent":y*100/len_list}
        result.append(new_dict)
    return result

def search_db(transaction_id):
    all_matches = Transactions.objects(transaction_id= transaction_id)
    topics_lists = [literal_eval(item.topics) for item in all_matches]
    print(topics_lists)
    print(len(topics_lists))
    topics = [ item for elem in topics_lists for item in elem]
    len_topics = len(topics)
    topics_dict = dict(Counter(topics).most_common())
    return format_dict(topics_dict, len_topics)

def get_ta_result(transaction_id):
    return {"transaction_id": transaction_id,
            "TA":search_db(transaction_id)}
