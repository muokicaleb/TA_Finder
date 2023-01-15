import os
import traceback
from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler
from uuid import uuid4
from .model import update_transactions_db, update_topics_db
import demoji


CONSUMER_KEY=os.getenv('CONSUMER_KEY')
CONSUMER_SECRET=os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN=os.getenv('ACCESS_TOKEN')
ACCESS_SECRET=os.getenv('ACCESS_SECRET')


# initialize the tweepy api
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = API(auth, wait_on_rate_limit=True)


def get_users_tweets(user_id):
    tweets = api.user_timeline(user_id=user_id, 
                           # 200 is the maximum allowed count
                           count=200,
                           include_rts = False,
                           # Necessary to keep full_text 
                           # otherwise only the first 140 words are extracted
                           tweet_mode = 'extended'
                           )
    return tweets


def clear_tweet_text(txt):
    removed_mention = ' '.join(word for word in txt.split() if word[0]!='@')
    no_emoji = demoji.replace(removed_mention, "")
    return no_emoji
 

def run(dict_data):
    try:
        user_id, transaction_id = dict_data['follower_id'], dict_data['transaction_id']
        all_tweets = get_users_tweets(user_id)
        users_topics = [ clear_tweet_text(item.full_text)
                        for item in all_tweets] + [ clear_tweet_text(all_tweets[0].user.description)]
        print("Got topics")

        _ = update_transactions_db({ "transaction_id":transaction_id,
                                    "user_id":user_id,
                                    "topics":users_topics})

    # _ = [update_topics_db(item) for item in users_topics]
    except:
        traceback.print_exc()

    

