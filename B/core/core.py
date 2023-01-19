import os
import traceback
from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler
from uuid import uuid4
from .model import update_transactions_db, update_topics_db
import demoji
import requests

CONSUMER_KEY=os.getenv('CONSUMER_KEY')
CONSUMER_SECRET=os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN=os.getenv('ACCESS_TOKEN')
ACCESS_SECRET=os.getenv('ACCESS_SECRET')
SEMANTIC_SERVICE_URL=os.getenv('SEMANTIC_SERVICE_URL')


# initialize the tweepy api
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = API(auth, wait_on_rate_limit=True)


def get_users_tweets(user_id):
    tweets = api.user_timeline(user_id=user_id, 
                           count=200,
                           include_rts = False,
                           tweet_mode = 'extended'
                           )
    return tweets


def clear_tweet_text(txt):
    removed_mention = ' '.join(word for word in txt.split() if word[0]!='@')
    no_emoji = demoji.replace(removed_mention, "")
    #print(removed_mention)
    return no_emoji
 
def get_topics(txt_list):

    payload = {"sentences": txt_list}
    print(len(txt_list))

    response = requests.post(SEMANTIC_SERVICE_URL, 
                             json = payload, verify=False)

    return response.json()["topics"]

def run(dict_data):
    try:
        user_id = dict_data['follower_id']
        transaction_id = dict_data['transaction_id']
        all_tweets = get_users_tweets(user_id)
        users_sentences = [clear_tweet_text(item.full_text)
                        for item in all_tweets] + [ 
                            clear_tweet_text(all_tweets[0].user.description)]
        users_sentences = [x for x in users_sentences if x]
        users_topics = get_topics(users_sentences)
        

        _ = update_transactions_db({ "transaction_id":transaction_id,
                                     "user_id":user_id,
                                     "topics":users_topics})
    except:
        traceback.print_exc()
